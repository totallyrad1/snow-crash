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

## The self-defense checks
Disassembly of `main` shows four anti-tamper checks (each prints and exits):

1. `ptrace(PTRACE_TRACEME, 0, 1, 0)` returns **-1 under a debugger** -> "You should
   not reverse this". (`test eax,eax; jns ok` - it continues only if `eax >= 0`.)
2. `getenv("LD_PRELOAD")` non-NULL -> "LD_PRELOAD detected".
3. `open("/etc/ld.so.preload")` succeeds -> preload-file detected.
4. reads `/proc/self/maps` with a raw `syscall_open` and requires every mapped
   library to be `libc` or `ld` (via `isLib`) -> "LD_PRELOAD detected through memory maps".

Checks 2-4 exist to stop `LD_PRELOAD`. Indeed `LD_PRELOAD=./getuid.so getflag` was
caught twice (getenv, then the memory-map scan). But **a debugger injects no library
and sets no `LD_PRELOAD`**, so under gdb checks 2-4 pass on their own - only check 1
(ptrace) trips, and we defeat it by editing a register.

## Exploit - gdb: edit `eax` past the ptrace check, then spoof `getuid()`
`getflag` is not setuid, so we can run it directly under gdb and make two register edits:

- after `ptrace` returns `-1`, set `eax` to a non-negative value so the anti-debug
  branch (`jns`) is taken and we continue;
- after `getuid` returns our real uid, set `eax` to `3014` (flag14) so the switch
  dispatches to flag14's case.

```gdb
$ gdb -q /bin/getflag
(gdb) break ptrace
(gdb) run
                        # stops at ptrace
(gdb) finish            # let ptrace run and return to main; eax = -1 (we are traced)
(gdb) set $eax = 0      # pretend ptrace succeeded -> passes `test eax,eax; jns`
(gdb) break getuid
(gdb) continue          # getenv / open / maps checks pass on the way (no preload)
                        # stops at getuid
(gdb) finish            # let getuid return; eax = 2014 (level14)
(gdb) set $eax = 3014   # 0xbc6 = flag14's uid
(gdb) continue
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```

(`finish` stops on return to `main`, at the instruction right after the call, before
`test`/the switch runs - so overwriting `eax` there changes what those instructions see.)

## Why it works
gdb drives the process with `ptrace`, but it **maps nothing into the target's address
space** and sets no environment variable, so `/proc/self/maps` stays clean (libc + ld)
and `getenv("LD_PRELOAD")` is NULL - checks 2-4 never fire. The only tell is check 1:
a process can have at most one tracer, so `PTRACE_TRACEME` fails (`-1`) while gdb is
attached. Forcing `eax >= 0` hides that. The token is computed **inside** getflag as
`ft_des(<per-uid constant>)`, so once `getuid` appears to return 3014, getflag builds
and prints flag14's token with no privileges required.

## Verification
Spoofing to uid **3000 (flag00)** instead - `set $eax = 3000` at the getuid step -
prints `x24ti5gi3x0ol2eh4esiuxias`, flag00's known token from level00. That proves the
value is genuinely getflag's own output, not something fabricated.

## Alternative (no debugger): static patch
The same result without gdb: run a **copy** and overwrite the `call getuid@plt` at
`0x8048afd` (`e8 ae f9 ff ff`) with `mov $0xbc6,%eax` (`b8 c6 0b 00 00`, same 5 bytes).
The copy runs untampered so all four checks pass, and `eax` is forced to 3014.

## Result
- **flag14 token (final):** `7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ`

Project complete: level00-level09 (mandatory) + level10-level14 (bonus) = 125%.
