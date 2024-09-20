from collections import ChainMap 
# using ChainMap
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

chain = ChainMap(dict1, dict2)
print(chain)
print(chain['a'])
print(chain['b'])

# using merging
merged = {**dict1, **dict2}
print(merged)
