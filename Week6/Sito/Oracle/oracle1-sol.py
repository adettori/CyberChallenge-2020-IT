#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
from Crypto.Util.number import *
#inverse and long_to_bytes

def start(argv=[], *a, **kw):
    return remote("149.202.200.158", 7011, *a, **kw)

e = 65537 #generate() default value

io = start()

io.recvuntil("Encrypted flag: ")
enc_flag = io.recvuntil("\n", True)
io.recvuntil(">")

enc_hidden_flag = int(enc_flag) * (2**e)

io.sendline("2")
io.sendline(str(enc_hidden_flag))
io.recvuntil("Decrypted: ")

dec_hidden_flag = io.recvuntil("\n", True)

true_flag = int(dec_hidden_flag)//2
print(long_to_bytes(true_flag).decode())

io.interactive()
