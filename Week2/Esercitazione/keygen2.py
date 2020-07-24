from z3 import *

s = Solver()

a = Array("a", BitVecSort(32), BitVecSort(32))

#len = 16

for i in range(16):
    s.add(Or(And(a[i] >= 0, a[i] <= 9), And(a[i] >= 0xa , a[i] <= 0x23)))

#check 1
x1 = (a[0] + a[1]) % 0x24
x2 = If(x1 == 0xe, BitVecVal(1, 32), BitVecVal(0, 32))
s.add(x1 == 0xe)

#check 2
x1 = (a[2] + a[3]) % 0x24
x2 = If(x1 == 0x18, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 3
x1 = (a[2] - a[0]) % 0x24
x2 = If(x1 == 0x6, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 4
x1 = (a[1] + a[3] + a[5]) % 0x24
x2 = If(x1 == 0x4, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 5
x1 = (a[2] + a[4] + a[6]) % 0x24
x2 = If(x1 == 0xd, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 6
x1 = (a[3] + a[4] + a[5]) % 0x24
x2 = If(x1 == 0x16, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 7
x1 = (a[6] + a[8] + a[10]) % 0x24
x2 = If(x1 == 0x1f, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 8
x1 = (a[1] + a[4] + a[7]) % 0x24
x2 = If(x1 == 0x7, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 9
x1 = (a[9] + a[0xc] + a[0xf]) % 0x24
x2 = If(x1 == 0x14, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 10
x1 = (a[0xd] + a[0xe] + a[0xf]) % 0x24
x2 = If(x1 == 0xc, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 11
x1 = (a[8] + a[9] + a[10]) % 0x24
x2 = If(x1 == 0x1b, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

#check 12
x1 = (a[7] + a[0xc] + a[0xd]) % 0x24
x2 = If(x1 == 0x17, BitVecVal(1, 32), BitVecVal(0, 32))
s.add((x1 & 0xffffff00 | x2) != 0)

s.check()

result = ""

for i in range(16):
    x = int(str(s.model().eval(a[i])))
    if(x < 0xa):
        x += 0x30
    else:
        x += 0x37

    result += chr(x)


print(result)
