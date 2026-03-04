import string

from collections import deque
from itertools import batched, chain

from rsconst import *

import qrcodegen as nayuki


def verify(message, version, encoding):
	if encoding == 'b':
		seg = nayuki.QrSegment.make_bytes(message)
	elif encoding == 'a':
		seg = nayuki.QrSegment.make_alphanumeric(message.decode('ascii'))
	else:
		raise ValueError(encoding)
	
	nayuki_qr = nayuki.QrCode.encode_segments([seg], nayuki.QrCode.Ecc.LOW, minversion=version, maxversion=version, mask=0, boostecl=False)
	size = nayuki_qr.get_size()
	
	qr = QrCode(version)
	for j in range(size):
		for i in range(size):
			qr.pxl_on(i, j, nayuki_qr.get_module(j, i))  # nayuki flips i/j

	return qr


ALPHANUMERIC = (string.digits + string.ascii_uppercase + ' $%*+-./:').encode('ascii')
AN_TABLE = { a: i for i, a in enumerate(ALPHANUMERIC) }

FORMAT_L0 = 0b111011111000100

VERSION_INFO = [
	0b000111110010010100,
	0b001000010110111100,
	0b001001101010011001,
	0b001010010011010011,
	0b001011101111110110,
]


def skip_alignment(i, j, align_i, align_j):
	return abs(i - align_i) <= 2 and abs(j - align_j) <= 2


class QrCode:

	def __init__(self, version):
		self.version = version
		self.size = 21 + 4 * (version - 1)
		self.matrix = tuple(bytearray(self.size) for _ in range(self.size))
		if version == 1:
			self.skip = self.skip1
		elif version < 7:
			self.skip = self.skip2
		elif version <= 14:
			self.skip = self.skip7
		else:
			raise ValueError(version)

	def pxl_on(self, i, j, state=1):
		if not (0 <= i < self.size) or not (0 <= j < self.size):
			raise ValueError(i, j)
		self.matrix[i][j] = state

	def disp(self):
		print('▒' * (self.size + 4))
		for row1, row2 in batched(chain(self.matrix, [(0 for _ in range(self.size))]), 2):
			print('▒▒', end='')
			for px1, px2 in zip(row1, row2, strict=True):
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
		for r in range(0, 5):
			for c in range(0, 5):
				self.pxl_on(i + r - 2, j + c - 2, pattern[r][c])

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
	
	def put_version_info(self):
		bits = VERSION_INFO[self.version - 7]
		for i in range(18):
			b = (bits >> i) & 1
			self.pxl_on(self.size - 11 + (i % 3), i // 3, b)
			self.pxl_on(i // 3, self.size - 11 + (i % 3), b)
	
	def setup(self):
		self.put_position(0, 0)
		self.put_position(0, self.size - 7)
		self.put_position(self.size - 7, 0)
		if self.version != 1:
			self.put_alignment(self.size - 7, self.size - 7)
		if self.version > 6:
			middle = 6 + (self.size - 13) // 2
			self.put_alignment(6, middle)
			self.put_alignment(middle, 6)
			self.put_alignment(middle, middle)
			self.put_alignment(middle, self.size - 7)
			self.put_alignment(self.size - 7, middle)
			self.put_version_info()
		self.put_timing()
		self.put_format()

	def top_row(self, j):
		return 9 if j < 9 or j > self.size - 9 else 0

	def bottom_row(self, j):
		return self.size - 9 if j < 9 else self.size - 1

	def skip1(self, i, j):
		return i == 6

	def skip2(self, i, j):	
		return i == 6 or skip_alignment(i, j, self.size - 7, self.size - 7)

	def skip7(self, i, j):
		middle = 6 + (self.size - 13) // 2
		return (
			i == 6
			or skip_alignment(i, j, 6, middle)
			or skip_alignment(i, j, middle, 6)
			or skip_alignment(i, j, middle, middle)
			or skip_alignment(i, j, middle, self.size - 7)
			or skip_alignment(i, j, self.size - 7, middle)
			or skip_alignment(i, j, self.size - 7, self.size - 7)
			or self.size - 11 <= i <= self.size - 9 and 0 <= j <= 5
			or self.size - 11 <= j <= self.size - 9 and 0 <= i <= 5
		)

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
		return isinstance(other, QrCode) and self.matrix == other.matrix
	
	def __xor__(self, other):
		if not isinstance(other, QrCode) or self.size != other.size:
			raise ValueError(other)
			
		x = QrCode(self.version)
		for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix, strict=True)):
			for j, (col1, col2) in enumerate(zip(row1, row2, strict=True)):
				x.pxl_on(i, j, col1 ^ col2)
		return x
	
	def __repr__(self):
		return f"QrCode version {self.version} ({self.size}x{self.size})"


def mask0(i, j):
	return (i + j) % 2 == 0


global_xor = 0


def get_ecc_bytes(data, rs_poly):
	global global_xor
	n_ecc = len(rs_poly)
	ecc = [0] * n_ecc
	for r, b in enumerate(data):
		offset = r % n_ecc
		factor = b ^ ecc[offset]
		global_xor += 1
		ecc[offset] = 0
		if factor != 0:
			for i, coef in enumerate(rs_poly):
				ecc[(i + r + 1) % n_ecc] ^= GF256_EXP[(GF256_LOG[coef] + GF256_LOG[factor]) % 255]
				global_xor += 1

	return bytes(ecc)


def get_ecc_bytes(data, rs_poly, blocks=1):
	global global_xor
	n_ecc = len(rs_poly) // blocks
	ecc = deque(0 for _ in range(n_ecc))
	for b in data:
		factor = b ^ ecc[0]
		global_xor += 1
		ecc[0] = 0
		ecc.rotate(-1)
		if factor != 0:
			for i, coef in enumerate(rs_poly):
				ecc[i % n_ecc] ^= GF256_EXP[(GF256_LOG[coef] + GF256_LOG[factor]) % 255]
				global_xor += 1

	return bytes(ecc)


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

	def binary(self, message, version):
		self.put(4, 4)
		self.put(len(message), 8 if version < 10 else 16)
		for m in message:
			self.put(m)
	
	def alphanumeric(self, message, version):
		self.put(2, 4)
		self.put(len(message), 9 if version < 10 else 11)
		for pair in batched(message, 2):
			if len(pair) == 2:
				c1, c2 = pair
				self.put(45 * AN_TABLE[c1] + AN_TABLE[c2], 11)
			else:
				(c1,) = pair
				self.put(AN_TABLE[c1], 6)


BIT_LENGTH = [152, 272, 440, 640, 864, 1088, 1248, 1552, 1856, 2192, 2592]


def zip_skip(*iterables):
	iterators = [iter(i) for i in iterables]
	while True:
		values = []
		for it in iterators:
			try:
				value = next(it)
			except StopIteration:
				pass
			else:
				values.append(value)

		if not values:
			return

		yield tuple(values)


def interleave(blocks, rs_poly):
	codewords = bytearray()
	for col in zip_skip(*blocks):
		codewords.extend(col)
	for col in zip(*(get_ecc_bytes(block, rs_poly) for block in blocks), strict=True):
		codewords.extend(col)
	return codewords


def get_codewords(message, version, encoding):
	buffer = BitBuffer()
	if not callable(encoding):
		encoding = {
			'b': BitBuffer.binary,
			'a': BitBuffer.alphanumeric,
		}[encoding]
	encoding(buffer, message, version)
	data = buffer.buffer

	max_bits = BIT_LENGTH[version - 1]
	if buffer.bit_length > max_bits:
		raise ValueError(f"bits: {buffer.bit_length}; max {max_bits}")
	
	buffer.put(0, min(4, max_bits - buffer.bit_length))

	for f in range(0, max_bits // 8 - len(data)):
		data.append([0xEC, 0x11][f % 2])
	
	print(' '.join(f"{b:02X}" for b in data))
	
	rs_poly = RS_POLY[version]
	
	if version < 6:
		data.extend(get_ecc_bytes(data, RS_POLY[version]))
		codewords = data
	elif version == 10:
		codewords = interleave([data[:68], data[68:136], data[136:205], data[205:]], rs_poly)
	elif version == 11:
		q = len(data) // 4
		codewords = interleave([data[:q], data[q:2*q], data[2*q:3*q], data[3*q:]], rs_poly)		
	elif version < 11:
		h = len(data) // 2
		codewords = interleave([data[:h], data[h:]], rs_poly)
	else:
		raise ValueError(version)
	
	codewords.append(0)
	return codewords


def generate(message, version, encoding):
	qr = QrCode(version)	
	qr.setup()
	try:
		codewords = get_codewords(message, version, encoding)
		qr.put_codewords(codewords)
	finally:
		correct = verify(message, version, encoding)
		if qr == correct:
			qr.disp()
			print('Correct!')
		else:
			(qr ^ correct).disp()
			print('Incorrect! Diff displayed.')
		print('xor', global_xor)


if __name__ == '__main__':
	import argparse
	from bisect import bisect_left
	from pathlib import Path

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', type=Path)
	parser.add_argument('-v', '--version', type=int)
	parser.add_argument('-e', '--encoding')
	args, tokens = parser.parse_known_args()
	
	if tokens and args.input:
		parser.error(f"Received input file and message args")
	
	if args.input:
		with open(args.input, 'rb') as f:
			message = f.read()
	else:
		message = ' '.join(tokens).encode('utf-8')
		
	version = args.version
	encoding = args.encoding
	if encoding is None:
		a_set = frozenset(ALPHANUMERIC)
		# all(0x7fffffe07ffec3100000000 & (1<<ord(a)) for a in message)
		encoding = 'a' if all(a in a_set for a in message) else 'b'

	if version is None:
		b_length = [17, 32, 53,  78, 106, 134, 154, 192, 230, 271, 321]
		a_length = [25, 47, 77, 114, 154, 195, 224, 279, 335, 395, 468]
		table = a_length if encoding == 'a' else b_length
		index = bisect_left(table, len(message))
		if index == len(table):
			parser.error(f"Message too long ({len(message)})")
		version = index + 1
	
	generate(message, version, encoding)
