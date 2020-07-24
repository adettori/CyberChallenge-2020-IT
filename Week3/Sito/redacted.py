#!/usr/bin/env python

from Crypto.Cipher import AES, XOR
import binascii, sys
from string import printable

'''
KEY = "yn9RB3Lr43xJK2██".encode() # len = 16, mancano 2 char
IV  = "████████████████".encode() # len = 16
msg = "AES with CBC is very unbreakable".encode() # len = 32 AES with CBC is |very unbreakable

aes = AES.new(KEY, AES.MODE_CBC, IV)
print(binascii.hexlify(aes.encrypt(msg)).decode())

# output:
# c5██████████████████████████d49e78c670cb67a9e5773d696dc96b78c4e0 # len = 64 
# 2nd block = 78c670cb67a9e5773d696dc96b78c4e0
'''

# Dato che l'ultimo blocco cifrato non e' affetto dall'avere IV corretto in CBC, troviamo le ultime due cifre della chiave

cur_key = "yn9RB3Lr43xJK2"
cur_iv = "0123456789123456"
cipher_text = "c511111111111111111111111111d49e78c670cb67a9e5773d696dc96b78c4e0"
first_block = "c511111111111111111111111111d49e"
second_block = "78c670cb67a9e5773d696dc96b78c4e0"
msg = "AES with CBC is very unbreakable".encode()

'''
for i in range(93):
    for j in range(93):
        tmp_key = cur_key + printable[i] + printable[j]
        tmp_aes = AES.new(tmp_key, AES.MODE_CBC, cur_iv)
        res1 = tmp_aes.decrypt(binascii.unhexlify(cipher_text.encode()))

        xor = XOR.new(binascii.unhexlify("d49e")) # Unica parte conosciuta di first_block
        res2 = xor.decrypt(res1)

        if(res1[30:32] == msg[30:32]):
                xor = XOR.new(binascii.unhexlify("c5")) # Unica parte conosciuta di first_block
                res2 = xor.decrypt(res1)
                if(res1[16:17] == msg[16:17]):
                    print(tmp_key) # result = yn9RB3Lr43xJK2tp
'''
'''
# troviamo il primo blocco di ciphertext
cur_key = "yn9RB3Lr43xJK2tp"
cur_iv = "0123456789123456"
cipher_text = "c511111111111111111111111111d49e78c670cb67a9e5773d696dc96b78c4e0"
first_block = "c511111111111111111111111111d49e"
second_block = "78c670cb67a9e5773d696dc96b78c4e0"
msg = "AES with CBC is very unbreakable".encode()

aes = AES.new(cur_key, AES.MODE_ECB) # Necessario decriptare il secondo blocco con ECB dato che abbiamo la chiave e non IV
res1 = aes.decrypt(binascii.unhexlify(cipher_text.encode()))

dec_second_block = res1[16:32]  # plain_second_block = cipher_first_block xor post_aes_cipher_second_block, quindi...

xor = XOR.new(dec_second_block)
res2 = xor.decrypt(msg[16:32])
print(binascii.hexlify(res2)) # result = c5dc598a00e6e31272bcb2ed502ad49e first_cipher_block
'''

# decriptiamo il primo cipher_block
cur_key = "yn9RB3Lr43xJK2tp"
cur_iv = "0123456789123456"
cipher_text = "c5dc598a00e6e31272bcb2ed502ad49e78c670cb67a9e5773d696dc96b78c4e0"

aes = AES.new(cur_key, AES.MODE_ECB)
res1 = aes.decrypt(binascii.unhexlify(cipher_text.encode()))

dec_first_block = res1[0:16]
xor = XOR.new(dec_first_block)
flag_content = xor.decrypt(msg[0:16])
print((flag_content))
