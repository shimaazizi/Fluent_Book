from collections import Counter 

# with counter from collections
words = ['apple', 'cherry', 'apple', 'banana', 'cherry']
counter = Counter(words)

print(counter)


# with manual

words = 'aabsbdba'
counter1 ={}

for char in words:
    if char not in counter1:
        counter1[char] =1
    else:
        counter1[char] += 1
print(counter1)