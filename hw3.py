import yaml


def write_to_yaml(path):
    data = {
        'first': ['one', 'two', 'three'],
        'second': 123,
        'third': {
            '€': 'euro',
            '¥': 'yen'}
    }

    with open(path, 'w') as file:
        yaml.dump(data, file, Dumper=yaml.Dumper, default_flow_style=True, allow_unicode=True)

write_to_yaml('files/write.yaml')