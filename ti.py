import builtins
import math
import numbers
import operator
from functools import wraps
from itertools import accumulate, pairwise, chain, repeat
from math import prod


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
		return f"{{{','.join(repr(o) for o in self)}}}"


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


def LIST(*data):
	for num in data:
		_check_number(num)
	return TIList(data)

def seq(iterable):
	return LIST(*list(iterable))

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


dim = len

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
	return s.find(t) + 1

def length(s):
	# ensure string
	return len(s)

def sub(s, start, length):
	if length < 1:
		raise ValueError(length)
	if not(1 <= start <= len(s) - length + 1):
		raise ValueError(s, start, length)
	return s[start - 1 : start - 1 + length]

Str1 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ;!,'-.?:"
Str2 = "ATTACK AT DAWN"
LLEN = LIST(152,272,440,640,864,1088,1248,1552,1856,2192,2592)

def prgmBITBUF1():
	global N,S,L,LCW
	for I in For(S-1,0,-1):
		Ans = int(N/(2**I))
		B=2*int(Ans/2)
		if not_(fPart(L/8)):
			LCW[1+dim(LCW)] = 0
		if B:
			LCW[dim(LCW)] = LCW[dim(LCW)]+2**(7-8*fPart(L/8))
		L = L + 1


def prgmBITBUF():
	global L, LCW, L1, S

	for I in For(1,dim(L1)):
		N = L1[I]
		R = S
		O = 8*fPart(L/8)
		if O!=0:
			T = min([8-O,R])
			Ans = 2**T
			LCW[dim(LCW)] = LCW[dim(LCW)]+Ans*fPart(int(N/2**(R-T))/Ans)*2**(8-O-T)
			R = R-T

		while R>=8:
			LCW[1+dim(LCW)] = 256*fPart(int(N/2**(R-8))/256)
			R = R-8

		if R>0:
			Ans = 2**R
			LCW[1+dim(LCW)] = Ans*fPart(N/Ans)*2**(8-R)

		L = L+S

L = 0
LCW = LIST()
print('LCW', LCW)

S = 4
L1 = LIST(2)
prgmBITBUF()

S = 9
L1 = LIST(length(Str2))
prgmBITBUF()

S = 11
L1 = seq(45*max(1,inString(Str1,sub(Str2,I,1)))+max(1,inString(Str1,sub(Str2,I+1,1)))-46 for I in For(1,length(Str2)-1,2))
prgmBITBUF()

if fPart(length(Str2)/2):
	S = 6
	L1 = LIST(max(1,inString(Str1,sub(Str2,length(Str2),1)))-1)
	prgmBITBUF()

S = min(LIST(4,LLEN[1]-L))
L1 = LIST(0)
prgmBITBUF()

for F in For(1,int(LLEN[1]/8)-dim(LCW)):
	LCW[1+dim(LCW)] = LIST(0xEC,0x11)[2*(fPart(F/2))]

# Always pad
LCW[1+dim(LCW)] = 0

print('LCW', LCW)
print(' '.join(f"{round(b):02X}" for b in LCW))

LGFL = LIST(0,1,25,2,50,26,198,3,223,51,238,27,104,199,75,4,100,224,14,52,141,239,129,28,193,105,248,200,8,76,113,5,138,101,47,225,36,15,33,53,147,142,218,240,18,130,69,29,181,194,125,106,39,249,185,201,154,9,120,77,228,114,166,6,191,139,98,102,221,48,253,226,152,37,179,16,145,34,136,54,208,148,206,143,150,219,189,241,210,19,92,131,56,70,64,30,66,182,163,195,72,126,110,107,58,40,84,250,133,186,61,202,94,155,159,10,21,121,43,78,212,229,172,115,243,167,87,7,112,192,247,140,128,99,13,103,74,222,237,49,197,254,24,227,165,153,119,38,184,180,124,17,68,146,217,35,32,137,46,55,63,209,91,149,188,207,205,144,135,151,178,220,252,190,97,242,86,211,171,20,42,93,158,132,60,57,83,71,109,65,162,31,45,67,216,183,123,164,118,196,23,73,236,127,12,111,246,108,161,59,82,41,157,85,170,251,96,134,177,187,204,62,90,203,89,95,176,156,169,160,81,11,245,22,235,122,117,44,215,79,174,213,233,230,231,173,232,116,214,244,234,168,80,88,175)  # original list is undefined at 0. I removed element 0 here, so this list is kind of 0-indexed now
LGFX = LIST(1,2,4,8,16,32,64,128,29,58,116,232,205,135,19,38,76,152,45,90,180,117,234,201,143,3,6,12,24,48,96,192,157,39,78,156,37,74,148,53,106,212,181,119,238,193,159,35,70,140,5,10,20,40,80,160,93,186,105,210,185,111,222,161,95,190,97,194,153,47,94,188,101,202,137,15,30,60,120,240,253,231,211,187,107,214,177,127,254,225,223,163,91,182,113,226,217,175,67,134,17,34,68,136,13,26,52,104,208,189,103,206,129,31,62,124,248,237,199,147,59,118,236,197,151,51,102,204,133,23,46,92,184,109,218,169,79,158,33,66,132,21,42,84,168,77,154,41,82,164,85,170,73,146,57,114,228,213,183,115,230,209,191,99,198,145,63,126,252,229,215,179,123,246,241,255,227,219,171,75,150,49,98,196,149,55,110,220,165,87,174,65,130,25,50,100,200,141,7,14,28,56,112,224,221,167,83,166,81,162,89,178,121,242,249,239,195,155,43,86,172,69,138,9,18,36,72,144,61,122,244,245,247,243,251,235,203,139,11,22,44,88,176,125,250,233,207,131,27,54,108,216,173,71,142)

LRS7 = LIST(127, 122, 154, 164, 11, 68, 117)

L3 = LRS7
L2 = seq(0 for _ in For(1, dim(L3)))
L4 = seq(2 ** N for N in For(8,1,-1))

for I in For(1, dim(LCW)):
	B = LCW[I]
	F = .5*sum(L4*(1==abs(int(2*fPart(complex(L2[1],B)/L4)))))
	L2 = delta_list(cumSum(L2))
	L2[1 + dim(L2)] = 0
	for J in For(1,(F!=0)*dim(L3)):
		Ans = LGFL[L3[J]] + LGFL[F]
		L2[J] = .5*sum(L4*(1==abs(int(2*fPart(complex(L2[J],LGFX[1+Ans-255*(Ans>254)])/L4)))))

print(' '.join(f"{round(b):02X}" for b in L2))
LCW = augment(LCW,L2)


print(' '.join(f"{round(b):02X}" for b in LCW))
