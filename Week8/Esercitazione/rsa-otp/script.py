#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from Crypto.Util.number import long_to_bytes

def start(argv=[], *a, **kw):
    return remote("131.114.59.19", 8205, *a, **kw)

enc_flag = b"100466966051500205016976448031575650442163975791047254836866484168453861519484940513687386944283125179729267609186948511826769810155629519560602799877116717513543387887339230054079378896370244533415304024930335671876696309832558828607560330252389403332634139562239223217210881583116143551906989260033635744382"
dec_flag_len = 127 #bit

min_tries = 127
max_tries = 500

def count_zeroes(loop_sz):

    io = start()
    n_tries = 0
    n_zeroes = 0

    for i in range(loop_sz):
        io.recvline()
        io.sendline("1")
        result = io.recvline(False)

        if(int(result) == 1):
            n_zeroes += 1

        n_tries += 1
    return (n_zeroes, n_tries)


for i in range(min_tries, max_tries):

    zero1, tries1 = count_zeroes(i)
    zero2, tries2 = count_zeroes(i)

    if(zero1 == zero2):
        print("Try num:%d,  zeroes:%d" % (i, zero1))


#res = count_zeroes(10000)
#print(res[0]/res[1])

#io = start()
#io.sendline(enc_flag)
#io.interactive()
