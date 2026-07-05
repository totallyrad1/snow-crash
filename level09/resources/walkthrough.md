# level09

## Goal
Decode the `~/token` file to get `flag09`'s password, then run getflag.

## Recon
```sh
$ ls -l ~
-rwsr-sr-x 1 flag09 level09 7640 Mar  5  2016 level09
----r--r-- 1 flag09 level09   26 Mar  5  2016 token       # readable by us
$ xxd ~/token
0000000: 6634 6b6d 6d36 707c 3d82 7f70 826e 8382  f4kmm6p|=..p.n..
0000010: 4442 8344 757b 7f8c 890a                 DB.Du{....
```

The `level09` binary encodes a string by **adding each byte's index** to it:
`out[i] = in[i] + i`. You can confirm this by feeding it known input, e.g.
`~/level09 AAAAA` prints `ABCDE`. The token file is the *encoded* password.

## Exploit - reverse the encoding
Subtract the index from every byte: `in[i] = out[i] - i`.

```sh
$ ./decode.py ~/token
f3iji1ju5yuevaus41q1afiuq
```

Worked example for the first bytes: `0x66-0='f'`, `0x34-1='3'`, `0x6b-2='i'`,
`0x6d-3='j'`, `0x6d-4='i'`, `0x36-5='1'` ...

That is **flag09's password**:

```sh
$ ssh flag09@<VM> -p 4242        # password: f3iji1ju5yuevaus41q1afiuq
flag09@SnowCrash$ getflag
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```

## Result
- **flag09 password:** `f3iji1ju5yuevaus41q1afiuq`
- **level10 password (token):** `s5cAJpM8ev6XHw998pRWG728z`

This completes the mandatory part (level00 - level09).
