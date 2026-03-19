import math

L1 = []
L = 0  


def fPart(num):
	return num - math.trunc(num)


def put(N, S):
	global L1, L
	
	R = S
	O = 8*fPart(L/8)
	if O!=0:
		T = min([8-O,R])
		Ans = 2**T
		L1[-1] += Ans*fPart(int(N/2**(R-T))/Ans)*2**(8-O-T)
		R = R-T

	while R>=8:
		L1.append(256*fPart(int(N/2**(R-8))/256))
		R = R-8

	if R>0:
		Ans = 2**R
		L1.append(Ans*fPart(N/Ans)*2**(8-R))

	L = L+S


put(2, 4)
put(15, 9)
put(479, 11)
put(1315, 11)
print(L1)
print(' '.join(f"{round(b):02X}" for b in L1))
# 20 79 DF A4 68 C3 2F 53 D4 A7 6D E6 00