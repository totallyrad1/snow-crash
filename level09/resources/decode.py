#!/usr/bin/env python3
"""level09 - decode the ~/token file.

The level09 SUID binary encodes a string by adding each character's INDEX to it
(byte[i] = original[i] + i). To recover the password we do the inverse:
original[i] = byte[i] - i.

Usage: ./decode.py token
"""
import sys

data = open(sys.argv[1], "rb").read()
out = []
for i, b in enumerate(data):
    c = (b - i) & 0xff
    if c == 0x0a:            # trailing newline in the token file
        continue
    out.append(chr(c))
print("".join(out))
