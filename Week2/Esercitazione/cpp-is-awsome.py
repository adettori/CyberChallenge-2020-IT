
str1 = "24 00 00 00 00 00 00 00 05 00 00 00 36 00 00 00 65 00 00 00 07 00 00 00 27 00 00 00 26 00 00 00 2d 00 00 00 01 00 00 00 03 00 00 00 00 00 00 00 0d 00 00 00 56 00 00 00 01 00 00 00 03 00 00 00 65 00 00 00 03 00 00 00 2d 00 00 00 16 00 00 00 02 00 00 00 15 00 00 00 03 00 00 00 65 00 00 00 00 00 00 00 29 00 00 00 44 00 00 00 44 00 00 00 01 00 00 00 44 00 00 00 2b 00 00 00"

important_str = "4c 33 74 5f 4d 45 5f 54 33 6c 6c 5f 59 30 75 5f 53 30 6d 33 74 68 31 6e 67 5f 31 6d 70 30 72 74 61 6e 74 5f 41 5f 7b 46 4c 34 47 7d 5f 57 30 6e 74 5f 62 33 5f 33 58 34 63 74 6c 79 5f 74 68 34 74 5f 33 34 35 79 5f 74 30 5f 63 34 70 74 75 72 33 5f 48 30 77 65 76 33 72 5f 31 54 5f 77 31 6c 6c 5f 62 33 5f 43 30 30 6c 5f 31 46 5f 59 30 75 5f 67 30 74 5f 31 74 00"

array1 = []
important_array = []

count = 0
for i in str1.split():
    if(count % 4 == 0):
        array1.append(int(i, 16))
    count += 1

for i in important_str.split():
    important_array.append(int(i, 16))

result = ""

for i in array1:
    result += chr(important_array[i])

print(result)
