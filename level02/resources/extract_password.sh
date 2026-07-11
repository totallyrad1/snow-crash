#!/usr/bin/env bash
#
# level02 - recover the telnet password from level02.pcap.
#
# Telnet sends every keystroke in plaintext, so the typed password is right there in
# the capture. The only twist: the person used the Backspace/Delete key (byte 0x7f)
# to fix typos, so we "replay" those deletes to get the final, corrected password.
#
# Usage: ./extract_password.sh [level02.pcap]

set -euo pipefail
PCAP="${1:-level02.pcap}"

# The telnet server runs on the non-standard port 12121, so we tell tshark to decode
# that port as telnet with '-d tcp.port==12121,telnet'. The 'telnet.data' field is the
# application data with telnet's own IAC negotiation already stripped out for us. We
# keep only the client->server direction (tcp.dstport==12121) = exactly what was typed
# (not the server's echo).
tshark -r "$PCAP" -d tcp.port==12121,telnet \
       -Y 'tcp.dstport == 12121 && telnet.data' \
       -T fields -e telnet.data 2>/dev/null \
  | tr -d '\n' \
  | perl -0777 -ne '
      s/\\r/\n/g; tr/\r/\n/;                 # tshark shows the Enter key as \r -> line break
      $pw = ""; for (split /\n/) { $pw = $_ if /\S/ }   # the last line typed is the password
      1 while $pw =~ s/[^\x7f]\x7f//;         # each Backspace (0x7f) erases the char before it
      print "password: $pw\n";
    '
