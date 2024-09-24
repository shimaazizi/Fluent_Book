from unicodedata import normalize
s1 = 'café'    
s2 = 'cafe\u0301' 

print(normalize('NFC', s1) == normalize('NFC', s2)) 