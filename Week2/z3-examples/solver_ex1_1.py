from z3 import *


s = Solver()

x = Int('x')

s.add( x % 7 == 0)
s.add( x % 5 == 0)
s.add( x / 1000 == 5)
s.add( (x / 100) % 10 == 3)


s.check()

m = s.model()

print(m)
