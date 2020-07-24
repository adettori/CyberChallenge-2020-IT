#!/usr/bin/env python
import socketserver
from Crypto.Cipher import AES
import os
import random

FLAG = b"CCIT{aaaabaaacaaadaaaeaaafaaaga}" #32 bytes

def xor(x, y):
    return bytes([x[idx] ^ y[idx] for idx in range(len(x))])


#32 bit in 16 byte
def random_bytes():
    a= random.getrandbits(32).to_bytes(16, 'little')
    return a

#Cripta random_bytes e usa ciphered come xor per ogni blocco
def encrypt(aes, msg):
    blocks = [msg[idx:idx+16] for idx in range(0, len(msg), 16)]
    cipher = b''
    for block in blocks:
        block += bytes([0 for _ in range(16 - len(block))]) #Padding di 0
        cipher += xor(aes.encrypt(random_bytes()), block)
    return cipher


def send_enc(req, aes, msg):
    req.sendall(encrypt(aes, msg))


def recv_exact(req, length):
    buf = b''
    while length > 0:
        data = req.recv(length)
        if data == b'':
            raise EOFError()
        buf += data
        length -= len(data)
    return buf


#Msg da 32 byte
def recv_msg(req):
    return recv_exact(req, 32)


#Seed da 16 byte
def recv_seed(req):
    try:
        data = int(recv_exact(req, 16))
        print(data)
    except ValueError as e:
        req.sendall('Not a valid int\n')
        raise(e)
    return data


def main(req):
    try:
        req.sendall(b'Send me a random seed\n')
        #Seed usato non per la chiave aes ma come plaintext da crittare e poi xorare
        random.seed(recv_seed(req))
        #Chiave prodotta da random di sistema
        aes = AES.new(os.urandom(16), AES.MODE_ECB)

        req.sendall(b'Encrypted flag:\n')
        #100 tentativi
        for _ in range(100):
            send_enc(req, aes, b'Encrypted Flag: ' + FLAG) #Messaggio iniziale da 16 byte
            req.sendall(b'\n')

        req.sendall(b'Okay bye\n')
        return
    except Exception as e:
        pass


class TaskHandler(socketserver.BaseRequestHandler):
    def handle(self):
        main(self.request)


if __name__ == '__main__':
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 1337), TaskHandler)
    server.serve_forever()
