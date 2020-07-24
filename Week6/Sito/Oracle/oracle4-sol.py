#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import sys
from Crypto.Util.number import *
#inverse and long_to_bytes

def start(argv=[], *a, **kw):
    return remote("149.202.200.158", 7014, *a, **kw)

e = 65537 #generate() default value
prime = 2

io = start()

io.recvuntil("Encrypted flag: ")
enc_flag = int(io.recvuntil("\n", True))

io.recvuntil(">")
io.sendline("2")
io.sendline(str(-enc_flag))
io.recvuntil("Decrypted: ")
neg_flag = int(io.recvuntil("\n", True))

io.recvuntil(">")
io.sendline("2")
io.sendline(str(-neg_flag))
io.recvuntil("Decrypted: ")
neg_flag2 = int(io.recvuntil("\n", True))

io.recvuntil(">")
io.sendline("1")
io.sendline(str(neg_flag2))
io.recvuntil("Encrypted: ")
flag = int(io.recvuntil("\n", True))

print(long_to_bytes(flag).decode())
