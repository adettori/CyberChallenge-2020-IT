#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
from string import printable
import sys

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

def start(argv=[], *a, **kw):
    return remote("131.114.59.19", 8203, *a, **kw)

block_size = 16

def encrypt(plaintext):

    io.recvuntil("Input a string to encrypt (input 'q' to quit):\n")
    io.sendline(plaintext)
    io.recvline()
    enc = io.recvline(False)

    return enc

def bruteforce_char(cur_enc_set, known_str, pad_len): #know_str includes initial push_padding

    initial_block_set = set()

    for e in cur_enc_set:
        initial_block = e[32:64]
        initial_block_set.add(initial_block)

    for i in printable:

        enc_block_set = set()

        tmp_str = printable[0:pad_len] + known_str + i

        while(len(enc_block_set) != 2):

            tmp_enc = encrypt(tmp_str)
            cur_block= tmp_enc[32:64]

            enc_block_set.add(cur_block)

        if(enc_block_set <= initial_block_set):
            new_str = known_str + i
            print(new_str)
            return new_str

    return None

# Con input di len 3 e bit casuale a 1 viene aggiunto un blocco all'output => len flag = 48-3-1-15 = 29
flag_len = 29

io = start()

cur_flag = ""

for i in range(flag_len):

    cur_padding = printable[0:2*block_size - (i+1)]

    enc_set = set()

    while(len(enc_set) != 2):

        cur_enc = encrypt(cur_padding)
        enc_set.add(cur_enc)

    ret = bruteforce_char(enc_set, cur_flag, 2*block_size - (i+1))

    if(ret == None):
        print("ERROR")
        sys.exit(1)

    cur_flag = ret

