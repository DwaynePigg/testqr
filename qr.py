import sys
import string
from itertools import batched, chain, repeat


ALPHANUMERIC = string.digits + string.ascii_uppercase + ' $%*+-./:'

FORMAT_L0 = 0b111011111000100

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
	pxl_on(size - 8, 8)


def put_format(bits=FORMAT_L0, size=33):
	# bits = 0b111111111111111
	for a in range(6):
		pxl_on(a, 8, (FORMAT_L0 >> a) & 1)

	pxl_on(7, 8, (FORMAT_L0 >> 6) & 1)
	pxl_on(8, 8, (FORMAT_L0 >> 7) & 1)
	pxl_on(8, 7, (FORMAT_L0 >> 8) & 1)

	for a in range(6):
		pxl_on(8, 5 - a, (FORMAT_L0 >> 9 + a) & 1)

	for a in range(8):
		pxl_on(8, size - 1 - a, (FORMAT_L0 >> a) & 1)

	for a in range(7):
		pxl_on(size - 7 + a, 8, (FORMAT_L0 >> 8 + a) & 1)



def mask0(i, j):
	return (i + j) % 2 == 0



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
put_timing()
put_format()


def skip(i, j):
	return i == 6 or abs(i - 26) <= 2 and abs(j - 26) <= 2


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
	
	# TODO: ECC
	for _ in range(20):
		yield from (0, 0, 0, 0, 0, 0, 0, 0)
	
	yield from (0, 0, 0, 0, 0, 0, 0)


def top_row(j):
	return 9 if j < 9 or j > 24 else 0


def bottom_row(j):
	return 24 if j < 9 else 32


i = 32
j = 32
d = 1
a = 0
bits = iter_bits('HELLO WORLD!HELLO WORLD!HELLO WORLD!HELLO WORLD!HELLO WORLD!HELLO WORLD!000000')

try:
	# sys.exit()
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
			if i < top_row(j):
				d = -1
				j -= (2 + (j == 8))
				i = top_row(j)
		else:
			if i > bottom_row(j):
				d = 1
				j -= (2 + (j == 8))
				i = bottom_row(j)
finally:
	disp_graph()
