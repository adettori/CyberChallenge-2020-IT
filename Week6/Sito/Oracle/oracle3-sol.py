#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
from Crypto.Util.number import *
#inverse and long_to_bytes

def start(argv=[], *a, **kw):
    return remote("149.202.200.158", 7013, *a, **kw)

def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]

#Idea: p t.c. p|c
#(c/p)^d mod n = m/(p^d) mod n
#calcolo p^d
#(m/p^d)*p^d = m
#Decritto ed encritto per ottenere m modulo n
#Usa quattro richieste al server

e = 65537 #generate() default value
primes_list = primes(100000)

io = start()

io.recvuntil("Encrypted flag: ")
enc_flag = int(io.recvuntil("\n", True))

#find enc_flag factor
factor = 0
for i in primes_list:
    res = enc_flag // i

    if(res*i == enc_flag):
        factor = i
        break

io.recvuntil(">")
io.sendline("2")
enc_flag_div_fact = enc_flag // factor
io.sendline(str(enc_flag_div_fact))
io.recvuntil("Decrypted: ")
dec_flag_1 = int(io.recvuntil("\n", True))

io.recvuntil(">")
io.sendline("2")
io.sendline(str(factor))
io.recvuntil("Decrypted: ")
dec_factor_1 = int(io.recvuntil("\n", True))

product_dec_factor_flag = dec_factor_1 * dec_flag_1

io.recvuntil(">")
io.sendline("2")
io.sendline(str(product_dec_factor_flag))
io.recvuntil("Decrypted: ")
dec_flag2 = int(io.recvuntil("\n", True))

io.recvuntil(">")
io.sendline("1")
io.sendline(str(dec_flag2))
io.recvuntil("Encrypted: ")
flag = int(io.recvuntil("\n", True))

bytes_flag = long_to_bytes(flag)
print(bytes_flag.decode())

