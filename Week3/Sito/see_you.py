#!/usr/bin/python3

import string
import base64
from binascii import hexlify
import binascii
import itertools
import sys

#from secret import KEY

'''
La gestione di base64 e' stata un incubo... ricorda che se si confrontano i numeri in base64 un'operazione che per esempio dovrebbe cambiare normalmente, cambia la 4a cifra in base64 dato che ogni valore e' rappresentato con 6 bit.
'''

def decode_base64(string):
    return str(base64.urlsafe_b64decode(string.encode('ascii')), 'ascii')

def encrypt(clear, key):
  enc = []
  for i in range(len(clear)):
    key_c = key[i % len(key)]
    enc_c = chr((ord(clear[i]) + ord(key_c)) % 128)
    enc.append(enc_c)
  return str(base64.urlsafe_b64encode("".join(enc).encode('ascii')), 'ascii')

# NON E' NECESSARIO FARE UNA BASE64 DECODE TRA UN DECRYPT E L'ALTRO
def decrypt(enc, key):
    dec = []
    enc = str(base64.urlsafe_b64decode(enc.encode('ascii')), 'ascii')
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((128 + ord(enc[i]) - ord(key_c)) % 128)
        dec.append(dec_c)
    return "".join(dec)

def check_keys(main_key, plain, cipher):
    
    if(len(main_key) == 4):
        
        dec = decrypt(cipher, main_key)
        sec_key = main_key

        try:
            ret2 = decode_base64(dec).encode()
        except (binascii.Error, UnicodeDecodeError):
            return

        enc = encrypt(plain, sec_key)
        ret1 = decode_base64(enc).encode()

        for j in range(len(sec_key)):

            if(ret2[j] != ret1[j]):
                
                diff = ret2[j] - ret1[j]

                new_char = ord(sec_key[j]) + diff

                if(new_char > 122 or new_char < 97):
                    break

                sec_key = sec_key[0:j] + chr(new_char) + sec_key[j+1:len(sec_key)]
        
                enc = encrypt(plain, sec_key)
                ret1 = decode_base64(enc).encode()

                if(ret2 == ret1):
                    print("CCIT{%s}" % (sec_key + main_key))
                    sys.exit()

    else:
        for i in string.ascii_lowercase:
            tmp_key = main_key + i
            check_keys(tmp_key, plain, cipher)

    
m = "See you later in the city center"
c = "QSldSTQ7HkpIJj9cQBY3VUhbQ01HXD9VRBVYSkE6UWRQS0NHRVE3VUQrTDE="

check_keys("", m, c)

'''
#Bruteforce not possible
def find_key(key1, key2):

    if((len(key1) + len(key2)) == 8):
        original_m = "See you later in the city center"
        original_c = "QSldSTQ7HkpIJj9cQBY3VUhbQ01HXD9VRBVYSkE6UWRQS0NHRVE3VUQrTDE="

        k1 = key1
        k2 = key2

        c1 = decrypt(original_c, k2)
        c1 = str(base64.urlsafe_b64encode("".join(c1).encode('ascii')), 'ascii')
        m = decrypt(c1, k1)

        print(key1 + key2)

        if(m == original_m):
            print("flag: CCIT{%s}" % key)
            return True
    else:
        for char1 in string.ascii_lowercase:
            key1 += char1
            for char2 in string.ascii_lowercase:
                key2 += char2
                ret = find_key(key1, key2)

                if(ret):
                    return True

                key2 = key2[:-1]
            key1 = key1[:-1]

    return False
'''



#assert(len(KEY) == 8)
#assert(all(c in string.ascii_lowercase for c in KEY))

#print("flag: CCIT{%s}" % KEY)

'''
k1 = KEY[0:4]
k2 = KEY[4:8]

d = encrypt(m, k1)
c = encrypt(d, k2)

print("Message:", m)
print("Ciphertext:", c)


m = "See you later in the city center"
c = "QSldSTQ7HkpIJj9cQBY3VUhbQ01HXD9VRBVYSkE6UWRQS0NHRVE3VUQrTDE="
'''

