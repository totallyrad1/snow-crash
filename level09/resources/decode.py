#!/usr/bin/env python3
# level09: the binary encodes a string as  byte[i] = original[i] + i.
# So we decode by subtracting each byte's index:  original[i] = byte[i] - i.
#
# Usage: ./decode.py token
import sys

data = open(sys.argv[1], "rb").read().rstrip(b"\n")   # read the token, drop trailing newline

password = ""
for i in range(len(data)):
    password += chr(data[i] - i)                       # undo "+ index"
print(password)
