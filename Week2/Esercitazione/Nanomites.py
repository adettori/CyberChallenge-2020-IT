data_str = "0b 6e 42 14 54 34 1d 6e 4a 26 36 30 2f 6d 30 38 58 31 41 74 41 4a 6a 65 53 5f 33 5c 49 33 65 34 37 6e 64 73 77 79 66"

rip_step = 0x9
rip_array_res = [0xb] # starting address 0x00400acc
rip_array = []
data_array = []

for byte in data_str.split():
    data_array.append(int(byte, 16))

result1 = ""

for i in range(len(data_array)//3):
    result1 += chr(data_array[i*3 + ((i - (i >> 0x1f) & 0x1) + (i >> 0x1f)) + 1])

print(result1)

