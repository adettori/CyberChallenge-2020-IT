#!/usr/bin/env python3

import signal
import string
import sys
from Crypto.Random import random
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA
from secret import FLAG

TIMEOUT = 300
BLOCK_SIZE = 16

to_sign = "CyberChallenge2020"
key = DSA.generate(1024)

rng = random.randint(1, key.q-1)
a = 1500450271
b = 2860486313
def next_rng():
    global rng
    rng = (a*rng + b) % key.q
    assert(rng != 0)
    return rng

def menu():
    print()
    print("1. Sign a message")
    print("2. Get the flag")
    print("3. Quit")
    print()
    print("Insert your choice")
    return input("> ")


def sign():
    try:
        msg = input("Give me the message to sign: ")
        assert(all(c in string.printable for c in msg))
        assert(msg != to_sign)
        h = SHA.new(msg.encode()).digest()
        k = next_rng()
        sign = key.sign(h, k)
        print(f"The signature is {sign}")
    except:
        print("Error!")


def verify():
    try:
        print(f"Give me the signature of '{to_sign}': ")
        r = int(input("r: "))
        s = int(input("s: "))
        h = SHA.new(to_sign.encode()).digest()
        return key.verify(h, (r, s))
    except:
        return False


def main():

    print("=================================")
    print("Online One-Time Signature Service")
    print("=================================")
    print()
    print("q =", key.q)
    print()

    for i in range(128):

        if i == 127:
            choice = "2"
        else:
            choice = menu()

        if choice == "1":
            sign()
        elif choice == "2":
            if verify():
                print("Congratulation!")
                print(f"Here's your flag: {FLAG}")
            else:
                print("Error! Wrong signature!!")
                print("Exiting...")
            sys.exit(0)
        elif choice == "3":
            sys.exit(0)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    main()
