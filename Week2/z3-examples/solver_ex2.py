from z3 import *

# There are a few datatypes to choose from. For our purpose,
# 32-bit BitVecs are a good representation of ints. Z3 has its
# own int, which is more a 'mathematical int', it can get infinitely
# large and does not support bitwise operations.
x, y, z = BitVecs("x y z", 32)

#Now just add the constraints
s = Solver()
s.add(x % 7 == 0)
s.add((x | y) & 0xFF == 123)
s.add(x > 1337337)
s.add(z == (x + y)/2)
s.add(z < 42424242)

#and check if a solution exists. If there is one, it will be printed.
while s.check() != z3.sat:
    pass
	
print(s.model())

