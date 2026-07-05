# level01

## Goal
Find `flag01`'s password, run `getflag`, obtain the `level02` token.

## Recon
Nothing is owned by `flag01`, but the historical mistake is in `/etc/passwd`:
instead of an `x` (which means "hash is in the shadow file"), `flag01` stores its
password hash directly in the second field:

```sh
$ grep flag01 /etc/passwd
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

`42hDRfypTqqnw` is a 13-character **traditional DES `crypt(3)`** hash. The first two
characters (`42`) are the salt.

## Exploit
This is an offline hash-cracking problem (not SSH brute force, which is forbidden).
Copy the passwd line locally and run John the Ripper:

```sh
$ echo 'flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash' > hash.txt
$ john --format=descrypt hash.txt
$ john --show --format=descrypt hash.txt
flag01:abcdefg:3001:3001::/home/flag/flag01:/bin/bash
```

Password: **`abcdefg`** (john finds it almost instantly in single/wordlist mode
because it is a trivial lowercase string).

## Getflag
```sh
$ ssh flag01@<VM> -p 4242       # password: abcdefg
flag01@SnowCrash$ getflag
Check flag.Here is your token : f2av5il02puano7naaf6adaaf
```

## Result
- **flag01 password:** `abcdefg`
- **level02 password (token):** `f2av5il02puano7naaf6adaaf`
