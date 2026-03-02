def pxl_on(i, j, state):
	if state:
		print(f"Pxl-On({i}, {j})")


def put_format(bits=0b111011111000100, size=33):
	for a in range(6):
		pxl_on(a, 8, (bits >> a) & 1)

	pxl_on(7, 8, (bits >> 6) & 1)
	pxl_on(8, 8, (bits >> 7) & 1)
	pxl_on(8, 7, (bits >> 8) & 1)

	for a in range(6):
		pxl_on(8, 5 - a, (bits >> 9 + a) & 1)

	for a in range(8):
		pxl_on(8, size - 1 - a, (bits >> a) & 1)

	for a in range(7):
		pxl_on(size - 7 + a, 8, (bits >> 8 + a) & 1)

put_format()