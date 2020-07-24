#!/bin/env python3

import random
from Crypto.Util.number import isPrime, bytes_to_long
from secret import FLAG

while True:
  x = random.randint(2, 2**768)

  p = x**2 - x + 1
  q = x**4 - x**3 + x**2 - x + 1

  if isPrime(p) and isPrime(q):
    break

m = bytes_to_long(FLAG.encode())
e = 65537
n = p*q

c = pow(m, e, n)

print("n =", n)
print("e =", e)
print("c =", c)
