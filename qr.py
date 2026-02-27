import sys
import string

from collections import deque
from itertools import batched, chain, repeat

import qrcode
import segno
from segno import encoder
from qrcodegen import QrCode, QrSegment


def verify_nayuki(message):
	seg = QrSegment.make_bytes(message.encode('utf-8'))
	qr = QrCode.encode_segments([seg], QrCode.Ecc.LOW, minversion=4, maxversion=4, mask=0, boostecl=False)
	return tuple(bytes(1 if qr.get_module(j, i) else 0 for j in range(33))
    for i in range(33))


def verify_qr(message):
	qr = qrcode.QRCode(version=4, error_correction=qrcode.constants.ERROR_CORRECT_L, mask_pattern=0)
	qr.add_data(message)
	qr.make()
	# qr.print_ascii(invert=True)
	print(' '.join(f"{b:02X}" for b in qr.data_cache))
	return tuple(bytearray(row) for row in qr.modules)


def verify_segno(message):
	qr = segno.make(message.encode('utf-8'), version=4, error='L', mask=0, mode='byte', boost_error=False)
	return qr.matrix


GF256_LOG = bytes([0,0,1,25,2,50,26,198,3,223,51,238,27,104,199,75,4,100,224,14,52,141,239,129,28,193,105,248,200,8,76,113,5,138,101,47,225,36,15,33,53,147,142,218,240,18,130,69,29,181,194,125,106,39,249,185,201,154,9,120,77,228,114,166,6,191,139,98,102,221,48,253,226,152,37,179,16,145,34,136,54,208,148,206,143,150,219,189,241,210,19,92,131,56,70,64,30,66,182,163,195,72,126,110,107,58,40,84,250,133,186,61,202,94,155,159,10,21,121,43,78,212,229,172,115,243,167,87,7,112,192,247,140,128,99,13,103,74,222,237,49,197,254,24,227,165,153,119,38,184,180,124,17,68,146,217,35,32,137,46,55,63,209,91,149,188,207,205,144,135,151,178,220,252,190,97,242,86,211,171,20,42,93,158,132,60,57,83,71,109,65,162,31,45,67,216,183,123,164,118,196,23,73,236,127,12,111,246,108,161,59,82,41,157,85,170,251,96,134,177,187,204,62,90,203,89,95,176,156,169,160,81,11,245,22,235,122,117,44,215,79,174,213,233,230,231,173,232,116,214,244,234,168,80,88,175])
GF256_EXP = bytes([1,2,4,8,16,32,64,128,29,58,116,232,205,135,19,38,76,152,45,90,180,117,234,201,143,3,6,12,24,48,96,192,157,39,78,156,37,74,148,53,106,212,181,119,238,193,159,35,70,140,5,10,20,40,80,160,93,186,105,210,185,111,222,161,95,190,97,194,153,47,94,188,101,202,137,15,30,60,120,240,253,231,211,187,107,214,177,127,254,225,223,163,91,182,113,226,217,175,67,134,17,34,68,136,13,26,52,104,208,189,103,206,129,31,62,124,248,237,199,147,59,118,236,197,151,51,102,204,133,23,46,92,184,109,218,169,79,158,33,66,132,21,42,84,168,77,154,41,82,164,85,170,73,146,57,114,228,213,183,115,230,209,191,99,198,145,63,126,252,229,215,179,123,246,241,255,227,219,171,75,150,49,98,196,149,55,110,220,165,87,174,65,130,25,50,100,200,141,7,14,28,56,112,224,221,167,83,166,81,162,89,178,121,242,249,239,195,155,43,86,172,69,138,9,18,36,72,144,61,122,244,245,247,243,251,235,203,139,11,22,44,88,176,125,250,233,207,131,27,54,108,216,173,71,142])
RS_POLY_20 = bytes([152, 185, 240, 5, 111, 99, 6, 220, 112, 150, 69, 36, 187, 22, 228, 198, 121, 121, 165, 174])
RS_POLY_20_LOG = bytes([17, 60, 79, 50, 61, 163, 26, 187, 202, 180, 221, 225, 83, 239, 156, 164, 212, 212, 188, 190])
RS_POLY_7 = bytes([127, 122, 154, 164, 11, 68, 117])


ALPHANUMERIC = string.digits + string.ascii_uppercase + ' $%*+-./:'

FORMAT_L0 = 0b111011111000100


matrix = tuple(bytearray(33) for _ in range(33))


def pxl_on(i, j, state=1):
	if not (0 <= i < 33) or not (0 <= j < 33):
		raise ValueError(i, j)
	matrix[i][j] = state


def disp_graph(graph=matrix):
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


# for i in range(33):
	# for j in range(33):
		# pxl_on(i, j, abs(i - 26) <= 2 and abs(j - 26) <= 2 or abs(i - 8) <= 2 and abs(j - 26) <= 2 or abs(i - 26) <= 2 and abs(j - 8) <= 2)


# disp_graph()
# sys.exit()

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


def get_ecc_bytes(data, n_ecc=20):
	ecc = deque(0 for _ in range(n_ecc))
	for b in data:
		factor = b ^ ecc[0]
		ecc[0] = 0
		ecc.rotate(-1)
		if factor != 0:
			for i, coef in enumerate(RS_POLY_20_LOG):
				ecc[i] ^= GF256_EXP[(coef + GF256_LOG[factor]) % 255]

	return bytes(ecc)


def iter_bits(message='HELLO WORLD!'):
	message_bytes = message.encode('utf-8')
	buf = bytearray([0x4 << 4])
	
	def pack_half(b):
		buf[-1] |= b >> 4
		buf.append((b & 0xF) << 4)

	length = len(message_bytes)
	pack_half(length)
	for m in message_bytes:
		pack_half(m)
	
	for f in range(0, 78 - length):
		buf.append([0xEC, 0x11][f % 2])

	print(' '.join(f"{b:02X}" for b in buf + get_ecc_bytes(buf)))
	
	for b in buf:
		yield from iter_int_bits(b)
	for e in get_ecc_bytes(buf):
		yield from iter_int_bits(e)

	yield from (0, 0, 0, 0, 0, 0, 0)


def top_row(j):
	return 9 if j < 9 or j > 24 else 0


def bottom_row(j):
	return 24 if j < 9 else 32
	
	
def _ti_bottom_row(J):
	return 32-8*(J<9)
def _ti_top_row(J):
	return 9*(J<9 or J>24)


i = 32
j = 32
d = 1
a = 0

message = ' '.join(sys.argv[1:])

bits = bytes(iter_bits(message))

correct = verify_qr(message)
bits_it = iter(bits)

try:
	# sys.exit()
	while True:
		zig = j - (a % 2)
		if not skip(i, zig):
			try:
				b = next(bits_it)
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
	if matrix == correct:
		disp_graph()
		print('Correct!')
	else:
		diff = [
			[col1 ^ col2 for col1, col2 in zip(row1, row2)] 
		for row1, row2 in zip(matrix, correct)]
		disp_graph(diff)
		print('Incorrect! Diff displayed.')
