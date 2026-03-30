from itertools import batched
import qrcodegen as nayuki

REPLACE = str.maketrans("?;',!", "$%*+/")


def print_screen(screen):
	print('▒' * 100)
	for row1, row2 in batched(screen, 2):
		print('▒▒', end='')
		for px1, px2 in zip(row1, row2, strict=True):
			print(' ▀▄█'[~(px1 | (px2 << 1))], end='')
		print('▒▒')
	print('▒' * 100)


def verify(message, version, mode, test_codewords, test_screen):
	if mode in {1, 'a', 'alphanumeric'}:
		seg = nayuki.QrSegment.make_alphanumeric(message.translate(REPLACE))
	elif mode in {0, 'b', 'binary'}:
		seg = nayuki.QrSegment.make_bytes(message.encode('ascii'))
	else:
		raise ValueError(mode)
	
	screen = tuple(bytearray(96) for _ in range(64))
	nayuki_qr = nayuki.QrCode.encode_segments([seg], nayuki.QrCode.Ecc.LOW, minversion=version, maxversion=version, mask=0, boostecl=False)
	size = nayuki_qr.get_size()

	for j in range(size):
		for i in range(size):
			if nayuki_qr.get_module(j, i):
				screen[i][j] = 1
	
	codewords = list(nayuki_qr.codewords)
	if len(codewords) == len(test_codewords) - 1 and test_codewords[-1] == 0:
		test_codewords = test_codewords[:-1]
	
	if codewords == test_codewords:
		print('CODEWORDS CORRECT')
	else:
		print('!!!CODEWORDS INCORRECT!!!')
		print('Expected:')
		print(codewords)
		print('Actual:')
		print(test_codewords)
	
	if screen == test_screen:
		print('SCREEN CORRECT')
	else:
		print('!!!SCREEN INCORRECT!!!')
		print('Continue for actual')
		input()
		print_screen(screen)
		print('Continue for diff')
		input()
		diff = tuple(bytearray(96) for _ in range(64))
		for i in range(64):
			for j in range(96):
				diff[i][j] = int(screen[i][j] ^ test_screen[i][j])
		print_screen(diff)
