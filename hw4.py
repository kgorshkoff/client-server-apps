a = 'разработка'
b = 'администрирование'
c = 'protocol'
d = 'standard'

a = a.encode('utf-8')
b = b.encode('utf-8')
c = c.encode('utf-8')
d = d.encode('utf-8')

print(f'{a}, {b}, {c}, {d}')

a = a.decode('utf-8')
b = b.decode('utf-8')
c = c.decode('utf-8')
d = d.decode('utf-8')

print(f'{a}, {b}, {c}, {d}')

a = a.encode('latin-1')
b = b.encode('latin-1')
c = c.encode('latin-1')
d = d.encode('latin-1')

print(f'{a}, {b}, {c}, {d}')

a = a.decode('latin-1')
b = b.decode('latin-1')
c = c.decode('latin-1')
d = d.decode('latin-1')

print(f'{a}, {b}, {c}, {d}')

'''
    a = a.encode('latin-1')
UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-9: ordinal not in range(256)

При попытке закодировать кириллицу в кодировку "latin-1" возникает ошибка, 
так как подобных симоволов в этой кодировке не существует
'''