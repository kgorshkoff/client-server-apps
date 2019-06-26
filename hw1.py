import os
import re
import csv
import chardet
from pprint import pprint


def get_data():
    l_name = []
    l_code = []
    l_type = []
    l_prod = []
    cols = ['Название ОС', 'Код продукта', 'Тип системы', 'Изготовитель системы']
    data = []

    path = 'files/'

    for file in os.listdir(path):
        if file.endswith('.txt'):
            enc = chardet.detect(open(path + file, 'rb').read(200)).get('encoding')
            with open(path + file, encoding=enc) as f:
                for line in f:
                    if re.search(cols[0], line) is not None:
                        a = line.split(':')
                        b = a[1].strip()
                        l_name.append(b)
                    elif re.search(cols[1], line) is not None:
                        a = line.split(':')
                        b = a[1].strip()
                        l_code.append(b)
                    elif re.search(cols[2], line) is not None:
                        a = line.split(':')
                        b = a[1].strip()
                        l_type.append(b)
                    elif re.search(cols[3], line) is not None:
                        a = line.split(':')
                        b = a[1].strip()
                        l_prod.append(b)

    data.append(cols)

    for i in range(len(cols) - 1):
        tmp = []
        tmp.append(l_name[i])
        tmp.append(l_code[i])
        tmp.append(l_type[i])
        tmp.append(l_prod[i])
        data.append(tmp)

    return data


def write_to_csv(path):
    data = get_data()

    with open(path, 'w') as file:
        csv.writer(file).writerows(data)


write_to_csv('files/write.csv')