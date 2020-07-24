#!/usr/bin/env python

from Crypto.Util.number import *

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

n=561985565696052620466091856149686893774419565625295691069663316673425409620917583731032457879432617979438142137
e=65537
c=328055279212128616898203809983039708787490384650725890748576927208883055381430000756624369636820903704775835777

p = 29
q = 19378812610208711050554891591368513578428260883630885898953907471497427917962675301070084754463193723428901453

tot = (p-1)*(q-1)

d = modinv(e, tot)
print(long_to_bytes(pow(c, d, n)).decode())
