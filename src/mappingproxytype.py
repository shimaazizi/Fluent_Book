from types import MappingProxyType

d = {1: "A"}
d_proxy = MappingProxyType(d)

print(d_proxy)
d[2] = 'B'
print(d)
print(d_proxy)








