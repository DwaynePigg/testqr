import argparse
import builtins
parser = argparse.ArgumentParser()
parser.add_argument('-v', default=0, type=builtins.int)
parser.add_argument('-m', default="ATTACK AT DAWN")
parser.add_argument('-e', default=1, type=builtins.int)
args = parser.parse_args()

from tisetup import *


# L1 = seq(range(16))
# print(L1)

# Q=dim(L1)/4

# L1 = seq(
	# not_(fPart(N))*L1[int(N)]
	# +(fPart(N)==.25)*L1[Q+int(N)]
	# +(fPart(N)==.5)*L1[2*Q+int(N)]
	# +(fPart(N)==.75)*L1[3*Q+int(N)]
	# for N in For(1,Q+.75,.25)
# )

# # L1 = seq(not_(fPart(I/2))*L1[int(I/2)]+2*fPart(I/2)*L1[H+int(I/2)] for I in For(2,1+dim(L1)))
# # L1 = seq((fPart(I/2)==0)*L1[int(I/2)]+(fPart(I/2)==.5)*L1[H+int(I/2)] for I in For(2,1+dim(L1)))

# print(L1)

# Stop()



Str1 = args.m
E = args.e
V = args.v

if not_(V):
	if E:
		# Alphanumeric Mode
		Ans = L_[25,47,77,114,154,195,224,279,335,395,468]
	else:
		Ans = L_[17,32,53,78,106,134,154,192,230,271,321]

	V = 1+sum(Ans<length(Str1))

if V>11:
	Disp("Message too long")
	Stop()

print('Version:', V)

L_GFL = L_[0,1,25,2,50,26,198,3,223,51,238,27,104,199,75,4,100,224,14,52,141,239,129,28,193,105,248,200,8,76,113,5,138,101,47,225,36,15,33,53,147,142,218,240,18,130,69,29,181,194,125,106,39,249,185,201,154,9,120,77,228,114,166,6,191,139,98,102,221,48,253,226,152,37,179,16,145,34,136,54,208,148,206,143,150,219,189,241,210,19,92,131,56,70,64,30,66,182,163,195,72,126,110,107,58,40,84,250,133,186,61,202,94,155,159,10,21,121,43,78,212,229,172,115,243,167,87,7,112,192,247,140,128,99,13,103,74,222,237,49,197,254,24,227,165,153,119,38,184,180,124,17,68,146,217,35,32,137,46,55,63,209,91,149,188,207,205,144,135,151,178,220,252,190,97,242,86,211,171,20,42,93,158,132,60,57,83,71,109,65,162,31,45,67,216,183,123,164,118,196,23,73,236,127,12,111,246,108,161,59,82,41,157,85,170,251,96,134,177,187,204,62,90,203,89,95,176,156,169,160,81,11,245,22,235,122,117,44,215,79,174,213,233,230,231,173,232,116,214,244,234,168,80,88,175]  # original list is undefined at 0. I removed element 0 here, so this list is kind of 0-indexed now
L_GFX = L_[1,2,4,8,16,32,64,128,29,58,116,232,205,135,19,38,76,152,45,90,180,117,234,201,143,3,6,12,24,48,96,192,157,39,78,156,37,74,148,53,106,212,181,119,238,193,159,35,70,140,5,10,20,40,80,160,93,186,105,210,185,111,222,161,95,190,97,194,153,47,94,188,101,202,137,15,30,60,120,240,253,231,211,187,107,214,177,127,254,225,223,163,91,182,113,226,217,175,67,134,17,34,68,136,13,26,52,104,208,189,103,206,129,31,62,124,248,237,199,147,59,118,236,197,151,51,102,204,133,23,46,92,184,109,218,169,79,158,33,66,132,21,42,84,168,77,154,41,82,164,85,170,73,146,57,114,228,213,183,115,230,209,191,99,198,145,63,126,252,229,215,179,123,246,241,255,227,219,171,75,150,49,98,196,149,55,110,220,165,87,174,65,130,25,50,100,200,141,7,14,28,56,112,224,221,167,83,166,81,162,89,178,121,242,249,239,195,155,43,86,172,69,138,9,18,36,72,144,61,122,244,245,247,243,251,235,203,139,11,22,44,88,176,125,250,233,207,131,27,54,108,216,173,71,142]

L_RS7 = L_[127,122,154,164,11,68,117]
L_RS10 = L_[216,194,159,111,199,94,95,113,157,193]
L_RS15 = L_[29,196,111,163,112,74,10,105,105,139,132,151,32,134,26]
L_RS18 = L_[239,251,183,113,149,175,199,215,240,220,73,82,173,75,32,67,217,146]
L_RS20 = L_[152,185,240,5,111,99,6,220,112,150,69,36,187,22,228,198,121,121,165,174]
L_RS24 = L_[122,118,169,70,178,237,216,102,115,150,229,73,130,72,61,43,206,1,237,247,127,217,144,117]
L_RS26 = L_[246,51,183,4,136,98,199,152,77,56,206,24,145,40,209,117,233,42,135,68,70,144,146,77,43,94]
L_RS30 = L_[212,246,77,73,195,192,75,98,5,70,103,177,22,217,138,51,181,246,72,25,18,46,228,74,216,195,11,106,130,150]

if V==1:
	M = 152
	L2 = L_RS7
elif V==2:
	M = 272
	L2 = L_RS10
elif V==3:
	M = 440
	L2 = L_RS15
elif V==4:
	M = 640
	L2 = L_RS20
elif V==5:
	M = 864
	L2 = L_RS26
elif V==6:
	M = 1088
	L2 = L_RS18
elif V==7:
	M = 1248
	L2 = L_RS20
elif V==8:
	M = 1552
	L2 = L_RS24
elif V==9:
	M = 1856
	L2 = L_RS30
elif V==10:
	M = 2192
	L2 = L_RS18
elif V==11:
	M = 2592
	L2 = L_RS20


################
################
################

def prgmBITBEF():
	global L, L_CW, N, S
	for I in For(S-1,0,-1):
		B = 2*fPart(int(N/(2**I))/2)
		if not_(fPart(L/8)):
			L_CW[1+dim(L_CW)] = 0
		if B:
			L_CW[dim(L_CW)] = L_CW[dim(L_CW)]+2**(7-8*fPart(L/8))
		L = L + 1


def prgmBITBUF():
	global L, L_CW, N, S
	R = S
	# WHICH ONE???
	O = 8*fPart(L/8)
	O = L-8*int(L/8)
	if O:
		T = min(L_[8-O,R])
		L_CW[dim(L_CW)] = L_CW[dim(L_CW)]+2**T*fPart(int(N/2**(R-T))/2**T)*2**(8-O-T)
		R = R-T

	while R>=8:
		L_CW[1+dim(L_CW)] = 256*fPart(int(N/2**(R-8))/256)
		R = R-8

	if R>0:
		L_CW[1+dim(L_CW)] = 256*fPart(N/2**R)

	L = L+S

if E:

	#                                            $%*+-./:
	Str2 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ?;',-.!:"
	L = 4
	L_CW = L_[32]
	S = 9+2*(V>=10)
	N = length(Str1)
	prgmBITBUF()

	S = 11
	for I in For(1,length(Str1)-1,2):
		N = -46+45*max(L_[1,inString(Str2,sub(Str1,I,1))])+max(L_[1,inString(Str2,sub(Str1,I+1,1))])
		prgmBITBUF()

	if fPart(length(Str1)/2):
		S = 6
		N = -1+max(L_[1,inString(Str2,sub(Str1,length(Str1),1))])
		prgmBITBUF()

	# Could call BITBUF here but we can cheat
	S = min(L_[4,M-L])
	if S<=8*fPart((L-1)/8):
		L_CW[1+dim(L_CW)] = 0

else:

	Str2 = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
	L = 4
	L_CW = L_[64]
	S = 8+8*(V>=10)
	N = length(Str1)
	prgmBITBUF()
	O = S/8
	for I in For(1,length(Str1)):
		N = 31+max(L_[1,inString(Str2,sub(Str1,I,1))])
		L_CW[O+I] = int(N/16)+L_CW[O+I]
		L_CW[O+I+1] = 256*fPart(N/16)

	# Don't need to explicitly write terminator


for F in For(1,int(M/8)-dim(L_CW)):
	L_CW[1+dim(L_CW)] = 236-219*not_(fPart(F/2))

print('MSG:', L_CW)

L3 = seq(2 ** I for I in For(8,1,-1))  # Powers of 2 for fast XOR

def prgmQRECC():
	global L_CW, L1, L2, L3, M, N
	L1 = L_[()] # DelVar L1
	set_dim(L1, dim(L2))  # ECC buffer
	for I in For(M,N):
		B = L_CW[I]
		F = .5*sum(L3*(1==abs(int(2*fPart(complex(L1[1],B)/L3)))))
		L1 = delta_list(cumSum(L1))
		L1[1 + dim(L1)] = 0
		for J in For(1,(F!=0)*dim(L2)):
			Ans = L_GFL[L2[J]] + L_GFL[F]
			L1[J] = .5*sum(L3*(1==abs(int(2*fPart(complex(L1[J],L_GFX[1+Ans-255*(Ans>254)])/L3)))))

if V<=5:
	M = 1
	N = dim(L_CW)
	prgmQRECC()
	L_CW = augment(L_CW,L1)
elif V==10:
	M = 1
	N = 68
	prgmQRECC()
	L4 = L1.copy()
	M = 69
	N = 136
	prgmQRECC()
	L5 = L1.copy()
	M = 137
	N = 205
	prgmQRECC()
	L6 = L1.copy()
	M = 206
	N = 274
	prgmQRECC()
	L_CW = augment(
		seq(
			not_(fPart(N))*L_CW[int(N)]
			+(fPart(N)==.25)*L_CW[68+int(N)]
			+(fPart(N)==.5)*L_CW[136+int(N)]
			+(fPart(N)==.75)*L_CW[205+int(N)]
			for N in For(1,68.75,.25)
		), augment(
			L_[L_CW[205], L_CW[274]],
			seq(
				not_(fPart(N))*L4[int(N)]
				+(fPart(N)==.25)*L5[int(N)]
				+(fPart(N)==.5)*L6[int(N)]
				+(fPart(N)==.75)*L1[int(N)]
				for N in For(1,dim(L1)+.75,.25)
			)
		)
	)
elif V==11:
	M = 1
	N = 81
	prgmQRECC()
	L4 = L1.copy()
	M = 82
	N = 162
	prgmQRECC()
	L5 = L1.copy()
	M = 163
	N = 243
	prgmQRECC()
	L6 = L1.copy()
	M = 244
	N = 324
	prgmQRECC()
	L_CW = augment(
		seq(
			not_(fPart(N))*L_CW[int(N)]
			+(fPart(N)==.25)*L_CW[81+int(N)]
			+(fPart(N)==.5)*L_CW[162+int(N)]
			+(fPart(N)==.75)*L_CW[243+int(N)]
			for N in For(1,81.75,.25)
		),
		seq(
			not_(fPart(N))*L4[int(N)]
			+(fPart(N)==.25)*L5[int(N)]
			+(fPart(N)==.5)*L6[int(N)]
			+(fPart(N)==.75)*L1[int(N)]
			for N in For(1,dim(L1)+.75,.25)
		)
	)
else:
	H = .5*dim(L_CW)
	M = 1
	N = H
	prgmQRECC()
	L4 = L1.copy()
	M = H+1
	N = 2*H
	prgmQRECC()
	L_CW = augment(
		seq(
			not_(fPart(N))*L_CW[int(N)]
			+2*fPart(N)*L_CW[H+int(N)]
			for N in For(1,H+.5,.5)
		),
		seq(
			not_(fPart(N))*L4[int(N)]
			+2*fPart(N)*L1[int(N)]
			for N in For(1,dim(L1)+.5,.5)
		)
	)


# Always pad
L_CW[1+dim(L_CW)] = 0

print('CW: ', L_CW)
print('TI-PY RESULT:')
print(L_CW.hex())

def prgmQRVER():
	global L_CW
	Ans = dim(L_CW)
	int(sqrt(8*Ans+400)/4-4-(Ans==26))


# def skip1():
	# return I=6

# def skip2():
	# return I=6 or abs(i-S+7)<=2 and abs(J-S+7)<=2

# def skip7():
	# D = 2*V+2
	# return I=6 or abs(D*fPart(I-4)/D))<=4 and abs(D*fPart(J-4)/D))<=4 and (abs(i-j)<=S/2-2) or I>=S-11 and J<=5 or J>=S-11 and I<=5


S = 17+4*V
for X in For(1,3):
	K = (S-7)*(X==3)
	L = (S-7)*(X==2)
	for J in For(L,L+5):
		Pxl_On(K,J)
	
	for I in For(K,K+5):
		Pxl_On(I,L+6)
	
	for J in For(L+6,L+1,-1):
		Pxl_On(K+6,J)
	
	for I in For(K+6,K+1,-1):
		Pxl_On(I,L)
	
	for I in For(K+2,K+4):
		for J in For(L+2,L+4):
			Pxl_On(I,J)

"TIMING"

for I in For(8,S-8):
	if not_(fPart(I/2)):
		Pxl_On(I,6)

for J in For(8,S-8):
	if not_(fPart(J/2)):
		Pxl_On(6,J)

Pxl_On(S-8,8)

"FORMAT"

Pxl_On(2,8)
Pxl_On(7,8)
Pxl_On(8,8)
Pxl_On(8,7)
Pxl_On(8,5)
Pxl_On(8,4)
Pxl_On(8,2)
Pxl_On(8,1)
Pxl_On(8,0)
Pxl_On(8,S-3)
Pxl_On(8,S-7)
Pxl_On(8,S-8)
Pxl_On(S-7,8)
Pxl_On(S-6,8)
Pxl_On(S-5,8)
Pxl_On(S-3,8)
Pxl_On(S-2,8)
Pxl_On(S-1,8)

"ALIGNMENT"

if V>1:
	if V<=6:
		L1 = L_[S-7]
		L2 = L_[S-7]
	else:
		Ans = L_[31892,34236,39577,42195,48118]
		B = Ans[V-6]
		for I in For(0,5):
			for J in For(S-11,S-9):
				if fPart(B/2):
					Pxl_On(I,J)
					Pxl_On(J,I)
				B = int(B/2)

		M = 6+.5*S-6.5
		L1 = L_[6,M,M,M,S-7,S-7]
		L2 = L_[M,6,M,S-7,M,S-7]
		
	for X in For(1,dim(L1)):
		K = L1[X]
		L = L2[X]
		for J in For(L-2,L+1):
			Pxl_On(K-2,J)
		
		for I in For(K-2,K+1):
			Pxl_On(I,L+2)
		
		for J in For(L+2,L-1,-1):
			Pxl_On(K+2,J)
		
		for I in For(K+2,K-1,-1):
			Pxl_On(I,L-2)
		
		Pxl_On(K,L)
	
else:
	pass


DispGraph()

check = list(qr.get_codewords((Str1.translate(str.maketrans("?;',!", "$%*+/")) if E else Str1).encode(), V, 'a' if E else 'b'))
if check == L_CW.inner:
	print('CORRECT!')
else:
	print('REAL RESULT:')
	print(' '.join(f"{b:02X}" for b in check))
	print('!!! INCORRECT !!!')
	for i, (b1, b2) in enumerate(zip(L_CW.inner, check)):
		if b1 != b2:
			print(i, b1, b2)
