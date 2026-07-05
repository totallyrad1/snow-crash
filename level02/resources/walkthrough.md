# level02

## Goal
Find `flag02`'s password from the network capture in the home directory.

## Recon
```sh
$ ls -l ~
----r--r-- 1 flag02 level02 8302 Aug 30  2015 level02.pcap
```

`level02.pcap` is a tcpdump capture, readable by us but owned by `flag02`. Copy it
off the box for analysis (do **not** commit the pcap: it is an ISO-provided binary):

```sh
$ scp -P 4242 level02@<VM>:~/level02.pcap .
```

## Analysis
There is a single TCP conversation - a **telnet** login (server port 12121):

```sh
$ tshark -r level02.pcap -q -z conv,tcp
59.233.235.218:39247 <-> 59.233.235.223:12121   ...
$ tshark -r level02.pcap -q -z follow,tcp,ascii,0
... wwwbugs login: level... Password: ...
```

The interesting bytes are what the **client typed** (client -> server). Extract those
payloads and reconstruct the keystrokes. Telnet echoes each character, and the typist
made mistakes and used the **delete key (0x7f)**, so a naive `strings` gives the wrong
answer - you must replay the backspaces:

```sh
$ tshark -r level02.pcap -Y 'tcp.srcport==39247 && tcp.len>0' \
         -T fields -e tcp.payload > c2s.hex
$ ./reconstruct.py c2s.hex
password: ft_waNDReL0L
```

The raw typed stream at the password prompt was:

```
ft_wandr <DEL><DEL><DEL> NDRel <DEL> L0L <CR>
ft_wandr -> ft_wand -> ft_wan -> ft_wa -> ft_waNDRel -> ft_waNDRe -> ft_waNDReL0L
```

## Getflag
```sh
$ ssh flag02@<VM> -p 4242       # password: ft_waNDReL0L
flag02@SnowCrash$ getflag
Check flag.Here is your token : kooda2puivaav1idi4f57q8iq
```

## Result
- **flag02 password:** `ft_waNDReL0L`
- **level03 password (token):** `kooda2puivaav1idi4f57q8iq`
