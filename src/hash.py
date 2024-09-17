t = (1, 2, (30, 40))

print(hash(t))

t1 = (1, 2, [30, 40])

# raise error because 
print(hash(t1))
