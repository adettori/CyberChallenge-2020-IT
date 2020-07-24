#!/usr/bin/env sage-python
# -*- coding: utf-8 -*-
from pwn import *
from binascii import unhexlify, hexlify
from sage.all import *

#https://eprint.iacr.org/2016/475.pdf

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote("131.114.59.19", 8201, *a, **kw)
    else:
        return process("./serverGalois.py", *a, **kw)

def slice_and_pad(b_str, bsize=16):
    b_str += b"\x00" * (len(b_str) % bsize)
    return [bytearray(b_str[k:k+bsize]) for k in range(0, len(b_str), bsize)]

def unhex_blocks(h_str, bsize=16):
    h_str = unhexlify(h_str)
    return slice_and_pad(h_str, bsize)

def xor(a, b):
    assert(len(a) == len(b))
    return bytearray([a[i] ^ b[i] for i in range((len(a)))])

def byte_to_bin(byte):
    b = bin(byte)[2:]
    return "0" * (8 - len(b)) + b

def block_to_bin(block):
    assert(len(block) == 16)
    b = ""
    for byte in block:
        b += byte_to_bin(byte)
    return b

def bytes_to_poly(block, a):
    f = 0
    for e, bit in enumerate(block_to_bin(block)):
        f += int(bit) * a**e
    return f

def poly_to_int(poly):
    a = 0
    for i, bit in enumerate(poly._vector_()):
        a |= int(bit) << (127 - i)
    return a

def poly_to_hex(poly):
    return (hex(poly_to_int(poly))[2:]).upper()

io = start()

io.recvuntil(" ")
enc_flag = io.recvline(False)

msg_1 = "aaaabaaacaaadaaaeaaafaaagaaahaaa"
msg_2 = "iaaajaaakaaalaaamaaanaaaoaaapaaa"

io.sendline("1")
io.sendline(msg_1)

io.recvuntil("('")
enc_msg_1 = io.recvuntil("'", True)
io.recvuntil("'")
tag_msg_1 = io.recvuntil("'", True)

io.sendline("1")
io.sendline(msg_2)

io.recvuntil("('")
enc_msg_2 = io.recvuntil("'", True)
io.recvuntil("'")
tag_msg_2 = io.recvuntil("'", True)


C1 = unhex_blocks(enc_msg_1)

T1 = unhex_blocks(tag_msg_1)

C2 = unhex_blocks(enc_msg_2)

T2 = unhex_blocks(tag_msg_2)

C3 = unhex_blocks(enc_flag)

# Same length for all messages
bit_len_plain = len(C1) // 2 * 8
bit_len_plain_str = hex(bit_len_plain)[2:]

bit_len_plain_str = bit_len_plain_str.rjust(16, "0")

L = unhex_blocks(bit_len_plain_str)


T = xor(T1[0], T2[0])
C = [
    xor(C1[0], C2[0]),
    xor(C1[1], C2[1])
]

# Sage magic

F, a = GF(2**128, name="a").objgen()
R, X = PolynomialRing(F, name="X").objgen()

C1_p = [
    bytes_to_poly(C1[0], a),
    bytes_to_poly(C1[1], a)
]
T1_p = bytes_to_poly(T1[0], a)

C2_p = [
    bytes_to_poly(C2[0], a),
    bytes_to_poly(C2[1], a)
]
T2_p = bytes_to_poly(T2[0], a)

C3_p = [
    bytes_to_poly(C3[0], a),
    bytes_to_poly(C3[1], a)
]

C_p = [
    bytes_to_poly(C[0], a),
    bytes_to_poly(C[1], a)
]
T_p = bytes_to_poly(T, a)

L_p = bytes_to_poly(L[0], a)


f1 = C1_p[0] * X**3 + C1_p[1] * X**2 + L_p * X
f1_t = C1_p[0] * X**3 + C1_p[1] * X**2 + L_p * X + T1_p
f2 = C2_p[0] * X**3 + C2_p[1] * X**2 + L_p * X
f2_t = C2_p[0] * X**3 + C2_p[1] * X**2 + L_p * X + T2_p
f3 = C3_p[0] * X**3 + C3_p[1] * X**2 + L_p * X
p = C_p[0] * X**3 + C_p[1] * X**2 + T_p

for root, _ in p.roots():
    EJ = f1_t(root)
    tag_pol = f3(root) + EJ
    tag_val = poly_to_hex(tag_pol)

    io.sendline("2")
    io.sendline(enc_flag)
    io.sendline(tag_val)

io.interactive()
'''
block_size = 128 #bit
finite_field = 2**block_size
F, a = GF(2**128, name="a").objgen()
R, X = PolynomialRing(F, name="X").gen()

def len_gcm(int_value):
    bin_value = bin(int_value)[2:]
    bit_len = len(bin_value)

    return bit_len

def build_tag_pol_wo_S(enc_value, x=None):


    pos = 0
    bin_flag = bin(enc_value)[2:]
    ciphertext_array = []

    for i in range(math.ceil(len(bin_flag)/block_size)):
        ciphertext_array.append(str(bin_flag[block_size*i:block_size*(i+1)]))

    pol = len_gcm(enc_value)*x

    exp = len(ciphertext_array)+1

    for i in ciphertext_array:

        pol += int(i, 2)*(x**exp)
        exp -= 1

    #missing the S term

    return pol

io = start()

io.recvuntil(" ")
enc_flag = int(io.recvline(False), 16)

msg_1 = "1"*32
msg_2 = "2"*32

io.sendline("1")
io.sendline(msg_1)

io.recvuntil("('")
enc_msg_1 = int(io.recvuntil("'", True), 16)
io.recvuntil("'")
tag_msg_1 = int(io.recvuntil("'", True), 16)

io.sendline("1")
io.sendline(msg_2)

io.recvuntil("('")
enc_msg_2 = int(io.recvuntil("'", True), 16)
io.recvuntil("'")
tag_msg_2 = int(io.recvuntil("'", True), 16)

coeff_2 = enc_msg_1^enc_msg_2
coeff_1 = len_gcm(enc_msg_1)
res_pol2 = enc_msg_2*xvar**2 + len_gcm(enc_msg_2)*xvar
sum_tag = tag_msg_1 ^ tag_msg_2
res = res_pol1+res_pol2+sum_tag
roots_pol = solve(res, xvar)

S = tag_msg_1 + enc_msg_1*(roots_pol[0]**2) + len_gcm(enc_msg_2)*roots_pol[0]

test = enc_msg_2*(roots_pol[0]**2) + len_gcm(enc_msg_2)*roots_pol[0] + S
print(test)

#Find S term
sum_tag_pol = build_tag_pol_wo_S(enc_msg_1) + build_tag_pol_wo_S(enc_msg_2)
sum_tag = tag_msg_1 ^ tag_msg_2 #Among the roots of this pol is H

res_pol = sum_tag_pol + sum_tag
roots_pol = res_pol.roots()
print(roots_pol)

S = tag_msg_1 + build_tag_pol_wo_S(enc_msg_1, roots_pol[0][0])

#Cerchiamo di calcolare tag_msg_2
res = build_tag_pol_wo_S(enc_msg_2, roots_pol[0][0]) + S
print(res)
'''
