#!/usr/bin/env python3

import signal
from binascii import hexlify
from string import printable
from random import randint
#from secret import FLAG
from Crypto.Cipher import AES

TIMEOUT = 300
BLOCK = 16

def pad(s):
    #Il padding rimane uguale se la lunghezza di s non cambia, se la s ha len 16 allora il padding sono 16 \x10
    return s + (BLOCK - len(s) % BLOCK) * chr(BLOCK - len(s) % BLOCK)

def randkey(length):
    #Chiave da 16 caratteri "printable" con randint da 0 a 92 inclusi, codificata in utf-8
  return "".join([printable[randint(0, len(printable)-8)] for _ in range(length)]).encode()

def handle():
  print("=====================================")
  print("=     Secure Password Encrypter     =")
  print("=     Now with secure padding!      =")
  print("=====================================")

  cipher = AES.new(randkey(BLOCK), AES.MODE_ECB)

  while True:
    print("")
    try:
      #password = input("Give me the password to encrypt:")
      #password = 'u1n?}\n\n\n\n\n\n\n\n\n\n'
      #password = 'u1n?}\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a'
      password = '0\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
      password = pad(password + str(randkey(31))).encode()
      password = hexlify(cipher.encrypt(password)).decode()
      print("Here is you secure encrypted password:", password)
      password = '0\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a'
      password = password
      print(len(password))
      password = pad(password + str(randkey(31))).encode()
      password = hexlify(cipher.encrypt(password)).decode()
      print("Here is you secure encrypted password:", password)
      break;
    except EOFError:
      break

if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
