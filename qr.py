import sys
from itertools import batched, chain


graph = [[0] * 33 for _ in range(33)]


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


def put_timing_horiz(i, j, j_end):
	for r in range(j, j_end + 1):
		pxl_on(i, r, r % 2 == 0)


def put_timing_vert(i, j, i_end):
	for c in range(i, i_end + 1):
		pxl_on(c, j, c % 2 == 0)


def upper_bound(j):
	return 9 if j < 9 or j > 24 else 0


def lower_bound(j):
	return 24 if j < 9 else 32


def skip(i, j):
	return i == 6 or (24 <= i <= 28 and 24 <= j <= 28)


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
	for f in range(len(message_bytes), 114):
		yield from iter_int_bits([0xEC, 0x11][f % 2])


i = 32
j = 32
d = 1
bits = iter_bits()
# sys.exit()

for a in range(841):
	zig = j - (a % 2)
	if not skip(i, zig):
		try:
			b = next(bits)
		except StopIteration:
			break
		pxl_on(i, zig, b ^ mask0(i, zig))
		
	i -= d * (a % 2)

	if d == 1:
		if i < upper_bound(j):
			d = -1
			j -= 2
			if j == 6:
				j = 5
			i = upper_bound(j)
	else:
		if i > lower_bound(j):
			d = 1
			j -= 2
			if j == 6:
				j = 5
			i = lower_bound(j)


put_position(0, 0)
put_position(0, 26)
put_position(26, 0)
put_alignment(24, 24)
put_timing_horiz(6, 7, 25)
put_timing_vert(7, 6, 25)
disp_graph()