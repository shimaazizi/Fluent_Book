import array 
import time


data = array.array('i', range(100))

mv = memoryview(data)

print(mv)

print(list(mv))

slice_view  = mv[10:20]

slice_view[0] = 2

print(data)

#######
large_data = bytearray(b'a' * 10_000_000)
start_time = time.time()
sliced_data = large_data[2_000_000:5_000_000]
sliced_data = b"XYZ" * len(sliced_data)


end_time = time.time()
print("Time without memoryview :", end_time - start_time)

####

start_time = time.time()
view = memoryview(large_data)
view[2_000_000:5_000_000] = b"XYZ" * 1_000_000 


end_time = time.time()
print("Time with memoryview :", end_time - start_time)
