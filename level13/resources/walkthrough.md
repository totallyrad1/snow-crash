# level13 (bonus)

## Goal
Get the token printed by the `level13` SUID binary.

## Recon
```sh
$ ls -l ~
-rwsr-sr-x 1 flag13 level13 7303 Aug 30  2015 level13
$ ~/level13
UID 2013 started us but we we expect 4242
$ strings ~/level13 | grep -E 'getuid|4242|token'
getuid
UID %d started us but we we expect %d
your token is %s
```

The binary calls `getuid()`; unless it returns **4242** it exits. Otherwise it prints
`your token is <TOKEN>`. Crucially the token is **computed inside the binary**, so we
don't need flag13's privileges - we only need to pass the `getuid()` check.

## Exploit - LD_PRELOAD a fake getuid()
We can't `setuid(4242)`. `LD_PRELOAD` would let us override `getuid()`, but the loader
**ignores LD_PRELOAD for setuid binaries**. So we run a **non-setuid copy** of the
binary (copying drops the setuid bit) with our preload:

```sh
cp ~/level13 /tmp/l13x/level13
echo 'uid_t getuid(void){return 4242;}' > getuid.c   # + <sys/types.h>
gcc -shared -fPIC getuid.c -o getuid.so              # 32-bit box -> matching .so
LD_PRELOAD=/tmp/l13x/getuid.so /tmp/l13x/level13
your token is 2A31L79asukciNyi8uppkEuSx
```

## Result
- **level14 password (token):** `2A31L79asukciNyi8uppkEuSx`
  (verified: it logs straight into `level14`.)
