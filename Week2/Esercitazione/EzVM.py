from z3 import *

array = [b"\x00"] * 256

input_array = [b"\x4e", b"\x46", b"\x47", b"\x47", b"\x2d", b"\x4f", b"\x4f", b"\x4f", b"\x4b", b"\x2d", b"\x42", b"\x41", b"\x43", b"\x48", b"\x2d", b"\x4e", b"\x41", b"\x4f", b"\x49", b"\x2d", b"\x4f", b"\x4f", b"\x4e", b"\x49"]

symbol_array = ["0"] * 256

def EzVM():
    with open("./EzVM", "rb") as f:

        global array
        array = [b"\x00"] * 256

        new_byte = f.read(1)

        n_checks = 0

        while new_byte != b"":

            op = int.from_bytes(new_byte, 'big')

            if(op == 0):
                pass
            elif(op == 1):
                op1 = int.from_bytes(f.read(1), 'big')
                op2 = int.from_bytes(f.read(1), 'big')
        
                counter = 0
                for num in input_array:
                    array[op2 + counter] = num
                    symbol_array[op2 + counter] = "a[" + str(op2 + counter) + "]"
                    counter += 1

                assert(counter == op1)

            elif(op == 2):
                op1 = f.read(1)
                op2 = int.from_bytes(f.read(1), 'big')

                array[op2] = op1
                symbol_array[op2] = str(int.from_bytes(op1, 'big'))
            elif(op == 3):
                op1 = int.from_bytes(f.read(1), 'big')
                op2 = int.from_bytes(f.read(1), 'big')
                op3 = int.from_bytes(f.read(1), 'big')

                array[op3] = ((int.from_bytes(array[op1], 'big') + int.from_bytes(array[op2], 'big')) \
                    & 0xff).to_bytes(1, 'big')
                symbol_array[op3] = " (" + symbol_array[op1] + " + " + symbol_array[op2] + ") "
            elif(op == 4):
                op1 = int.from_bytes(f.read(1), 'big')
                op2 = int.from_bytes(f.read(1), 'big')
                op3 = int.from_bytes(f.read(1), 'big')

                array[op3] = ((int.from_bytes(array[op1], 'big') - int.from_bytes(array[op2], 'big')) \
                    & 0xff).to_bytes(1, 'big')
                symbol_array[op3] = " (" + symbol_array[op1] + " - " + symbol_array[op2] + ") "
            elif(op == 5):
                op1 = int.from_bytes(f.read(1), 'big')

                array[op1] = ((~int.from_bytes(array[op1], 'big')) & 0xff).to_bytes(1, 'big')
                symbol_array[op1] = " ( ~" + symbol_array[op1] + ") "
            elif(op == 6):
                op1 = int.from_bytes(f.read(1), 'big')
                op2 = int.from_bytes(f.read(1), 'big')
                op3 = int.from_bytes(f.read(1), 'big')

                array[op3] = ((int.from_bytes(array[op1], 'big') & int.from_bytes(array[op2], 'big')) \
                    & 0xff).to_bytes(1, 'big')
                symbol_array[op3] = " (" + symbol_array[op1] + " & " + symbol_array[op2] + ") "
            elif(op == 7):
                op1 = int.from_bytes(f.read(1), 'big')
                op2 = int.from_bytes(f.read(1), 'big')
                op3 = int.from_bytes(f.read(1), 'big')

                array[op3] = ((int.from_bytes(array[op1], 'big') | int.from_bytes(array[op2], 'big')) \
                    & 0xff).to_bytes(1, 'big')
                symbol_array[op3] = " (" + symbol_array[op1] + " | " + symbol_array[op2] + ") "
            elif(op == 8):
                op1 = int.from_bytes(f.read(1), 'big')
                op2 = int.from_bytes(f.read(1), 'big')
                op3 = int.from_bytes(f.read(1), 'big')

                array[op3] = ((int.from_bytes(array[op1], 'big') ^ int.from_bytes(array[op2], 'big')) \
                    & 0xff).to_bytes(1, 'big')
                symbol_array[op3] = " (" + symbol_array[op1] + " ^ " + symbol_array[op2] + ") "
            elif(op == 9):
                op1 = int.from_bytes(f.read(1), 'big')
                op2 = int.from_bytes(f.read(1), 'big')

                if(array[op1] != array[op2]):
                    print("Expr1: ", end="")
                    print(symbol_array[op1])
                    print("Expr2: ", end="")
                    print(symbol_array[op2])
                    new_byte = b""
                    continue

                n_checks += 1

            new_byte = f.read(1)

    return n_checks

s = Solver()

a = Array("a", BitVecSort(8), BitVecSort(8))

#checks 1
s.add(a[0x4] == 0x2d)
s.add(a[0x9] == 0x2d)
s.add(a[0xe] == 0x2d)
s.add(a[0x13] == 0x2d)

#checks 2
for i in range(0x18):
    if(not i in [0x4, 0x9, 0xe, 0x13]):
        s.add(a[i] & 0xf0 == 0x40)

#checks 3
s.add(( ( ( ( ~ ( (a[3] & 15)  | 240) )  +  ( ( ~ ( (a[2] & 15)  | 240) )  +  ( ( ~ ( (a[1] & 15)  | 240) )  +  ( ( ~ ( (a[0] & 15)  | 240) )  + 0) ) ) )  - 243)  ^ 39) == 0)

#checks 4
s.add(( ( ( ( ~ ( (a[8] & 15)  | 240) )  +  ( ( ~ ( (a[7] & 15)  | 240) )  +  ( ( ~ ( (a[6] & 15)  | 240) )  +  ( ( ~ ( (a[5] & 15)  | 240) )  + 0) ) ) )  - 205)  ^ 55) == 0)

#checks 5
s.add(( ( ( ( ~ ( (a[13] & 15)  | 240) )  +  ( ( ~ ( (a[12] & 15)  | 240) )  +  ( ( ~ ( (a[11] & 15)  | 240) )  +  ( ( ~ ( (a[10] & 15)  | 240) )  + 0) ) ) )  - 26)  ^ 20) == 0)

#checks 6
s.add(( ( ( ( ~ ( (a[18] & 15)  | 240) )  +  ( ( ~ ( (a[17] & 15)  | 240) )  +  ( ( ~ ( (a[16] & 15)  | 240) )  +  ( ( ~ ( (a[15] & 15)  | 240) )  + 0) ) ) )  - 102)  ^ 175) == 0)

#checks 7
s.add(( ( ( ( ~ ( (a[23] & 15)  | 240) )  +  ( ( ~ ( (a[22] & 15)  | 240) )  +  ( ( ~ ( (a[21] & 15)  | 240) )  +  ( ( ~ ( (a[20] & 15)  | 240) )  + 0) ) ) )  - 77)  ^ 186) == 0)

s.check()

result = ""

for i in range(0x18):
    result += chr(int(str(s.model().eval(a[i]))))
    print(int(str(s.model().eval(a[i]))).to_bytes(1, 'big').hex(), end=" ")

print()

print(result)

# tot_check = 29

num_checks = EzVM()

print(num_checks)
