#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
from string import printable

# Set up pwntools for the correct architecture
context.update(arch='amd64')
exe = '/bin/nc'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start(["149.202.200.158", "7001"])

string = "CCIT{s1d3_ch4nn3"
cur_cycles = 0
cur_char = ""

for j in range(16):
    for i in printable[0:93]:
        tmp_str = string + i
        io.recvuntil("Give me the password to check:")
        io.sendline(tmp_str)
        io.recvuntil("Wrong password, checked in ")
        tmp_cycles = int(io.recvuntil(" ", drop=True))

        if(tmp_cycles > cur_cycles):
            cur_cycles = tmp_cycles
            cur_char = i

    string += cur_char
    cur_cycles = 0
    cur_char = ""
    print(string)

io.interactive()

