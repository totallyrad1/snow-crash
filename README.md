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
| 05 | Cron | World-writable dir run by a flag05 cron job | done |
| 06 | Code injection | PHP `preg_replace /e` (backtick operator) | done |
| 07 | SUID / env | `LOGNAME` command injection | done |
| 08 | Access control | symlink bypass of a substring filter | done |
| 09 | Crypto | per-index byte-offset encoding | done |
| 10 | Race (bonus) | `access()`/`open()` TOCTOU over network | done |
| 11 | Injection (bonus) | Lua `io.popen` daemon injection | done |
| 12 | Injection (bonus) | Perl CGI injection (glob bypass of uppercasing) | done |
| 13 | SUID (bonus) | `getuid()` bypass via LD_PRELOAD on a copy | done |
| 14 | Reversing (bonus) | gdb: edit eax past ptrace check + spoof getuid() | done |

## Credentials / tokens (proof)

Each `levelXX` logs in with the token printed by `getflag` in the previous level.

| Login | Password (token) | How obtained |
|-------|------------------|--------------|
| level00 | `level00` | given by subject |
| level01 | `x24ti5gi3x0ol2eh4esiuxias` | getflag as flag00 |
| level02 | `f2av5il02puano7naaf6adaaf` | getflag as flag01 |
| level03 | `kooda2puivaav1idi4f57q8iq` | getflag as flag02 |
| level04 | `qi0maab88jeaj46qoumi7maus` | getflag as flag03 |
| level05 | `ne2searoevaevoem4ov4ar8ap` | getflag as flag04 |
| level06 | `viuaaale9huek52boumoomioc` | getflag as flag05 |
| level07 | `wiok45aaoguiboiki2tuin6ub` | getflag as flag06 |
| level08 | `fiumuikeil55xe9cu4dood66h` | getflag as flag07 |
| level09 | `25749xKZ8L7DkSCwJkT9dyv6f` | getflag as flag08 |
| level10 | `s5cAJpM8ev6XHw998pRWG728z` | getflag as flag09 |
| level11 | `feulo4b72j7edeahuete3no7c` | getflag as flag10 |
| level12 | `fa6v5ateaw21peobuub8ipe6s` | getflag as flag11 |
| level13 | `g1qKMiRpXf53AWhDaU7FEkczr` | getflag as flag12 |
| level14 | `2A31L79asukciNyi8uppkEuSx` | level13 binary (LD_PRELOAD getuid) |
| flag14 (final) | `7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ` | patched getflag |

Intermediate `flagXX` passwords recovered along the way (see per-level walkthroughs):
flag00 `nottoohardhere`, flag01 `abcdefg`, flag02 `ft_waNDReL0L`,
flag08 `quif5eloekouj29ke0vouxean`, flag09 `f3iji1ju5yuevaus41q1afiuq`,
flag10 `woupa2yuojeeaaed06riuj63c`.

> The subject PDF and Windows `Zone.Identifier` artifacts are git-ignored: the
> resource folders must contain no binary files.
