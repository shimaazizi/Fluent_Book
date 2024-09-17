import array 

data = array.array('i', range(100))

mv = memoryview(data)

print(mv)

print(list(mv))

slice_view  = mv[10:20]

slice_view[0] = 2

print(data)