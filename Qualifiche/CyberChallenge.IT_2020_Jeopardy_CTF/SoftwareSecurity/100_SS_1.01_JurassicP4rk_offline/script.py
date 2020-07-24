#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template jurassic_p4rk
from pwn import *

exe = context.binary = ELF('jurassic_p4rk')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

io = start()

array = [0x900, 0x3840, 0x2584, 0x24c1, 10000, 0x2649, 0x900, 0x28a4, 0x28a4, 0x27d9, 0]

string  = ""

for i in array:

    string += chr(math.isqrt(i))

io.sendline(string)

io.interactive()

