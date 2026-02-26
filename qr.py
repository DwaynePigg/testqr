import sys
import string
from itertools import batched, chain


def pxl_on(i, j, state=1):
	if not (0 <= i < 33) or not (0 <= j < 33):
		raise ValueError(i, j)
	graph[i][j] = state


def disp_graph():
	print('▒' * 37)
	for row1, row2 in batched(chain(graph, [(0 for _ in range(33))]), 2):
		print('▒▒', end='')
		for px1, px2 in zip(row1, row2):
			print(' ▀▄█'[~(px1 | (px2 << 1))], end='')
		print('▒▒')
	print('▒' * 37)


def put_position(i, j):
	pattern = [
		[1,1,1,1,1,1,1],
		[1,0,0,0,0,0,1],
		[1,0,1,1,1,0,1],
		[1,0,1,1,1,0,1],
		[1,0,1,1,1,0,1],
		[1,0,0,0,0,0,1],
		[1,1,1,1,1,1,1],
	]
	for r in range(7):
		for c in range(7):
			pxl_on(i + r, j + c, pattern[r][c])


def put_alignment(i, j):
	pattern = [
		[1,1,1,1,1],
		[1,0,0,0,1],
		[1,0,1,0,1],
		[1,0,0,0,1],
		[1,1,1,1,1],
	]
	for r in range(5):
		for c in range(5):
			pxl_on(i + r, j + c, pattern[r][c])


def put_timing(size=33):
	for j in range(7, size - 7):
		pxl_on(6, j, 1 - j % 2)
	for i in range(7, size - 7):
		pxl_on(i, 6, 1 - i % 2)


ALPHANUMERIC = string.digits + string.ascii_uppercase + ' $%*+-./:'


# _,X = 0,1
# graph = [
	# [X,X,X,X,X,X,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,X,X,X,X,X,X],
	# [X,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,_,_,_,_,X],
	# [X,_,X,X,X,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,X,X,X,_,X],
	# [X,_,X,X,X,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,X,X,X,_,X],
	# [X,_,X,X,X,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,X,X,X,_,X],
	# [X,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,_,_,_,_,X],
	# [X,X,X,X,X,X,X,_,X,_,X,_,X,_,X,_,X,_,X,_,X,_,X,_,X,_,X,X,X,X,X,X,X],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,X,X,X,X,_,_,_,_],
	# [_,_,_,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,_,_,X,_,_,_,_],
	# [X,X,X,X,X,X,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,X,_,X,_,_,_,_],
	# [X,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,_,_,_,X,_,_,_,_],
	# [X,_,X,X,X,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,X,X,X,X,_,_,_,_],
	# [X,_,X,X,X,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [X,_,X,X,X,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [X,_,_,_,_,_,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
	# [X,X,X,X,X,X,X,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
# ]

graph = [[0] * 33 for _ in range(33)]
put_position(0, 0)
put_position(0, 26)
put_position(26, 0)
put_alignment(24, 24)
put_timing(33)

FORMAT_L0 = 0b111011111000100

for a in range(6):
	pxl_on(8, a, (FORMAT_L0 >> (14 - a)) & 1)
for a in range(6):
	pxl_on(5 - a, 8, (FORMAT_L0 >> (5 - a)) & 1)

pxl_on(8, 7, (FORMAT_L0 >> 8) & 1)
pxl_on(8, 8, (FORMAT_L0 >> 7) & 1)
pxl_on(7, 8, (FORMAT_L0 >> 6) & 1)

for a in range(8):
	pxl_on(8, 32 - a, (FORMAT_L0 >> a) & 1)
for a in range(7):
	pxl_on(26 + a, 8, (FORMAT_L0 >> a + 8) & 1)


def skip(i, j):
	return i == 6 or abs(i - 26) <= 2 and abs(j - 26) <= 2


def mask0(i, j):
	return (i + j) % 2 == 0


def iter_int_bits(n):
	for i in range(7, -1, -1):
		yield (n >> i) & 1


def iter_bits(message='HELLO WORLD!'):
	yield from (0, 1, 0, 0)
	yield from iter_int_bits(len(message))
	message_bytes = message.encode('utf-8')
	for b in message_bytes:
		yield from iter_int_bits(b)
	yield from (0, 0, 0, 0)
	for f in range(len(message_bytes), 78):
		yield from iter_int_bits([0xEC, 0x11][f % 2])


# P-Mint(P/M

def get_codewords(message='HELLO WORLD!'):
	length = len(message)
	B = 64
	
	
	
	L1 = []
	I = 4
	for L in message:
		pass



i = 32
j = 32
d = 1
a = 0
bits = iter_bits()

try:
	while True:
		zig = j - (a % 2)
		if not skip(i, zig):
			try:
				b = next(bits)
			except StopIteration:
				break
			pxl_on(i, zig, b ^ mask0(i, zig))
			
		i -= d * (a % 2)
		a += 1

		if d == 1:
			top_row = 9 if j < 9 or j > 24 else 0
			if i < top_row:
				d = -1
				j -= (2 + (j == 6))
				i = top_row
		else:
			bottom_row = 24 if j < 9 else 32
			if i > bottom_row:
				d = 1
				j -= (2 + (j == 6))
				i = bottom_row
finally:
	disp_graph()
