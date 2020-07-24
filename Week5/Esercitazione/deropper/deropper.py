#!/usr/bin/env python
import r2pipe
import sys
import re
from z3 import *

#DATA = 0x004040a0
# -Prende i return del programma e li confronta con r[]
# -Negli offset sono contenuti dei payload
# -exit(num) calcola num&0xFF come return del programma ljust(8, b"\x00")

#Radare2 analysis
r2_obj = r2pipe.open("main", flags=['-2']) #No stderr
r2_obj.cmd('aa')

istr_dict = dict()

flag_base = 0x004040a0

def disassemble_istr_until_ret(istr_addr):
    
    istr_array = []

    disasm_code = r2_obj.cmd("pd @0x%x" % istr_addr).split("\n")
    
    ret_found = False
    index = 0

    while(not ret_found):
        disasm_line = disasm_code[index]

        dist_start_istr = 43
        istr_line = re.search(".?"*dist_start_istr + "(.+?)$", disasm_line).group(1)
        
        if("ret" in istr_line):
            ret_found = True
        
        istr_array.append(istr_line.strip())
        index += 1

    return istr_array


def format_payload(payload_str):
    
    index = 0
    istr_array = []
    addr_len = 8

    while(payload_str[index] == ord("a")):
        index += 1
    
    payload_str = payload_str[index:len(payload_str)]
    
    for i in range(0, len(payload_str) - addr_len, addr_len):
        istr_array.append(payload_str[i:i+addr_len].ljust(8, b"\x00"))

    return istr_array

def assembly_add(op1, op2, regs_dict):

    if("byte" in op1 or "byte" in op2):
        print("PROBLEM")
        sys.exit(2)

    sum_res= f"({regs_dict[op1]} + {regs_dict[op2]})"

    regs_dict[op1] = sum_res
    return regs_dict

def assembly_sub(op1, op2, regs_dict):

    if("byte" in op1 or "byte" in op2):
        print("PROBLEM")
        sys.exit(2)

    sum_res= f"({regs_dict[op1]} - {regs_dict[op2]})"

    regs_dict[op1] = sum_res

    return regs_dict

def assembly_xor(op1, op2, regs_dict):

    regs_dict[op1] = f"({regs_dict[op1]} ^ {regs_dict[op2]})"

    return regs_dict

def assembly_mov(op1, op2, regs_dict):

    done = False

    if("byte" in op2):
        op2 = re.search("\[(.+?)\]$", op2).group(1)

        regs_dict[op1] = f"(flag_str[{regs_dict[op2]}])"
        done = True

    if("byte" in op1):
        print("PROBLEM")
        sys.exit(2)
    
    if(not done):
        regs_dict[op1] = f"({regs_dict[op2]})"

    return regs_dict

def simulate_assembly(payload_array):

    regs = dict()

    payload_iter = iter(payload_array)
    expr = ""

    for p in payload_iter:

        value = int.from_bytes(p, "little")

        if(value < 0x400000):
            print("ERROR!")
            sys.exit(1)

        if(value in istr_dict.keys()):
            istr_array = istr_dict[value]
        else:
            istr_array = disassemble_istr_until_ret(value)
            istr_dict[value] = istr_array


        for istr in istr_array:
            
            istr_mne = istr.split(" ")[0]
            #print(istr)

            if(istr_mne == "ret"):
                break
            istr_operands = istr[len(istr_mne):len(istr)].strip()

            if(istr_mne == "pop"):
                value = int.from_bytes(next(payload_iter, None), 'little')

                if(value >= flag_base):
                    value -= flag_base

                regs[istr_operands] = f"({value})"
                #print("0x%x" % value)

            elif(istr_mne == "add"):

                op1 = istr_operands.split(", ")[0]
                op2 = istr_operands.split(", ")[1]
            
                regs = assembly_add(op1, op2, regs)
            elif(istr_mne == "sub"):

                op1 = istr_operands.split(", ")[0]
                op2 = istr_operands.split(", ")[1]
            
                regs = assembly_sub(op1, op2, regs)

            elif(istr_mne == "xor"):

                op1 = istr_operands.split(", ")[0]
                op2 = istr_operands.split(", ")[1]
            
                regs = assembly_xor(op1, op2, regs)

            elif(istr_mne == "movzx" or istr_mne == "mov"):
            
                op1 = istr_operands.split(", ")[0]
                op2 = istr_operands.split(", ")[1]
            
                regs = assembly_mov(op1, op2, regs)

            else:
                print("PROBLEM")
                sys.exit(3)

            #print(regs)
    return regs["rdi"]

returns = [208, 225, 237, 20, 214, 183, 79, 105, 207, 217, 125, 66, 123, 104, 97, 99, 107 , 105, 109, 50, 48, 202, 111, 111, 29, 63, 223, 36, 0, 124, 100, 219, 32]
        
o = [296, 272, 272, 272, 296, 360, 272, 424, 272, 208, 120, 120, 120, 96, 120, 120, 120, 120, 120, 120, 120, 208, 120, 120, 208, 208, 208, 208, 208, 272, 120, 208, 208]

unique_flag = "abcdefghijklmnopqrstuvwxyz0123"

payload_list = []

with open('blob', 'rb') as f:
    for offset in o:
        payload = f.read(offset)

        formatted_payload = format_payload(payload)
        payload_list.append(formatted_payload)

s = Solver()

flag_str = Array("flag_str", BitVecSort(8), BitVecSort(8))

for i in range(len(payload_list)):

    expr = simulate_assembly(payload_list[i])

    s.add((eval(expr)) == returns[i])

s.check()

result = ""

for i in range(31):
    result += chr(int(str(s.model().eval(flag_str[i]))))

print(result)

