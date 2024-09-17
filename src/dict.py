a = dict(one=1, two=2, three=3)
b = {'one':1, 'two':2, 'three':3 }
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('one', 1), ('two', 2), ('three', 3)])

print(a, b, c, d)

dial_codes = [(86, 'china'), (91, 'india'), (1, 'united states')]

country_code = {country: code for code, country in dial_codes}
filtered_codes = {code: country for country, code in country_code.items() if code < 66}

print(filtered_codes)