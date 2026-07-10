#!/usr/bin/env python3
"""level02 - reconstruct the password typed in the telnet session captured in
level02.pcap.

Usage:
    ./reconstruct.py level02.pcap      # parse the capture directly (no tshark needed)
    ./reconstruct.py c2s.hex           # legacy: client->server TCP payloads as hex lines

The script:
  1. reads a classic pcap (Ethernet/IPv4/TCP), finds the telnet server via the SYN,
     and reassembles the client->server byte stream (the keystrokes);
  2. removes telnet IAC negotiation (including variable-length IAC SB..IAC SE blocks);
  3. replays the terminal edits: 0x7f/0x08 are destructive backspaces, 0x0d submits a
     line, 0x00/0x0a are ignored.
The password is the last non-empty reconstructed line.
"""
import sys

PCAP_MAGIC_LE = b"\xd4\xc3\xb2\xa1"   # microsecond, little-endian
PCAP_MAGIC_BE = b"\xa1\xb2\xc3\xd4"   # microsecond, big-endian
PCAPNG_MAGIC  = b"\x0a\x0d\x0d\x0a"


def u16(b, o, le):
    return int.from_bytes(b[o:o + 2], "little" if le else "big")


def u32(b, o, le):
    return int.from_bytes(b[o:o + 4], "little" if le else "big")


def parse_pcap(data):
    """Return the reassembled client->server TCP payload of the (first) telnet flow."""
    if data[:4] == PCAP_MAGIC_LE:
        le = True
    elif data[:4] == PCAP_MAGIC_BE:
        le = False
    elif data[:4] == PCAPNG_MAGIC:
        sys.exit("error: this is a pcapng file; re-save as classic pcap "
                 "(tshark -F pcap -r in.pcapng -w out.pcap) or pass a c2s.hex file")
    else:
        return None  # not a pcap

    linktype = u32(data, 20, le)
    if linktype != 1:
        sys.exit("error: link-layer type %d is not Ethernet (1)" % linktype)

    server = None                 # (dst_ip, dst_port) taken from the SYN
    segments = []                 # (seq, payload) client->server data segments
    off = 24                      # past the global header
    n = len(data)
    while off + 16 <= n:
        incl_len = u32(data, off + 8, le)
        pkt = data[off + 16:off + 16 + incl_len]
        off += 16 + incl_len

        # --- Ethernet ---
        if len(pkt) < 14:
            continue
        etype = int.from_bytes(pkt[12:14], "big")
        l3 = 14
        while etype == 0x8100 and len(pkt) >= l3 + 4:      # VLAN tag(s)
            etype = int.from_bytes(pkt[l3 + 2:l3 + 4], "big")
            l3 += 4
        if etype != 0x0800:                                # only IPv4
            continue

        # --- IPv4 ---
        ip = pkt[l3:]
        if len(ip) < 20 or (ip[0] >> 4) != 4:
            continue
        ihl = (ip[0] & 0x0f) * 4
        if ip[9] != 6:                                     # protocol 6 = TCP
            continue
        src_ip = ".".join(str(x) for x in ip[12:16])
        dst_ip = ".".join(str(x) for x in ip[16:20])

        # --- TCP ---
        tcp = ip[ihl:]
        if len(tcp) < 20:
            continue
        src_port = int.from_bytes(tcp[0:2], "big")
        dst_port = int.from_bytes(tcp[2:4], "big")
        seq = int.from_bytes(tcp[4:8], "big")
        data_off = (tcp[12] >> 4) * 4
        flags = tcp[13]
        payload = tcp[data_off:]

        syn, ack = flags & 0x02, flags & 0x10
        if syn and not ack and server is None:             # client's SYN -> server side
            server = (dst_ip, dst_port)

        if payload and server is not None and (dst_ip, dst_port) == server:
            segments.append((seq, bytes(payload)))

    if server is None:
        sys.exit("error: no TCP SYN found; cannot determine the telnet server")

    # reassemble by sequence number (handles reordering / duplicate retransmits)
    segments.sort(key=lambda s: s[0])
    stream = bytearray()
    next_seq = None
    for seq, payload in segments:
        if next_seq is None or seq == next_seq:
            stream += payload
            next_seq = seq + len(payload)
        elif seq > next_seq:                               # gap (missing segment)
            stream += payload
            next_seq = seq + len(payload)
        # seq < next_seq -> already-seen bytes, skip
    return bytes(stream)


def strip_telnet(data):
    """Remove telnet IAC commands, including variable-length IAC SB .. IAC SE."""
    out = bytearray()
    i, n = 0, len(data)
    while i < n:
        b = data[i]
        if b != 0xff:                    # normal byte
            out.append(b)
            i += 1
            continue
        if i + 1 >= n:                   # dangling IAC
            break
        cmd = data[i + 1]
        if cmd == 0xff:                  # escaped literal 0xff
            out.append(0xff)
            i += 2
        elif cmd in (0xfb, 0xfc, 0xfd, 0xfe):   # WILL/WONT/DO/DONT + option
            i += 3
        elif cmd == 0xfa:                # SB .. IAC SE (variable length)
            j = i + 2
            while j + 1 < n and not (data[j] == 0xff and data[j + 1] == 0xf0):
                j += 1
            i = j + 2
        else:                            # other 2-byte commands (SE, NOP, GA, ...)
            i += 2
    return bytes(out)


def replay_keystrokes(data):
    line, lines = [], []
    for b in data:
        if b in (0x7f, 0x08):            # backspace / delete
            if line:
                line.pop()
        elif b == 0x0d:                  # carriage return -> submit line
            lines.append(bytes(line).decode("latin1"))
            line = []
        elif b in (0x00, 0x0a):          # telnet NUL padding / LF: ignore
            pass
        else:
            line.append(b)
    if line:
        lines.append(bytes(line).decode("latin1"))
    return lines


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: %s <level02.pcap | c2s.hex>" % sys.argv[0])

    raw = open(sys.argv[1], "rb").read()
    stream = parse_pcap(raw)
    if stream is None:                   # legacy hex-lines input
        stream = bytearray()
        for line in raw.decode("latin1").splitlines():
            line = line.strip()
            if line:
                stream += bytes.fromhex(line)
        stream = bytes(stream)

    lines = replay_keystrokes(strip_telnet(stream))
    nonempty = [l for l in lines if l]
    for l in lines:
        print("line:", repr(l))
    if not nonempty:
        sys.exit("error: no printable input recovered")
    print("password:", nonempty[-1])


if __name__ == "__main__":
    main()
