def rotl(num, bits):
    bit = num & (1 << (bits-1))
    num <<= 1
    if(bit):
        num |= 1
    num &= (2**bits-1)

    return num

def rotr(num, bits):
    num &= (2**bits-1)
    bit = num & 1
    num >>= 1
    if(bit):
        num |= (1 << (bits-1))

    return num

with open("flag.txt.aes", "rb") as f:
	byte = f.read(1)
	i = 1
	while byte != b"":
		result = int.from_bytes(byte, "little")
		for x in range(i):
			result = rotl(result, 8)
		print(chr(result), end='')
		byte = f.read(1)
		i = i + 1
