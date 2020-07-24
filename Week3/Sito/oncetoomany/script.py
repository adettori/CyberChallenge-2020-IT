#!/bin/python3

from copy import copy
from string import printable
from binascii import unhexlify, hexlify

def xor_strings(str1, str2):
    byte1 = bytearray.fromhex(str1.strip())
    byte2 = bytearray.fromhex(str2.strip())
    min_len = min(len(byte1), len(byte2))
    result = bytearray(min_len)

    for i in range(min_len):
        result[i] = byte1[i] ^ byte2[i]

    return result

def str_bits(string, start):
    return start.join('{0:08b}'.format(ord(x), '8b') for x in string.strip())

def int_bits(string, start):
    return start.join('{0:08b}'.format(x, '8b') for x in string.strip())

message_file = open("./message.enc", "r")
messages = message_file.readlines()

'''
print("First 8 bytes of every message")
for i in messages:
    print(int_bits(unhexlify(i[0:16]), " "))

for i in range(len(messages)):
    for j in range(len(messages)):
        if(i == j):
            continue

        result = xor_strings(messages[i], messages[j])

        print(str(i) + ":" + str(j) + " " + int_bits(result[0:8], " "))

'''

def check_xor(start_key):

    candidate_keys = []
    for m in messages:

        cur_message = m.strip()
    
        for i in range(len(cur_message) - len(start_key)):

            if(i % 2 == 1):
                continue

            tmp_key = hexlify(bytearray(start_key, "utf-8")).decode()
            tmp_msg = cur_message[i:len(cur_message)]
            res = xor_strings(tmp_msg, tmp_key)

            candidate_keys.append([res, i])

    return candidate_keys

start_msg = "CCIT{"
keys_index = check_xor(start_msg)

def find_key(main_key, max_key_len, index):
    if(len(main_key) == max_key_len):
        
        decrypted_strings = []
        matching_keys = []

        for m in messages:
        
            cur_index = index

            tmp_key = hexlify(main_key).decode()
            tmp_msg = m[cur_index:len(m)].strip()
            
            res = xor_strings(tmp_msg, tmp_key)

            if(res == b""):
                return

            for c in res:
               if((not chr(c) in printable)):
                  return

            decrypted_strings.append(res)
            matching_keys.append(main_key)

        for i in range(len(decrypted_strings)):
            print(decrypted_strings[i], end="\t")
            print(matching_keys[i], end="\t")
            print(cur_index)

    else:
        for i in range(0xff):
            tmp_key = copy(main_key)
            tmp_key.append(i)
            find_key(tmp_key, max_key_len, index)

candidate_key = bytearray(b"\xef\x00A|\x1d\x01\x1a\x81`S\x14w\xaa\x89V\xdc\x17\xb5,3?\x83\x8en")
find_key(candidate_key, len(candidate_key)+1, 82)

'''
#Bootstrap, una volta ottenute le prime parole ho continuato a mano con grep, l'inglese torna sempre utile
for k in keys_index:
    find_key(k[0], k[1])
'''
