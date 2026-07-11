#!/usr/bin/env bash
# level02 - recover flag02's telnet password from level02.pcap (needs tshark).
#
# Telnet sends keystrokes in plaintext, so the password is in the capture. The only
# twist is that the typist used the Backspace/Delete key (byte 0x7f), which we replay.
#
# The pipeline, one obvious step per stage:
#   tshark : decode port 12121 as telnet, print the client's typed data (IAC removed)
#   tr     : glue the per-packet keystrokes into one stream
#   sed    : the Enter key (tshark writes it as \r) becomes a line break
#   perl   : replay Backspace - delete every "character + 0x7f" pair
#   tail   : the password is the last line typed
#
# Usage: ./extract_password.sh [level02.pcap]

tshark -r "${1:-level02.pcap}" -d tcp.port==12121,telnet \
       -Y 'tcp.dstport==12121 && telnet.data' -T fields -e telnet.data 2>/dev/null \
  | tr -d '\n' \
  | sed 's/\\r/\n/g' \
  | perl -pe '1 while s/[^\x7f]\x7f//' \
  | tail -1
