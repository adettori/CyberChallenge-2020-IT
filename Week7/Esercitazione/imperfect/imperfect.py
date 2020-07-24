#!/usr/bin/env python3

import random
from functools import reduce

flag = "ccit{faaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaa}a"
class stream:
  s = None
  m = None
  c = None
  n = None

  def __init__(self, s, m, c, n):
    self.s = s
    self.m = m
    self.c = c
    self.n = n

  def next(self): #((s*(m) % n) + c) % n => (s*(m) + c) % n
    next = self.s
    for _ in range(1, self.m): #res = (s*(m) % n)
      self.s += next
      if self.s >= self.n:
        self.s -= self.n
    self.s += self.c #res += c
    if self.s >= self.n: # res % n
      self.s -= self.n
    return next

def s2i(x): #Usato da prepare
  return (ord(x[0])<<8) | ord(x[1]) #Concatena una coppia di byte

def i2s(x): #Separa i due byte di sopra
  return [x>>8, x&0xff]

def i2i(x, y):
  z = [(((x&(1<<i))>>i) != ((y&(1<<i))>>i)) for i in range(16)][::-1] #xor dal bit piu' significante
  return reduce(lambda x, y: (x<<1)|y, z) #Apply lambda to z, lambda outputs z concatenated

def prepare(b):
  assert("ccit{f" in b)
  assert(0 == (1 & len(b))) #b ha lunghezza pari
  assert(0 == (1 & b.index("ccit{f"))) #ccit e' in una posizione pari
  assert('}' == b[b.index("ccit{f")+50]) #termina dopo 50 byte
  b = [b[i:i+2] for i in range(0, len(b), 2)]
  b = [s2i(x) for x in b] #Concatena due byte alla volta
  return b

def encrypt(b):
  n = 0xffff+1 #Limits to max 2 bytes len output
  s = random.sample([i for i in range(2, n) if i & 0 == 0], 1)[0] #Qualsiasi numero
  c = random.sample([i for i in range(2, n) if i & 1 == 1], 1)[0] #Numero dispari
  m = random.sample([i for i in range(2, n) if i & 3 == 1], 1)[0] #i&3==1 <=> 2o bit 0 e 1o bit 1=>dispari
  print(m)
  print(m%2)
  gen = stream(s, m, c, n)
  o = []
  for x in b:
    o.extend(i2s(i2i(x, gen.next()))) #Concatena alla fine gli elementi della lista arg
  return o

def main():
  with open("test.enc", "wb") as f:
    string = ''.join(chr(i) for i in encrypt(prepare(flag)))
    print(len(string))
    f.write(bytes(string, "utf-8"))

if __name__ == "__main__":
  main()
