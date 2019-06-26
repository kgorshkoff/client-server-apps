import json

def write_order_to_json(file, item, quantity, price, buyer, date):
    new_data = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }

    with open(file, 'r') as f:
        data = json.load(f)

    data['orders'].append(new_data)

    with open(file, 'w') as f:
        raw = json.dumps(data, indent=4)
        f.write(raw)

write_order_to_json('files/orders.json', 'Keyboard', 5, 200, 'Ivan', '30.05.2018')
write_order_to_json('files/orders.json', 'Monitor', 11, 200, 'Max', '30.05.2018')
write_order_to_json('files/orders.json', 'Mouse', 114, 50, 'George', '30.05.2018')