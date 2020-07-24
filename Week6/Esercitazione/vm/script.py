#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from string import printable
import subprocess
import re

exe = context.binary = ELF('VM_original')

def start(argv=[], *a, **kw):
    return process(["perf", "stat", "-e instructions",exe.path], *a, **kw)

gdbscript = '''
br *0x400cfe
continue
set pagination off
define do_count
set $count=0
while ($pc != $arg0)
stepi
set $count=$count+1
end
print $count
end
do_count 0x400d0f
'''.format(**locals())

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

cur_str = []
reg = re.compile(b'\n\n         (.*)       instructions')

while(True):

    min_instr = 2**64
    min_instr_char = "a"

    for i in printable[0:92]:

        child = subprocess.Popen(["perf", "stat", "-e instructions", "./VM_original"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        result = child.communicate(input=(b"".join(cur_str)) + bytes(i, "ascii"))
        perf_output = result[1]

        reg_result = reg.search(perf_output).group(1)
        reg_result = reg_result.replace(b",", b"")
        reg_result = int(reg_result)
#        print(perf_output)
        print(i + ": %d" % reg_result)

        if(reg_result < min_instr):
            min_instr = reg_result
            min_instr_char = i

    cur_str.append(bytes(min_instr_char, "ascii"))
    print(b"".join(cur_str))

#Il numero di istruzioni quando la stringa e' corretta e' inferiore
#CCIT 0x1b3b
#X-MA 0x1a1b
#C 0xb24

io.interactive()

