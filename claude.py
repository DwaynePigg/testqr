#!/usr/bin/env python3
"""
Minimal Version 4-L QR Code generator (no QR libraries).
Outputs the 33x33 matrix as binary (0/1) to stdout.

Usage: python3 qr_v4l.py "YOUR TEXT"
"""

import sys

# ---------------------------------------------------------------------------
# Reed-Solomon GF(256) arithmetic (primitive polynomial x^8+x^4+x^3+x^2+1 = 0x11d)
# ---------------------------------------------------------------------------
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


def gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return GF_EXP[GF_LOG[a] + GF_LOG[b]]


# def gf_poly_mul(p, q):
    # r = [0] * (len(p) + len(q) - 1)
    # for i, pi in enumerate(p):
        # for j, qj in enumerate(q):
            # r[i + j] ^= gf_mul(pi, qj)
    # return r

# def rs_generator_poly(n):
    # g = [1]
    # for i in range(n):
        # g = gf_poly_mul(g, [1, GF_EXP[i]])
    # return g

# def rs_encode(data, n_ec):
    # gen = rs_generator_poly(n_ec)
    # msg = list(data) + [0] * n_ec
    # for i in range(len(data)):
        # if msg[i] == 0:
            # continue
        # coef = msg[i]
        # for j, g in enumerate(gen):
            # msg[i + j] ^= gf_mul(coef, g)
    # return msg[len(data):]
	

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
    ecc = [*data, *([0] * n_ecc)]
    for i, b in enumerate(data):
        if b == 0:
            continue
        for j, g in enumerate(RS_GEN_20):
            msg[i + j] ^= gf_mul(b, g)
    return msg[len(data):]


# ---------------------------------------------------------------------------
# Version 4-L parameters
# VERSION = 4, EC = L
# Data codewords: 80, EC codewords: 20 (single block)
# ---------------------------------------------------------------------------
VERSION = 4
SIZE = 17 + VERSION * 4  # = 33

# Byte mode capacity for V4-L: 50 bytes max
MAX_DATA_BYTES = 50
N_DATA_CODEWORDS = 80
N_EC_CODEWORDS = 20

# ---------------------------------------------------------------------------
# Encode data into codewords (byte mode)
# ---------------------------------------------------------------------------
def encode_data(text):
    data = text.encode('iso-8859-1')
    if len(data) > MAX_DATA_BYTES:
        raise ValueError(f"Text too long for V4-L (max {MAX_DATA_BYTES} bytes)")

    bits = []

    def add_bits(val, n):
        for i in range(n - 1, -1, -1):
            bits.append((val >> i) & 1)

    # Mode indicator: byte mode = 0100
    add_bits(0b0100, 4)
    # Character count: 8 bits for byte mode V4
    add_bits(len(data), 8)
    # Data bytes
    for byte in data:
        add_bits(byte, 8)
    # Terminator
    add_bits(0, min(4, N_DATA_CODEWORDS * 8 - len(bits)))
    # Pad to byte boundary
    while len(bits) % 8:
        bits.append(0)
    # Pad codewords
    pad_bytes = [0xEC, 0x11]
    i = 0
    while len(bits) < N_DATA_CODEWORDS * 8:
        add_bits(pad_bytes[i % 2], 8)
        i += 1

    # Convert bits to bytes
    codewords = []
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i + 8]:
            byte = (byte << 1) | b
        codewords.append(byte)
    return codewords

# ---------------------------------------------------------------------------
# Build the full data + EC codeword sequence
# ---------------------------------------------------------------------------
def build_codewords(text):
    data_cw = encode_data(text)
    ec_cw = rs_encode(data_cw, N_EC_CODEWORDS)
    return data_cw + ec_cw

# ---------------------------------------------------------------------------
# Matrix building
# ---------------------------------------------------------------------------
def make_matrix(size):
    return [[None] * size for _ in range(size)]

def place_finder(matrix, row, col):
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
            matrix[row + r][col + c] = pattern[r][c]

def place_separators(matrix, size):
    # Horizontal separators
    for c in range(8):
        matrix[7][c] = 0
        matrix[size - 8][c] = 0
        matrix[7][size - 1 - c] = 0
    # Vertical separators
    for r in range(8):
        matrix[r][7] = 0
        matrix[size - 1 - r][7] = 0
        matrix[r][size - 8] = 0

def place_alignment(matrix):
    # V4 has one alignment pattern at (26, 26) (center coords)
    cr, cc = 26, 26
    for dr in range(-2, 3):
        for dc in range(-2, 3):
            m = max(abs(dr), abs(dc))
            matrix[cr + dr][cc + dc] = 1 if m == 2 or m == 0 else 0

def place_timing(matrix, size):
    for i in range(8, size - 8):
        val = 1 if i % 2 == 0 else 0
        matrix[6][i] = val
        matrix[i][6] = val

def place_dark_module(matrix):
    matrix[SIZE - 8][8] = 1

def reserve_format_areas(matrix, size):
    # Reserve format info areas with sentinel 2 so data placement skips them.
    # Top-left: row 8 cols 0-8, col 8 rows 0-8
    for i in range(9):
        if matrix[8][i] is None:
            matrix[8][i] = 2
        if matrix[i][8] is None:
            matrix[i][8] = 2
    # Top-right: row 8, cols size-7 to size-1 (7 bits)
    for i in range(size - 7, size):
        if matrix[8][i] is None:
            matrix[8][i] = 2
    # Bottom-left: col 8, rows size-7 to size-1 (7 bits)
    for i in range(size - 7, size):
        if matrix[i][8] is None:
            matrix[i][8] = 2

def is_function(matrix, r, c):
    return matrix[r][c] is not None

def place_data(matrix, codewords, size):
    bits = []
    for cw in codewords:
        for i in range(7, -1, -1):
            bits.append((cw >> i) & 1)

    bit_idx = 0
    # Columns in pairs from right to left, skipping col 6
    col = size - 1
    going_up = True
    while col > 0:
        if col == 6:
            col -= 1
            continue
        cols = [col, col - 1]
        rows = range(size - 1, -1, -1) if going_up else range(size)
        for r in rows:
            for c in cols:
                if not is_function(matrix, r, c):
                    if bit_idx < len(bits):
                        matrix[r][c] = bits[bit_idx]
                        bit_idx += 1
                    else:
                        matrix[r][c] = 0
        col -= 2
        going_up = not going_up

# ---------------------------------------------------------------------------
# Masking
# ---------------------------------------------------------------------------
MASK_CONDITIONS = [
    lambda r, c: (r + c) % 2 == 0,
    lambda r, c: r % 2 == 0,
    lambda r, c: c % 3 == 0,
    lambda r, c: (r + c) % 3 == 0,
    lambda r, c: (r // 2 + c // 3) % 2 == 0,
    lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
    lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
    lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
]

def apply_mask(matrix, mask_id, size):
    cond = MASK_CONDITIONS[mask_id]
    result = [row[:] for row in matrix]
    for r in range(size):
        for c in range(size):
            if result[r][c] in (0, 1) and not is_function_module(r, c, size):
                if cond(r, c):
                    result[r][c] ^= 1
    return result

def is_function_module(r, c, size):
    # Finder patterns + separators (9x9 corners)
    if r < 9 and c < 9: return True
    if r < 9 and c >= size - 7: return True
    if r >= size - 7 and c < 9: return True
    # Timing
    if r == 6 or c == 6: return True
    # Alignment pattern (V4): centered at 26,26, radius 2
    if 24 <= r <= 28 and 24 <= c <= 28: return True
    # Dark module
    if r == size - 8 and c == 8: return True
    return False

def penalty(matrix, size):
    score = 0
    # Rule 1: 5+ in a row
    for row in matrix:
        count = 1
        for i in range(1, size):
            if row[i] == row[i-1]:
                count += 1
            else:
                if count >= 5: score += count - 2
                count = 1
        if count >= 5: score += count - 2
    for c in range(size):
        count = 1
        for r in range(1, size):
            if matrix[r][c] == matrix[r-1][c]:
                count += 1
            else:
                if count >= 5: score += count - 2
                count = 1
        if count >= 5: score += count - 2
    # Rule 2: 2x2 blocks
    for r in range(size - 1):
        for c in range(size - 1):
            v = matrix[r][c]
            if v == matrix[r][c+1] == matrix[r+1][c] == matrix[r+1][c+1]:
                score += 3
    # Rule 3: specific patterns
    pat1 = [1,0,1,1,1,0,1,0,0,0,0]
    pat2 = [0,0,0,0,1,0,1,1,1,0,1]
    for row in matrix:
        for i in range(size - 10):
            if list(row[i:i+11]) in (pat1, pat2): score += 40
    for c in range(size):
        col = [matrix[r][c] for r in range(size)]
        for i in range(size - 10):
            if col[i:i+11] in (pat1, pat2): score += 40
    # Rule 4
    total = size * size
    dark = sum(sum(row) for row in matrix)
    pct = dark * 100 // total
    prev5 = pct - pct % 5
    next5 = prev5 + 5
    score += min(abs(prev5 - 50), abs(next5 - 50)) * 2
    return score

# ---------------------------------------------------------------------------
# Format information (EC=L=01, mask=best)
# ---------------------------------------------------------------------------
FORMAT_INFO = {
    # (EC_indicator, mask): format_string (15 bits, MSB first)
    # EC L = 01
}

def format_bits(ec_indicator, mask_id):
    # 5-bit data: ec(2) | mask(3)
    data = (ec_indicator << 3) | mask_id
    # Generator polynomial: x^10 + x^8 + x^5 + x^4 + x^2 + x + 1 = 0b10100110111
    gen = 0b10100110111
    remainder = data << 10
    for i in range(4, -1, -1):
        if remainder & (1 << (i + 10)):
            remainder ^= gen << i
    bits_15 = (data << 10) | remainder
    # XOR mask 101010000010010
    bits_15 ^= 0b101010000010010
    return bits_15

def place_format_info(matrix, mask_id, size):
    bits = format_bits(0b01, mask_id)  # EC=L=01
    # Top-left: row 8 (cols 0-5, skip 6, col 7 skipped for separator, col 8)
    # and col 8 (rows 7 down to 0, skipping row 6)
    # Standard QR format placement:
    # Sequence of 15 bits placed at specific (row,col) positions
    positions_tl = [
        (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,7),(8,8),
        (7,8),(5,8),(4,8),(3,8),(2,8),(1,8),(0,8)
    ]
    for i, (r, c) in enumerate(positions_tl):
        matrix[r][c] = (bits >> (14 - i)) & 1
    # Top-right: row 8, cols size-1 down to size-7 (7 bits, b0..b6)
    for i in range(7):
        matrix[8][size - 1 - i] = (bits >> i) & 1
    # Bottom-left: col 8, rows size-7 to size-1 (7 bits, b0..b6)
    for i in range(7):
        matrix[size - 7 + i][8] = (bits >> i) & 1

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def generate_qr(text):
    codewords = build_codewords(text)

    # Build base matrix with function patterns
    matrix = make_matrix(SIZE)
    place_finder(matrix, 0, 0)
    place_finder(matrix, 0, SIZE - 7)
    place_finder(matrix, SIZE - 7, 0)
    place_separators(matrix, SIZE)
    place_alignment(matrix)
    place_timing(matrix, SIZE)
    place_dark_module(matrix)
    reserve_format_areas(matrix, SIZE)

    # Place data bits
    place_data(matrix, codewords, SIZE)

    # Try all 8 masks, pick best
    best_matrix = None
    best_score = float('inf')
    best_mask = 0

    for mask_id in range(8):
        m = apply_mask(matrix, mask_id, SIZE)
        # Place format info
        place_format_info(m, mask_id, SIZE)
        s = penalty(m, SIZE)
        if s < best_score:
            best_score = s
            best_matrix = m
            best_mask = mask_id

    return best_matrix

def print_qr(matrix):
    for row in matrix:
        print(''.join(str(v) for v in row))

if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello, World!"
    matrix = generate_qr(text)
    print_qr(matrix)