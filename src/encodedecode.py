s = 'cafe'
b = s.encode('utf8')
print(b)
print(b.decode('utf8'))

# Error handling in unicode
city = 'São Paulo'
#city.encode('cp437')   (raise a UnicodeEncodeError)

# The solution:
print(city.encode('cp437', errors='ignore'))
# or
print(city.encode('cp437', errors='replace'))
# or
print(city.encode('cp437', errors='xmlcharrefreplace'))
