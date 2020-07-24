#!/usr/bin/env python

from Crypto.Util.number import *
#Useful for bytes_to_long and inverse

def iterative_egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q,r = b//a,b%a; m,n = x-u*q,y-v*q # use x//y for floor "floor division"
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

#Idea: Since the modulus n is the same and the gcd(e1,e2)=1, the diophantine equation e1*x + e2*y = 1 has
# a solution. Find the solution, it handles the negative exponents constructs the number m^(x*e1+y*e2)

n=5196832088920565976847626600109930685983685377698793940303688567224093844213838345196177721067370218315332090523532228920532139397652718602647376176214689
e1=15
e2=13
c1=2042084937526293083328581576825435106672034183860987592520636048680382212041801675344422421233222921527377650749831658168085014081281116990629250092000069
c2=199621218068987060560259773620211396108271911964032609729865342591708524675430090445150449567825472793342358513366241310112450278540477486174011171344408

gcd, x, y = iterative_egcd(e1, e2)

if(x < 0):
    res1 = pow(c1, -x, n)
    res1 = inverse(res1, n)
else:
    res1 = pow(c1, x, n)

if(y < 0):
    res2 = pow(c2, -y, n)
    res2 = inverse(res2, n)
else:
    res2 = pow(c2, y, n)

res3 = res1*res2 % n

print(long_to_bytes(res3).decode())
