import argparse

parser = argparse.ArgumentParser()
parser.add_argument('a', type=int)
parser.add_argument('b', type=int)
args = parser.parse_args()

def xor1():
	A = args.a
	B = args.b
	P = 128
	X = 0
	while P > 0:
		C=int(A>=P)
		D=int(B>=P)
		X=X+P*(C^D)
		A=A-P*C
		B=B-P*D
		P=P//2
		
	return X
	
	
def xor2():
	A = args.a
	B = args.b
	return sum(2**P * (int(2 * ((A / 2**(P + 1)) % 1)) ^ int(2 * ((B / 2**(P + 1)) % 1))) for P in range(8))



print(xor2(), args.a ^ args.b)
