#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import random
import os

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote("131.114.59.19", 8202, *a, **kw)
    else:
        return remote("127.0.0.1", 1337, *a, **kw)

def random_bytes():
    a= random.getrandbits(32).to_bytes(16, 'little')
    return a

def xor(x, y):
    return bytes([x[idx] ^ y[idx] for idx in range(len(x))])

def get_seed_xors(seed):
    io = start()

    io.recvline()
    io.sendline(str(seed))
    io.recvline() #Enc flag msg

    result = io.recvuntil("Okay bye\n", True)
    return result

block_size = 16

lower_limit = 10**15
upper_limit = 10**16-1
target_seed = -2

#Find vulnerable seed
while(target_seed == -1):
    seed_generator_seed = randint(lower_limit, upper_limit)
    random.seed(seed_generator_seed)

    seed_list = []

    for i in range(100):
        seed = random.getrandbits(32)

        if(seed in seed_list):
            target_seed = seed_generator_seed
            first_ind = seed_list.index(seed)
            second_ind = i
            print(first_ind)
            print(second_ind)
            print(target_seed)
            break

        seed_list.append(seed)

#seed list
# 9184740450027379 23 38
# 1537531411175743 3 34
# 9720430145908886 1 82
# 7056140672287178 26 90
# 5881151240618954 11 45
# 8576351639896358 34 40
# 9141080339348480 14 28
# 9483294129879740 10 83
# 3760393125937358 4 26
# 2374514217101539 7 77
seed_list = [9184740450027379, 1537531411175743, 9720430145908886, 7056140672287178, 5881151240618954,
             8576351639896358, 9141080339348480, 9483294129879740, 3760393125937358, 2374514217101539]
first_pos =  [23,    3,  1, 26, 11, 34, 14, 10, 4,  7]
second_pos = [38,   34, 82, 90, 45, 40, 28, 83, 26, 77]

#Idea: trova dei seed le cui posizioni in modulo ip_len siano diverse, conosci il primo blocco fai xor...
ip_len = 3 #Ipotesi sulla lunghezza della flag in blocchi, ottenuta osservano lo stream
target_ind = 1

rec = get_seed_xors(seed_list[target_ind])
enc_blocks = b"".join([rec[idx:idx+48] for idx in range(0, len(rec), 49)])

result_blocks = [enc_blocks[idx:idx+16] for idx in range(0, len(enc_blocks), 16)]

msg1_xor_enc = result_blocks[first_pos[target_ind]]
msg2_xor_enc = result_blocks[second_pos[target_ind]]

xor_seed_blocks = xor(msg1_xor_enc, msg2_xor_enc)

first_block = b'Encrypted Flag: ' #16 chars
second_block = xor(first_block, xor_seed_blocks)

target_ind = 3

rec = get_seed_xors(seed_list[target_ind])
enc_blocks = b"".join([rec[idx:idx+48] for idx in range(0, len(rec), 49)])

result_blocks = [enc_blocks[idx:idx+16] for idx in range(0, len(enc_blocks), 16)]

msg1_xor_enc = result_blocks[first_pos[target_ind]]
msg2_xor_enc = result_blocks[second_pos[target_ind]]

xor_seed_blocks = xor(msg1_xor_enc, msg2_xor_enc)

third_block = xor(first_block, xor_seed_blocks)

print(second_block + third_block)
