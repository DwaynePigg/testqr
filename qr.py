import sys
import string

from collections import deque
from itertools import batched, chain, repeat

from rsconst import *

from qrcodegen import QrCode, QrSegment


def verify(message, version, encoding):
	if encoding == 'b':
		seg = QrSegment.make_bytes(message.encode('utf-8'))
	elif encoding == 'a':
		seg = QrSegment.make_alphanumeric(message)
	else:
		raise ValueError(encoding)
		
	qr = QrCode.encode_segments([seg], QrCode.Ecc.LOW, minversion=version, maxversion=version, mask=0, boostecl=False)
	size = qr.get_size()
	matrix = Matrix(size)
	for j in range(size):
		for i in range(size):
			matrix.pxl_on(i, j, qr.get_module(j, i))

	return matrix


ALPHANUMERIC = string.digits + string.ascii_uppercase + ' $%*+-./:'
AN_TABLE = { a: i for i, a in enumerate(ALPHANUMERIC) }

FORMAT_L0 = 0b111011111000100


class Matrix:

	def __init__(self, size):
		self.matrix = tuple(bytearray(size) for _ in range(size))
	
	@property
	def size(self):
		return len(self.matrix)

	def pxl_on(self, i, j, state=1):
		if not (0 <= i < self.size) or not (0 <= j < self.size):
			raise ValueError(i, j)
		self.matrix[i][j] = state

	def disp(self):
		print('▒' * (self.size + 4))
		for row1, row2 in batched(chain(self.matrix, [(0 for _ in range(self.size))]), 2):
			print('▒▒', end='')
			for px1, px2 in zip(row1, row2):
				print(' ▀▄█'[~(px1 | (px2 << 1))], end='')
			print('▒▒')
		print('▒' * (self.size + 4))

	def put_position(self, i, j):
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
				self.pxl_on(i + r, j + c, pattern[r][c])

	def put_alignment(self, i, j):
		pattern = [
			[1,1,1,1,1],
			[1,0,0,0,1],
			[1,0,1,0,1],
			[1,0,0,0,1],
			[1,1,1,1,1],
		]
		for r in range(5):
			for c in range(5):
				self.pxl_on(i + r, j + c, pattern[r][c])

	def put_timing(self):
		for j in range(7, self.size - 7):
			self.pxl_on(6, j, 1 - j % 2)
		for i in range(7, self.size - 7):
			self.pxl_on(i, 6, 1 - i % 2)
		self.pxl_on(self.size - 8, 8)

	def put_format(self, bits=FORMAT_L0):
		# bits = 0b111111111111111
		# 0b111011111000100
		for a in range(6):
			self.pxl_on(a, 8, (FORMAT_L0 >> a) & 1)

		self.pxl_on(7, 8, (FORMAT_L0 >> 6) & 1)
		self.pxl_on(8, 8, (FORMAT_L0 >> 7) & 1)
		self.pxl_on(8, 7, (FORMAT_L0 >> 8) & 1)

		for a in range(6):
			self.pxl_on(8, 5 - a, (FORMAT_L0 >> 9 + a) & 1)

		for a in range(8):
			self.pxl_on(8, self.size- 1 - a, (FORMAT_L0 >> a) & 1)

		for a in range(7):
			self.pxl_on(self.size - 7 + a, 8, (FORMAT_L0 >> 8 + a) & 1)
	
	def setup(self):
		self.put_position(0, 0)
		self.put_position(0, self.size - 7)
		self.put_position(self.size - 7, 0)
		self.put_alignment(self.size - 9, self.size - 9)
		self.put_timing()
		self.put_format()

	def top_row(self, j):
		return 9 if j < 9 or j > self.size - 9 else 0

	def bottom_row(self, j):
		return self.size - 9 if j < 9 else self.size - 1

	def skip(self, i, j):
		return i == 6 or abs(i - self.size + 7) <= 2 and abs(j - self.size + 7) <= 2

	def put_codewords(self, codewords):
		i = self.size - 1
		col = self.size - 1
		d = -1
		end = 9
		index = 0
		curr = codewords[0]
		power = 128
		
		while col > 0:
			for j in (col, col - 1):
				if not self.skip(i, j):
					
					# no-bitwise mode
					b = int(curr >= power)
					curr -= b * power
					power //= 2
					if power < 1:
						power = 128
						index += 1
						curr = codewords[index]
						# Always add remainder just so we don't go out of bounds

					self.pxl_on(i, j, b ^ mask0(i, j))
					
			if i == end:
				d = -d
				col -= (2 + (col == 8))
				i = self.top_row(col)
				end = self.bottom_row(col)
				if d == -1:
					i, end = end, i
			else:
				i += d

	
	def __eq__(self, other):
		return isinstance(other, Matrix) and self.matrix == other.matrix
	
	def __xor__(self, other):
		if not isinstance(other, Matrix) or self.size != other.size:
			raise ValueError(other)
			
		x = Matrix(self.size)
		for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix)):
			for j, (col1, col2) in enumerate(zip(row1, row2)):
				x.pxl_on(i, j, col1 ^ col2)
		return x
	
	def __repr__(self):
		return f"[Matrix: {self.size}x{self.size}]"


def mask0(i, j):
	return (i + j) % 2 == 0


def iter_int_bits(n):
	for i in range(7, -1, -1):
		yield (n >> i) & 1


def get_ecc_bytes(data, rs_poly):
	n_ecc = len(rs_poly)
	ecc = [0] * n_ecc
	for r, b in enumerate(data):
		offset = r % n_ecc
		factor = b ^ ecc[offset]
		ecc[offset] = 0
		if factor != 0:
			for i, coef in enumerate(rs_poly):
				ecc[(i + r + 1) % n_ecc] ^= GF256_EXP[(GF256_LOG[coef] + GF256_LOG[factor]) % 255]

	return bytes(ecc)


def get_ecc_bytes(data, rs_poly, blocks=1):
	n_ecc = len(rs_poly) // blocks
	ecc = deque(0 for _ in range(n_ecc))
	for b in data:
		factor = b ^ ecc[0]
		ecc[0] = 0
		ecc.rotate(-1)
		if factor != 0:
			for i, coef in enumerate(rs_poly):
				ecc[i % n_ecc] ^= GF256_EXP[(GF256_LOG[coef] + GF256_LOG[factor]) % 255]

	return bytes(ecc)


def iter_bits(message):
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
	
	for b in buf:
		yield from iter_int_bits(b)
	for e in get_ecc_bytes(buf):
		yield from iter_int_bits(e)

	yield from (0, 0, 0, 0, 0, 0, 0)


class BitBuffer:

	def __init__(self):
		self.buffer = bytearray()
		self.bit_length = 0

	def put(self, n, size=8):
		power = 2 ** (size - 1)
		while power >= 1:
			bit = n >= power
			if self.bit_length % 8 == 0:
				self.buffer.append(0)
			if bit:
				self.buffer[-1] += 2 ** (7 - self.bit_length % 8)
			self.bit_length += 1
			n -= bit * power
			power /= 2

	def put(self, n, size=8):
		for i in range(size - 1, -1, -1):
			bit = int(n / (2 ** i)) % 2
			# bit2 = int(2 * ((int(n / (2 ** i)) / 2) % 1))
			if self.bit_length % 8 == 0:
				self.buffer.append(0)
			if bit:
				self.buffer[-1] += 2 ** (7 - self.bit_length % 8)
			self.bit_length += 1

	def binary(self, message):
		self.put(4, 4)
		message_bytes = message.encode('utf-8')
		self.put(len(message_bytes))
		for m in message_bytes:
			self.put(m)
		self.put(0, 4)
	
	def alphanumeric(self, message):
		self.put(2, 4)
		self.put(len(message), 9)
		for pair in batched(message, 2):
			if len(pair) == 2:
				c1, c2 = pair
				self.put(45 * AN_TABLE[c1] + AN_TABLE[c2], 11)
			else:
				(c1,) = pair
				self.put(AN_TABLE[c1], 6)

		self.put(0, 4)



DATA_LENGTH = [None, 19, 34, 55, 80, 108, 136, 156, 194, 232, 274, 324]


def get_codewords(message, version, encoding):
	buffer = BitBuffer()
	if not callable(encoding):
		encoding = {
			'b': BitBuffer.binary,
			'a': BitBuffer.alphanumeric,
		}[encoding]
	encoding(buffer, message)
	codewords = buffer.buffer
	
	print(' '.join(f"{b:02X}" for b in codewords))
	
	data_length = DATA_LENGTH[version]
	for f in range(0, data_length - len(codewords)):
		codewords.append([0xEC, 0x11][f % 2])
	
	if version < 6:
		codewords.extend(get_ecc_bytes(codewords, RS_POLY[version]))
	elif version < 11:
		block1 = codewords[:data_length // 2]
		block2 = codewords[data_length // 2:]
		rs_poly = RS_POLY[version]
		ecc1 = get_ecc_bytes(block1, rs_poly, 2)
		ecc2 = get_ecc_bytes(block2, rs_poly, 2)
		codewords = block1 + block2 + ecc1 + ecc2
	else:
		raise ValueError()
	
	codewords.append(0)
	return codewords


def generate(message, version, encoding):
	size = 21 + 4 * (version - 1)
	matrix = Matrix(size)
	matrix.setup()
	correct = verify(message, version, encoding)

	try:
		codewords = get_codewords(message, version, encoding)
		matrix.put_codewords(codewords)
	finally:
		if matrix == correct:
			matrix.disp()
			print('Correct!')
		else:
			(matrix ^ correct).disp()
			print('Incorrect! Diff displayed.')


generate(' '.join(sys.argv[1:]), 5, 'b')
