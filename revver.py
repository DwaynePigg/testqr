from tisetup import *

L1 = L_[26,44,70,100,134,172,196,242,292,346,404]
print(L1)
print(int((L1+27)**.5)-5)
print((L1/1.3)**.5)

C1 = 8*8*3+6+6+3+8+7+1
C2 = 25+7

# C = 250
# print(round(sqrt(L1*8+C)/4-4+(L1>172), 2))
# print(int(sqrt(L1*8+C)/4-4+(L1>172)))

C = 400
r = sqrt(L1*8+C)/4-4-(L1==26)
print(round(r,2))
print(int(r))

S=33

print(C1)

px=S**2 - 2*(S-16) - C1 - C2
print(px)
print(px/8)
