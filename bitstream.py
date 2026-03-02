import string

ALPHANUMERIC = string.digits + string.ascii_uppercase + " $%*+-./:"
LOOKUP = { a: i for i, a in enumerate(ALPHANUMERIC) }

class Bitstream:

	def __init__(self):
		self.buffer = bytearray()
		self.bit_length = 0

	def put(self, n, size=8):
		for i in range(size - 1, -1, -1):
			bit = int(n / (2 ** i)) % 2
			if self.bit_length % 8 == 0:
				self.buffer.append(0)
			if bit:
				self.buffer[-1] += 2 ** (7 - self.bit_length % 8)
			self.bit_length += 1
			


bs = Bitstream()
bs.put(4, 4)
bs.put(0xEC)
bs.put(0x11)
bs.put(1, 4)
print(' '.join(f"{b:02X}" for b in bs.buffer))
