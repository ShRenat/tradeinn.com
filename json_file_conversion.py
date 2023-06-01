import json
import pandas as pd


def replace_chars(string):
    chars_to_replace = ['+', '=', ' ', '®']
    replacement_char = '-'

    for char in chars_to_replace:
        string = string.replace(char, replacement_char)

    return string


with open('product.json', 'r', encoding='utf-8') as file:
    json_output = json.load(file)

url_to_add = 'https://www.tradeinn.com/bikeinn/ru'
pic_url_to_add = 'https://www.tradeinn.com/h'

results = []

id_modelos = json_output['id_modelos']

for model in id_modelos:
    all_size = []

    id_model = model['id_modelo']

    name = model['nombre_modelo']
    brand = model['marca']
    product_full_name = f'{brand} {name}'

    size = model['productes']
    for i in size:
        a = i['talla']
        all_size.append(a)

    price = float(model['precio_win'])
    pred_url = replace_chars(product_full_name)
    lower_url = pred_url.lower()
    url = f'{url_to_add}/{lower_url}/{id_model}/p'

    cut_id = id_model[:5]
    pic_url = f'{pic_url_to_add}/{cut_id}/{id_model}/{lower_url}.jpg'

    results.append([url, product_full_name, price, all_size, pic_url])

df = pd.DataFrame(results, columns=['URL', 'Name', 'Price', 'Size', 'Picture'])
# df.drop_duplicates(inplace=True)
df.to_csv('tradeinn-final-output.csv', sep=';', index=False)
