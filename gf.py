GF_EXP = [0] * 256
GF_LOG = [0] * 256

def _build_gf():
	x = 1
	for i in range(255):
		GF_EXP[i] = x
		GF_LOG[x] = i
		x <<= 1
		if x & 0x100:
			x ^= 0x11d

_build_gf()

def format_bits(ec_indicator, mask_id):
	data = (ec_indicator << 3) | mask_id
	gen = 0b10100110111
	remainder = data << 10
	for i in range(4, -1, -1):
		if remainder & (1 << (i + 10)):
			remainder ^= gen << i
	bits_15 = (data << 10) | remainder
	bits_15 ^= 0b101010000010010
	return bits_15



def gf_mul(a, b):
	if a == 0 or b == 0:
		return 0
	return GF_EXP[(GF_LOG[a] + GF_LOG[b]) % 256]


RS_GEN_20 = [
	227, 213, 211, 174,  18,  70,  38, 238, 
	158, 126, 236,  85, 241, 193, 107,  46, 
	112, 222, 209,  56,   1
]

def rs_encode(data, n_ec=20):
	msg = list(data) + [0] * n_ec
	for i in range(len(data)):
		if msg[i] == 0:
			continue
		coef = msg[i]
		for j, g in enumerate(RS_GEN_20):
			msg[i + j] ^= gf_mul(coef, g)
	return msg[len(data):]
	

def get_ecc_bytes(data, n_ecc=20):
	ecc = [*data, *[0] * n_ecc]
	for i in range(len(data)):
		coef = ecc[i]
		if coef != 0:
			for j, g in enumerate(RS_GEN_20):
				ecc[i + j] ^= GF_EXP[(GF_LOG[coef] + GF_LOG[g]) % 256]

	return ecc[len(data):]


data = 'HELLO WORLD!'.encode('utf-8')
print(rs_encode(data))
print(get_ecc_bytes(data))
