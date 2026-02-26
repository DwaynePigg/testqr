GF_EXP = [0] * 512
GF_LOG = [0] * 256

def _build_gf():
    x = 1
    for i in range(255):
        GF_EXP[i] = x
        GF_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11d
    for i in range(255, 512):
        GF_EXP[i] = GF_EXP[i - 255]

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

print(bin(format_bits(1, 0)))