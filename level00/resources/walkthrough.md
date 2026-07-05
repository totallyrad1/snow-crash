# level00

## Goal
Find the password of `flag00`, run `getflag`, obtain the token that is the
password for `level01`.

## Recon
Log in and look for anything owned by `flag00`:

```sh
ssh level00@<VM> -p 4242        # password: level00
find / -user flag00 -not -path "*/proc/*" 2>/dev/null
```

```
/usr/sbin/john
/rofs/usr/sbin/john
```

Both are the same file (`/rofs` is the read-only squashfs; `/usr/sbin/john` is the
live copy). It is world-readable:

```sh
$ ls -l /usr/sbin/john
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /usr/sbin/john
$ cat /usr/sbin/john
cdiiddwpgswtgt
```

## Exploit
`cdiiddwpgswtgt` is 14 lowercase letters -> a monoalphabetic substitution. Trying
Caesar shifts, a forward shift of **+11** (equivalently ROT-15 backward) yields a
readable English string:

```sh
$ ./decode.sh
nottoohardhere
```

That is the password for `flag00`.

## Getflag
```sh
$ ssh flag00@<VM> -p 4242       # password: nottoohardhere
flag00@SnowCrash$ getflag
Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias
```

## Result
- **flag00 password:** `nottoohardhere`
- **level01 password (token):** `x24ti5gi3x0ol2eh4esiuxias`
