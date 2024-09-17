from array import array 
from random import random 

floats = array('d', (random() for i in range(10**2)))
print(floats)