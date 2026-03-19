length = 0
buffer = bytearray()

def put(n, size):
	global length, buffer
	rem = 8 - (length % 8)
	while size > 1:
		buffer.append(0)
		count = size - rem
		# print('down' if count > 0 else 'up', abs(count))
		p = 2**count
		high = int(n / p)
		buffer[-1] |= high
		print(f"{f"{n:0{size}b}":>12} {size=:2} {rem=:1} {high=:08b}")
		size -= rem
		length += rem
		n = n % p
		rem = 8
	print('***', length)
	
	

put(2, 4)
put(15, 9)
put(479, 11)
put(1315, 11)
print(' '.join(f"{b:02X}" for b in buffer))
# 20 79 DF A4 68 C3 2F 53 D4 A7 6D EC 00 