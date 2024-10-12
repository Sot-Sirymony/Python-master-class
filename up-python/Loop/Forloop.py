
# Python program to illustrate
# Iterating over range 0 to n-1
n = 4
for i in range(0, n):
    print(i)
    
# Python program to illustrate
# Iterating over a list
print("List Iteration")
lst = ["Education", "for", "all"]
for i in lst:
    print(i)
    
# Iterating over a tuple (immutable)
print("\nTuple Iteration")
tup = ("Education", "for", "all")
for i in tup:
    print(i)
    
    
# Iterating over a String
print("\nString Iteration")
str = "University"
for i in str:
    print(i)
    
    
    
# Iterating over dictionary
print("\nDictionary Iteration")
d = dict()
d['xyz'] = 987
d['abc'] = 789
print(d)
for i in d:
    print("%s %d" % (i, d[i]))
    
    
    
# Iterating over a set
print("\nSet Iteration")
set1 = {9, 8, 7, 7, 8, 9}
for i in set1:
    print(i),    