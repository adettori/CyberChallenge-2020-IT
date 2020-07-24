#!/bin/env python

import random
from functools import reduce
from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes

def s2i(x): #Usato da prepare
  return (ord(x[0])<<8) | ord(x[1]) #Concatena una coppia di byte

def s2i_b(x): #Usato da prepare
  return (x[0]<<8) | x[1] #Concatena una coppia di byte

def i2s(x): #Separa i due byte di sopra
  return [x>>8, x&0xff]

def i2i(x, y):
  z = [(((x&(1<<i))>>i) != ((y&(1<<i))>>i)) for i in range(16)][::-1] #xor
  return reduce(lambda x, y: (x<<1)|y, z) #Apply lambda to z, lambda outputs z concatenated

def find_s0(sn, m, c, n):

    res = sn
    for i in range(n):
        res -= c

        if(res < 0):
            res+=mod

        res = (res*inverse(m, mod)) % mod

    return res

def gen_next(sn, m, c):
    return (sn*m + c) % mod

flag_start = "ccit{f"
flag_start_s2i = [s2i(flag_start[i:i+2]) for i in range(0, len(flag_start), 2)]
content = b""
mod = 0xffff+1

with open("./flag.enc", "rb") as f:
    content = f.read()

s2i_array = []

for i in range(0, len(content), 2):
    s2i_array.append(s2i_b(content[i:i+2]))

#Solve Sn = S0*m^n + c % mod
#Metodo ottenuto risolvendo il sistema val2=val1*m +c  val3=val2*m + c come per definizione di successione
for i in range(len(s2i_array) - 3):

    val1 = i2i(flag_start_s2i[0], s2i_array[i])
    val2 = i2i(flag_start_s2i[1], s2i_array[i+1])
    val3 = i2i(flag_start_s2i[2], s2i_array[i+2])

    diff_2_3 = val2-val3
    if(diff_2_3 < 0):
        diff_2_3 += mod

    diff_1_2 = val1-val2
    if(diff_1_2 < 0):
        diff_1_2 += mod

    m = (diff_2_3 * inverse(diff_1_2, mod)) % mod

    c = val2 - val1*m
    if(c<0):
        c += mod

    s0 = find_s0(val1, m, c, i+1)

    b_array = []

    cur_gen = s0
    for b in s2i_array:
        cur_gen = gen_next(cur_gen, m, c)

        b_array.extend(i2s(i2i(cur_gen, b)))

    string = ""

    try:
        for c in b_array:
            string += chr(c)

        print(string)
    except:
        pass
