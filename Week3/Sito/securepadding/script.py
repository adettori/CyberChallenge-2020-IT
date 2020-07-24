#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /usr/bin/netcat
from pwn import *
from binascii import unhexlify
from string import printable

# Set up pwntools for the correct architecture
exe = context.binary = ELF('/usr/bin/netcat')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

original_flag_len = 31
block_size = 16
alphabet_size = 93

io = start(["149.202.200.158", "7000"])

decrypted_flag = "CCIT{r3m3mb3r_th"
flag_len = len(decrypted_flag)

def brute_force_cur_char(byte_array, cur_flag, cur_len_tmp, start_block, end_block):

    for j in range(alphabet_size):
        line = printable[0:cur_len_tmp] + cur_flag + printable[j]

        io.recvuntil("Give me the password to encrypt:")
        
        encoded_str = line.encode()

        io.sendline(encoded_str)

        io.recvuntil("Here is you secure encrypted password: ")
        enc_password2 = io.recvline(keepends=False)
        cur_first_block = enc_password2[start_block:end_block]

        #print(str(cur_len_tmp) + "-" + str(j) + ":" + cur_flag)
        #print(encoded_str)
        #print(enc_password1)
        #print(enc_password2)
        #print(byte_array)
        #print(cur_first_block)

        if(cur_first_block == byte_array):
            return ord(printable[j])

    return -1

# I primi 16 byte, result = CCIT{r3m3mb3r_th
for i in range(16):
    if(flag_len >= 16):
        break

    io.recvuntil("Give me the password to encrypt:")
    io.sendline(printable[0:15-i])
    io.recvuntil("Here is you secure encrypted password: ")
    enc_password1 = io.recvline(keepends=False)
    password_len = len(enc_password1)
    cur_flag_block = enc_password1[0:2*block_size]

    ret = brute_force_cur_char(cur_flag_block, decrypted_flag, 15-i, 0, 2*block_size)

    if(ret >= 0):
        decrypted_flag = decrypted_flag + chr(ret)
        flag_len = len(decrypted_flag)
        print(decrypted_flag)
    elif(ret == -1):
        break

# Seconda parte recupera dalla "parte centrale" del cipher text
for i in range(15):
    io.recvuntil("Give me the password to encrypt:")
    io.sendline(printable[0:15-i])
    io.recvuntil("Here is you secure encrypted password: ")
    enc_password1 = io.recvline(keepends=False)
    password_len = len(enc_password1)
    cur_flag_block = enc_password1[32:32+2*block_size]

    for j in range(alphabet_size):
        line = printable[0:15-i] + decrypted_flag[flag_len-16-i:flag_len] + printable[j]

        io.recvuntil("Give me the password to encrypt:")
        
        encoded_str = line.encode()

        io.sendline(encoded_str)

        io.recvuntil("Here is you secure encrypted password: ")
        enc_password2 = io.recvline(keepends=False)
        cur_first_block = enc_password2[32:32+2*block_size]

        print(str(i-15) + "-" + str(j) + ":" + decrypted_flag)
        #print(encoded_str)
        print(enc_password1)
        print(enc_password2)
        print(cur_flag_block)
        print(cur_first_block)

        if(cur_first_block == cur_flag_block):
            decrypted_flag = decrypted_flag + printable[j]
            flag_len = len(decrypted_flag)
            print(decrypted_flag)

'''
OLD VERSION
def brute_force_cur_char(byte_array, cur_flag, cur_len_flag):

    for j in range(alphabet_size):
        padding_len = (block_size - (cur_len_flag+2 + original_flag_len) % block_size)
        padding_char = chr(block_size - (cur_len_flag+2 + original_flag_len) % block_size)
        line = printable[j] + cur_flag + padding_len * padding_char

        io.recvuntil("Give me the password to encrypt:")
        
        encoded_str = line.encode()

        io.sendline(encoded_str)

        io.recvuntil("Here is you secure encrypted password: ")
        enc_password2 = io.recvline(keepends=False)
        cur_first_block = enc_password2[0:2*block_size]

        print(str(cur_len_flag) + "-" + str(j) + ":" + cur_flag)
        print(encoded_str)
        print(enc_password1)
        print(enc_password2)
        print(byte_array)
        print(cur_first_block)

        if(padding_char == '\n'):
            break;

        if(cur_first_block == byte_array):
            return ord(printable[j])

    return -1

def brute_force_prec_char(byte_array, cur_flag, cur_len_flag):

    print("BRUTEFORCE PREC ENGAGED")
    for k in range(alphabet_size):
        tmp_flag = cur_flag
        tmp_flag = printable[k] + tmp_flag

        ret = brute_force_cur_char(byte_array, tmp_flag, cur_len_flag)

        if(ret >= 0):
            print("BRUTEFORCED: " + chr(ret) + printable[k])
            return ret
    return -2

io = start(["149.202.200.158", "7000"])

decrypted_flag = "u1n?}"
flag_len = len(decrypted_flag)
brute_force_prec = False

for i in range(flag_len,31):
    io.recvuntil("Give me the password to encrypt:")
    io.sendline(printable[0:i+2])
    io.recvuntil("Here is you secure encrypted password: ")
    enc_password1 = io.recvline(keepends=False)
    password_len = len(enc_password1)
    cur_last_block = enc_password1[password_len-2*block_size:password_len]

    ret = 0
    if(brute_force_prec == False):
        ret = brute_force_cur_char(cur_last_block, decrypted_flag, i)
    else:
        ret = brute_force_prec_char(cur_last_block, decrypted_flag, i)
        brute_force_prec = False

    if(ret >= 0):
        decrypted_flag = chr(ret) + decrypted_flag
        flag_len = len(decrypted_flag)
        print(decrypted_flag)
    elif(ret == -1):
        brute_force_prec = True
    elif(ret == -2):
        print("BRUTEFORCE FAILED")
        break
'''
