import z3
import string

flag = ""

x = z3.Int("x") # defines int variables in z3

s = z3.Solver()

s.add( x % 5 == 0)
s.add( x % 7 == 0)
s.add( x / 1000 == 5)
s.add( (x/100) % 10== 3)

while s.check() != z3.sat: # we wait for z3 to do its thing
    pass

print(s.model())
