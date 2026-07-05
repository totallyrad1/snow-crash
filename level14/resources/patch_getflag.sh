#!/bin/sh
# level14 exploit.
#
# /bin/getflag is NOT setuid (root:root 0755). It computes each flag user's token
# as ft_des(<per-uid constant>) and prints it only when getuid() matches that flag
# account. It defends itself with four anti-tamper checks, ALL of which pass for a
# normal (untampered) execution -- they exist only to catch gdb / LD_PRELOAD:
#   1. ptrace(PTRACE_TRACEME,..)   -> fails under a debugger  ("You should not reverse this")
#   2. getenv("LD_PRELOAD")        -> non-NULL if you preload
#   3. open("/etc/ld.so.preload")  -> succeeds if you use that file
#   4. read /proc/self/maps        -> every mapped lib must be libc or ld (whitelist)
#
# So the trick is NOT to inject anything: run a *copy* and statically patch the
# `call getuid@plt` at 0x8048afd (bytes e8 ae f9 ff ff) into `mov $uid,%eax`
# (b8 <uid little-endian> 00 00) -- exactly 5 bytes. The copy runs untampered
# (no gdb, no preload, /etc/ld.so.preload absent, maps only libc/ld), so all four
# checks pass, while eax is forced to flag14's uid (3014 = 0xbc6).

D=/tmp/l14x
rm -rf "$D"; mkdir -p "$D"; cd "$D"

patch_and_run() {          # $1 = uid low bytes little-endian, $2 = label
  cp /bin/getflag "$D/gf"
  python2 -c "
f=open('$D/gf','r+b'); f.seek(0xafd)
assert f.read(5)=='\xe8\xae\xf9\xff\xff'          # call getuid@plt
f.seek(0xafd); f.write('\xb8$1\x00\x00'); f.close()  # mov \$uid,%eax
"
  chmod 755 "$D/gf"
  printf '%s: ' "$2"; "$D/gf"
}

# 0xbb8 = 3000 (flag00): proves correctness -> x24ti5gi3x0ol2eh4esiuxias
patch_and_run '\xb8\x0b' 'validate flag00(3000)'
# 0xbc6 = 3014 (flag14): the real target
patch_and_run '\xc6\x0b' 'TARGET   flag14(3014)'
