#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long
from Crypto.Random.random import getrandbits # cryptographically secure random get pranked

from secret import d, flag


# 1024-bit rsa is unbreakable good luck
n = 137477930153023677652461319156668052004127498630179106472900685001647543482119088241024148836523782038991616192419898244423175204552475949051726128852374005165392089441539285236458768030898674515008191047827480863114006107416364034170615325099573183715071452890965984939995463550613603055000025060736899278821
e = 0x10001 #65537

f = bytes_to_long(bytes(flag,'utf-8'))
print("Encrypted flag:")
print(pow(f,e,n))

def otp(m):
	# perfect secrecy ahahahaha
	out = ""
	for i in bin(m)[2:]: #Salta il 0b di python
		out+=str(int(i)^getrandbits(1))
	return out

while 1:
	try:
		i = int(input("Enter message to sign: "))
		assert(0 < i < n)
		print("signed message (encrypted with unbreakable otp):")
		print(otp(pow(i,d,n)))
	except e:
		print("bad input, exiting",e)
		break
