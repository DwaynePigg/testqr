import math
import operator
import sys
from functools import wraps
from itertools import accumulate, pairwise, chain, repeat
from math import prod
from numbers import Number

import qr


class TIList:

	def __init__(self, data=()):
		self.inner = list(data)
	
	def __getitem__(self, i):
		if i != int(i) or not(1 <= i <= len(self)):
			raise IndexError(f"{i=}")
		return self.inner[int(i) - 1]
	
	def __setitem__(self, i, n):
		if i == len(self) + 1:
			self.inner.append(n)
		elif i != int(i) or not(1 <= i <= len(self)):
			raise ValueError(f"out of bounds: {i}; dim: {len(self)}")
		else:
			self.inner[int(i) - 1] = n
	
	def __len__(self):
		return len(self.inner)
	
	def __iter__(self):
		return (int(i) if int(i) == i else i for i in self.inner)
	
	def __repr__(self):
		return f"{{{','.join(repr(int(i) if int(i) == i else i) for i in self)}}}"
	
	def hex(self):
		def _iter():
			for i in self:
				if int(i) != i:
					raise ValueError(i)
				yield f"{int(i):02X}"
		return ' '.join(_iter())

	def copy():
		return TIList(list(self.inner))


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
	if not isinstance(num, Number):
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
		return ti_list((data,) if isinstance(data, Number) else data)

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
	if new_dim < len(lst):
		del lst.inner[new_dim:]
	elif new_dim > len(lst):
		lst.inner.extend(0 for _ in range(new_dim - len(lst)))

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

def augment(lst1, lst2):
	return TIList(chain(lst1, lst2))

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
	if step == 0:
		raise ValueError(f"{step=}")
	n = start
	op = operator.le if step > 0 else operator.ge
	while op(n, stop):
		yield n
		n += step

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
