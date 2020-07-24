from z3 import *

s = Solver()

x, y = Ints('x y')

s.add(x + y < 12)

while s.check() == sat:
	m = s.model()
	print(m)
	s.add(Or(x!=m[x], y != m[y]))
