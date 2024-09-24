open('cafe.txt', 'w', encoding='utf_8').write('café')

# Read without encodeing
print(open('cafe.txt').read())

# Read with encoding
open('cafe.txt', encoding='utf_8').read()
