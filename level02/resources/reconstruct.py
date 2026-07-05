#!/usr/bin/env python3
"""level02 - reconstruct the password typed in the telnet session captured in
level02.pcap.

Feed it the client->server TCP payloads (hex, one packet per line), e.g.:

    tshark -r level02.pcap -Y 'tcp.srcport==39247 && tcp.len>0' \
           -T fields -e tcp.payload > c2s.hex
    ./reconstruct.py c2s.hex

The telnet negotiation bytes (IAC = 0xff followed by command/option) are stripped,
then 0x7f / 0x08 are applied as destructive backspaces, and 0x0d ends a line.
The password is the last reconstructed line.
"""
import sys

raw = bytearray()
for line in open(sys.argv[1]):
    line = line.strip()
    if line:
        raw += bytes.fromhex(line)

# strip telnet IAC negotiations (0xff + 2 bytes); good enough for this capture
clean = bytearray()
i = 0
while i < len(raw):
    if raw[i] == 0xff:
        i += 3
        continue
    clean.append(raw[i])
    i += 1

# apply keystroke semantics
line, lines = [], []
for b in clean:
    if b in (0x7f, 0x08):        # backspace / delete
        if line:
            line.pop()
    elif b == 0x0d:              # carriage return -> submit line
        lines.append(bytes(line).decode("latin1"))
        line = []
    elif b in (0x00, 0x0a):      # telnet NUL padding / LF: ignore
        pass
    else:
        line.append(b)
if line:
    lines.append(bytes(line).decode("latin1"))

print("password:", lines[-1])
