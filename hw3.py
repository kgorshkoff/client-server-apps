a = b'attribute'
b = b'класс'
c = b'функция'
d = b'type'

print(f'{a}, {b}, {c}, {d}')

'''
В байт-строку можно преобразовать только ASCII символы, соответственно, 
строки "класс" и "функция" записать как байт-строки не получится.

  File "/Users/kirill/PycharmProjects/client-server-apps/hw3.py", line 2
    b = b'класс'
       ^
SyntaxError: bytes can only contain ASCII literal characters.

'''