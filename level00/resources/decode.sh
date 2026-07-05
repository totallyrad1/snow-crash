#!/usr/bin/env bash
# level00: decode the contents of /usr/sbin/john (a Caesar cipher).
# The correct key is a forward shift of +11.
# Usage: ./decode.sh [ciphertext]   (defaults to the value found on the box)
cipher="${1:-cdiiddwpgswtgt}"
echo "$cipher" | awk -v s=11 '{
  r="";
  for (i = 1; i <= length($0); i++) {
    c = substr($0, i, 1);
    o = index("abcdefghijklmnopqrstuvwxyz", c);
    if (o > 0) r = r substr("abcdefghijklmnopqrstuvwxyz", (o - 1 + s) % 26 + 1, 1);
    else       r = r c;
  }
  print r
}'
