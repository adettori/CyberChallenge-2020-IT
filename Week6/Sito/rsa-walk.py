#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
        return remote("149.202.200.158", 7010, *a, **kw)

# Iterative Algorithm (xgcd)
def iterative_egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q,r = b//a,b%a; m,n = x-u*q,y-v*q # use x//y for floor "floor division"
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def modinv(a, m):
    g, x, y = iterative_egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

io = start()

io.recvuntil("p = ")
p = int(io.recvuntil("\n", True))
io.recvuntil("q = ")
q = int(io.recvuntil("\n", True))

n = (p)*(q)

io.recvuntil("?")

io.sendline(str(n))

io.recvuntil("?")

string = "This is the plaintext"
new_str = ""
for i in string:
    new_str += hex(ord(i)).split("x")[1]

io.sendline(str(int(new_str, 16)))

io.recvuntil("p = ")
p = int(io.recvuntil("\n", True))
io.recvuntil("q = ")
q = int(io.recvuntil("\n", True))
io.recvuntil("m = ")
m = int(io.recvuntil("\n", True))
io.recvuntil("e = ")
e = int(io.recvuntil("\n", True))

io.recvuntil("?")

n = p*q

res = pow(m, e, n)

io.sendline(str(res))

io.recvuntil("p = ")
p = int(io.recvuntil("\n", True))
io.recvuntil("q = ")
q = int(io.recvuntil("\n", True))
io.recvuntil("e = ")
e = int(io.recvuntil("\n", True))

tot = (p-1)*(q-1)

io.recvuntil("?")
io.sendline(str(tot))

io.recvuntil("?")

io.sendline(str(modinv(e,tot)))

io.recvuntil("p = ")
p = int(io.recvuntil("\n", True))
io.recvuntil("q = ")
q = int(io.recvuntil("\n", True))
io.recvuntil("e = ")
e = int(io.recvuntil("\n", True))
io.recvuntil("c = ")
c = int(io.recvuntil("\n", True))

tot = (p-1)*(q-1)
n = p*q
d = modinv(e,tot)

res = pow(c, d, n)

io.sendline(str(res))


io.interactive()

