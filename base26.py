from itertools import batched

def base_26_encode(message):
	for group in batched(message, 5):
		group = ''.join(group)
		rem = 5 - len(group)
		if rem != 0:
			group += 'X' * rem
		
		print(group)


base_26_encode('ATTACKATDAWN')