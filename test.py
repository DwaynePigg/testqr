from tisetup import *

V = 7
S = 17+4*V
T = 2*V+2
M = 6+.5*S-6.5
L1 = L_[6,M,M,M,S-7,S-7]
L2 = L_[M,6,M,S-7,M,S-7]
Y1 = lambda: I==6 or abs(T*fPart(I/T)-6)<=2.1 and abs(T*fPart(J/T)-6)<=2.1 and (abs(I-J)<=S/2-2) or J>=S-11 and I<=5
Y2 = lambda: I==6 or min(abs(I-L1))<=2 and min(abs(J-L2))<=2 or J>=S-11 and I<=5

for I in For(0,S):
	for J in For(0,S):
		if Y2() and not Y1():
			Pxl_On(I,J)
	
DispGraph()
