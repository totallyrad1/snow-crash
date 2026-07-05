# Snow Crash

42 security project. A boot-to-root wargame: starting from `level00:level00` over
SSH (port `4242`), each level requires finding the password of the matching
`flagXX` account by exploiting the machine (weak permissions, SUID binaries,
source-code review, command injection, cracking, races, etc.). Running `getflag`
as `flagXX` prints a **token**, which is the password for the next `levelXX` account.

- **Mandatory:** level00 - level09
- **Bonus:** level10 - level14

## Repository layout

Each level lives in its own folder:

```
levelXX/
  flag                    # the getflag token for that level (= next level's password)
  resources/
    walkthrough.md        # how the level was solved, step by step
    ...                   # any scripts/notes used (text only, no binaries)
```

## How to reproduce

```sh
ssh levelXX@<VM-IP> -p 4242
```

The VM boots from the project ISO and prints its IP at the login prompt.

## Progress

| Level | Category | Technique | Status |
|-------|----------|-----------|--------|
| 00 | Encoding | Caesar-cipher (ROT+11) decode of a flag-owned file | done |
| 01 | Password cracking | DES `crypt` hash in `/etc/passwd` | done |
| 02 | Forensics | Recover password from a tcpdump capture | done |
| 03 | SUID / PATH | `$PATH` hijack of a relative command call | done |
| 04 | SUID / web | Perl CGI command injection (backticks) | done |
| 05 | Cron | Writable script run as flag via cron | pending |
| 06 | Code injection | PHP `preg_replace /e` | pending |
| 07 | SUID / env | `LOGNAME` command injection | pending |
| 08 | Access control | token file access bypass | pending |
| 09 | Crypto | per-index byte-offset encoding | pending |
| 10 | Race (bonus) | `access()`/`open()` TOCTOU over network | pending |
| 11 | Injection (bonus) | Lua `os.execute` daemon | pending |
| 12 | Injection (bonus) | Perl CGI over HTTP | pending |
| 13 | SUID (bonus) | `getuid()` check bypass | pending |
| 14 | Reversing (bonus) | final token recovery | pending |

> The subject PDF and Windows `Zone.Identifier` artifacts are git-ignored: the
> resource folders must contain no binary files.
