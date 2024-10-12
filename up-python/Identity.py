#Identity Oeprator Same Location
x=2
y=2
print("x is 2",x is 2)
print("x is not y",x is not y)
print("x is not y",id(x))
print("x is not y",id(y))
#Identity Oeprator Not Same Location
z={1,2,3}
w={1,2,3}
print("z is 2",x is 2)
print("w is not z",x is not y)
print("w is not w",id(w))
print("z is not z",id(z))

