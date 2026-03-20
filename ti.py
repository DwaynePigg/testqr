import math
import numbers
import operator
import sys
from functools import wraps
from itertools import accumulate, pairwise, chain, repeat
from math import prod

import qr


class TIList:

	def __init__(self, data):
		self.inner = list(data)
	
	def __getitem__(self, i):
		return self.inner[round(i) - 1]
	
	def __setitem__(self, i, n):
		i = round(i)
		if i == len(self) + 1:
			self.inner.append(n)
		elif not(1 <= i <= len(self)):
			raise ValueError(f"out of bounds: {i}; dim: {len(self)}")
		else:
			self.inner[i - 1] = n
	
	def __len__(self):
		return len(self.inner)
	
	def __iter__(self):
		return iter(self.inner)
	
	def __repr__(self):
		return f"{{{','.join(repr(int(i) if int(i) == i else i) for i in self)}}}"
	
	def hex(self):
		def _iter():
			for i in self:
				if int(i) != i:
					raise ValueError(i)
				yield f"{int(i):02X}"
		return ' '.join(_iter())


def and_(a, b):
	return int(bool(a and b))

def or_(a, b):
	return int(bool(a or b))

def xor(a, b):
	return int(bool(a) ^ bool(b))


for name, op in [
	('__add__', operator.add),
	('__radd__', operator.add),
	('__sub__', operator.sub),
	('__rsub__', lambda a, b: b - a),
	('__mul__', operator.mul),
	('__rmul__', operator.mul),
	# Can I use Fractions here?
	('__truediv__', operator.truediv),
	('__rtruediv__', lambda a, b: b / a),
	('__pow__', pow),
	('__rpow__', lambda a, b: b ** a),
	('__and__', and_),
	('__rand__', and_),
	('__or__', or_),
	('__ror__', or_),
	('__xor__', xor),
	('__rxor__', xor),
	('__eq__', operator.eq),
	('__ne__', operator.ne),
	('__lt__', operator.lt),
	('__gt__', operator.gt),
	('__le__', operator.le),
	('__ge__', operator.ge),
]:
	def list_op(self, other, op=op):
		if isinstance(other, TIList):
			return TIList(op(a, b) for a, b in zip(self, other, strict=True))
		return TIList(op(a, other) for a in self)

	setattr(TIList, name, list_op)


for name, op in [
	('__neg__', operator.neg),
	('__abs__', abs),
	('__round__', round),
	('__trunc__', math.trunc),
]:
	def list_op(self, op=op):
		return TIList(op(a) for a in self)

	setattr(TIList, name, list_op)


def _check_number(num):
	if not isinstance(num, numbers.Number):
		raise ValueError(f"Not a number: {num}")
	return num

def _check_list(lst):
	if not isinstance(lst, TIList):
		raise ValueError(f"Not a list: {lst}")
	return lst

def _check_str(str_):
	if not isinstance(str_, str):
		raise ValueError(f"Not a string: {str_}")
	return str_


def ti_list(data):
	for num in data:
		_check_number(num)
	return TIList(data)


class _ListAlias:
	def __getitem__(self, data):
		return ti_list((data,) if isinstance(data, numbers.Number) else data)

L_ = _ListAlias()


def Stop():
	sys.exit()

def Disp(*items):
	for item in items:
		print(item)

def seq(iterable):
	return ti_list(list(iterable))


def handle_complex(func):
	@wraps(func)
	def apply(a):
		return complex(func(a.real), func(a.imag)) if isinstance(a, complex) else func(a)
	return apply


def vectorized(func):
	@wraps(func)
	def apply(*args):
		len_check = set()
		vec = []
		for a in args:
			if isinstance(a, TIList):
				len_check.add(len(a))
				vec.append(a)
			else:
				vec.append(repeat(a))
		if not len_check:
			return func(*args)
		if len(len_check) == 1:
			return TIList(func(*v) for v in zip(*vec))
		raise ValueError(f"Dim mismatch: {len_check}")
		
	return apply


def dim(lst):
	return len(_check_list(lst))

def set_dim(lst, new_dim):
	del lst.inner[new_dim:]

@vectorized
def not_(num):
	return int(not num)

@vectorized 
@handle_complex
def iPart(num):
	return math.trunc(num)

@vectorized
@handle_complex
def int(num):
	return math.floor(num)

@vectorized
@handle_complex
def fPart(num):
	return num - math.trunc(num)

def cumSum(lst):
	return TIList(accumulate(_check_list(lst)))

def delta_list(lst):
	return TIList([b - a for a, b in pairwise(lst)])

def augment(*args):
	return TIList(chain.from_iterable(args))

@vectorized
def real(num):
	return num.real if isinstance(num, complex) else num

@vectorized
def imag(num):
	return num.imag if isinstance(num, complex) else 0

def sortA(lst, *dep, reverse=False):
	inner = _check_list(lst).inner
	indices = sorted(range(len(inner)), key=lambda i: inner[i], reverse=reverse)
	lst.inner = [inner[i] for i in indices]
	for d in dep:
		d.inner = [d.inner[i] for i in indices]

def sortD(lst, *dep):
	sortA(lst, *dep, reverse=True)

def Fill(lst, num):
	inner = _check_list(lst).inner
	_check_number(num)
	for i in len(inner):
		inner[i] = num

def For(start, stop, step=1):
	return range(start, stop + 1 if step > 0 else -1, step)

expr = eval

def inString(s, t):
	return _check_str(s).find(t) + 1

def length(s):
	return len(_check_str(s))

def sub(s, start, length):
	_check_str(s)
	if length < 1:
		raise ValueError(length)
	if not(1 <= start <= len(s) - length + 1):
		raise ValueError(s, start, length)
	return s[start - 1 : start - 1 + length]


###################
###################
#### END SETUP ####
###################
###################


Str1 = "ATTACK AT DAWN!"
E = 1

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
	O = 8*fPart(L/8)
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

	Str2 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ;!,'-.?:"
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

L1 = seq(0 for I in For(1,dim(L2)))  # ECC buffer
L3 = seq(2 ** I for I in For(8,1,-1))  # Powers of 2 for fast XOR

for I in For(1,dim(L_CW)):
	B = L_CW[I]
	F = .5*sum(L3*(1==abs(int(2*fPart(complex(L1[1],B)/L3)))))
	L1 = delta_list(cumSum(L1))
	L1[1 + dim(L1)] = 0
	for J in For(1,(F!=0)*dim(L2)):
		Ans = L_GFL[L2[J]] + L_GFL[F]
		L1[J] = .5*sum(L3*(1==abs(int(2*fPart(complex(L1[J],L_GFX[1+Ans-255*(Ans>254)])/L3)))))

print('ECC:', L1)
L_CW = augment(L_CW,L1)

# Always pad
L_CW[1+dim(L_CW)] = 0

print('CW: ', L_CW)
print(L_CW.hex())

check = list(qr.get_codewords((Str1.translate(str.maketrans(";!,'?", "$%*+/")) if E else Str1).encode(), V, 'a' if E else 'b'))
if check == L_CW.inner:
	print('CORRECT!')
else:
	print(' '.join(f"{b:02X}" for b in check))
	print('!!! INCORRECT !!!')
