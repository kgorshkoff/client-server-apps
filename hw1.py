import os
import re
import chardet

result = []


def get_data():
    path = 'files/'
    for file in os.listdir(path):
        if file.endswith('.txt'):
            enc = chardet.detect(open(path + file, 'rb').read(200)).get('encoding')
            with open(path + file, encoding=enc) as f:
                for line in f:
                    match = re.match(r'(Название ОС.*|Код продукта.*|Тип системы.*|Изготовитель системы.*)', line)
                    if match is not None:
                        result.append(match.group(0))

                print(result)
                # result = re.findall(r'(Название ОС.*|Код продукта.*|Тип системы.*|Изготовитель системы.*)', f.read())
                # print(result)

get_data()
