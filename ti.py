from itertools import accumulate, pairwise, chain
from math import floor as iPart


class TIList(list):
	
	def __getitem__(self, i):
		return super().__getitem__(i - 1)
	
	def __setitem__(self, i, n):
		if len(self) == i - 1:
			self.append(n)
		else:
			super().__setitem__(i, n - 1)

dim = len

def fPart(N):
	return N % 1

def cumSum(L):
	return list(accumulate(L))

def delta_list(L):
	return [b - a for a, b in pairwise(L)]

def augment(*lists):
	return list(chain.from_iterable(lists))


if __name__ == '__main__':
	L = TIList()
	print(L)
	L[1] = 7
	print(L)
