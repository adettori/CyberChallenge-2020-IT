#!/usr/bin/env python3

import signal
import os
import json
import string
import sys
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from secret import FLAG

TIMEOUT = 300
BLOCK_SIZE = 16


def pad(s): return s + (BLOCK_SIZE - len(s) %
                        BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s): return s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self):
        self.key = os.urandom(BLOCK_SIZE)

    def encrypt(self, raw):
        raw = pad(raw).encode()
        cipher = AES.new(self.key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode()


cipher = AESCipher()

def menu():
    print()
    print("1. Sign-up")
    print("2. Log-in")
    print("3. Quit")
    print()
    print("Insert your choice")
    return input("> ")

def signup():
    name = input("name: ")
    assert(all(c in string.printable for c in name))

    surname = input("surname: ")
    assert(all(c in string.printable for c in surname))

    email = input("email: ")
    assert(all(c in string.printable for c in email))

    data = '{"name": "%s", "surname": "%s", "email": "%s", "type": "user"}' % (name, surname, email)

    try :
        data = json.dumps(json.loads(data))
        print("Here's your login token:")
        print(cipher.encrypt(data))
    except:
        print("There is some error with your registration!")
        print("Try again...")

def login():
    token = input("login token: ")

    try:
        data = cipher.decrypt(token)
        data = json.loads(data)

        assert("name" in data)
        assert("surname" in data)
        assert("email" in data)
        assert("type" in data)

        if data["type"] == "admin":
            print("Welcome back admin!")
            print("Here is your flag:", FLAG)
        else:
            print("Hello user", data["name"], data["surname"])

    except:
        print("Error!")
        print("Invalid token!")


def main():
    print("   _____       _               _____ _           _ _                          ")
    print("  /  __ \     | |             /  __ \ |         | | |                         ")
    print("  | /  \/_   _| |__   ___ _ __| /  \/ |__   __ _| | | ___ _ __   __ _  ___    ")
    print("  | |   | | | | '_ \ / _ \ '__| |   | '_ \ / _` | | |/ _ \ '_ \ / _` |/ _ \   ")
    print("  | \__/\ |_| | |_) |  __/ |  | \__/\ | | | (_| | | |  __/ | | | (_| |  __/   ")
    print("   \____/\__, |_.__/ \___|_|   \____/_| |_|\__,_|_|_|\___|_| |_|\__, |\___|   ")
    print("          __/ |                                                  __/ |        ")
    print("         |___/                                                  |___/         ")
    print("    ___      _           _        ______                _                     ")
    print("   / _ \    | |         (_)       | ___ \              | |                    ")
    print("  / /_\ \ __| |_ __ ___  _ _ __   | |_/ /_ _ _ __   ___| |                    ")
    print("  |  _  |/ _` | '_ ` _ \| | '_ \  |  __/ _` | '_ \ / _ \ |                    ")
    print("  | | | | (_| | | | | | | | | | | | | | (_| | | | |  __/ |                    ")
    print("  \_| |_/\__,_|_| |_| |_|_|_| |_| \_|  \__,_|_| |_|\___|_|                    ")
    print()

    while True:
        choice = menu()
        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            sys.exit(0)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    main()
