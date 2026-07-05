# level14 (bonus) - final level

## Goal
Obtain `flag14`'s token. There is no `level15`: this token is the end of the project.

## Recon
The home directory is empty and nothing is owned by `flag14`. The only relevant
program is `/bin/getflag` itself, which is **not setuid** (`root:root 0755`) and
`not stripped`:

```sh
$ ls -l /bin/getflag
-rwxr-xr-x 1 root root 11833 Aug 30  2015 /bin/getflag
$ objdump -t /bin/getflag | grep 'F .text'
... ft_des ... isLib ... syscall_open ... syscall_gets ... main
```

`getflag` reads `getuid()` and prints `ft_des(<constant>)` for the matching flag
account. Because it is not setuid, running it as us just yields "Nope there is no
token here for you sorry." We must make it believe it runs as `flag14` (uid 3014).

## Why the easy tricks fail
Disassembly of `main` shows four self-defense checks (each prints and exits):

1. `ptrace(PTRACE_TRACEME, 0, 1, 0)` - returns -1 under a debugger.
   -> blocks **gdb** ("You should not reverse this").
2. `getenv("LD_PRELOAD")` non-NULL -> blocks env-visible preload.
3. `open("/etc/ld.so.preload")` succeeds -> blocks that preload file.
4. reads `/proc/self/maps` with a raw `syscall_open` and requires every mapped
   library to be `libc` or `ld` (via `isLib`) -> blocks **any** injected `.so`.

Indeed, `LD_PRELOAD=./getuid.so getflag` was caught two different ways:
`LD_PRELOAD detected` (getenv), then `LD_PRELOAD detected through memory maps`.

## Exploit - patch a copy, inject nothing
The four checks only fire when you *tamper* at runtime (debugger/preload). They all
pass for a normal execution. So run an untampered **copy** and change what `getuid`
returns by **static binary patching** - no debugger, no preload, nothing in maps.

At `0x8048afd` the code is `call getuid@plt` = `e8 ae f9 ff ff` (5 bytes). Replace it
with `mov $uid,%eax` = `b8 <uid_le> 00 00` (also 5 bytes). eax then holds the flag
uid and the switch prints that flag's `ft_des` token.

```sh
$ cp /bin/getflag /tmp/gf
# offset 0xafd = 0x8048afd - 0x8048000 ; 0xbc6 = 3014 (flag14)
$ python2 -c "f=open('/tmp/gf','r+b');f.seek(0xafd);f.write('\xb8\xc6\x0b\x00\x00');f.close()"
$ /tmp/gf
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```

See `patch_getflag.sh`.

## Proof of correctness
Patching to uid **3000 (flag00)** instead makes the same copy print
`x24ti5gi3x0ol2eh4esiuxias` - identical to the token `getflag` gave us as the real
flag00 back in level00. That confirms the patch reproduces getflag's own output.

## Result
- **flag14 token (final):** `7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ`

Project complete: level00-level09 (mandatory) + level10-level14 (bonus) = 125%.
