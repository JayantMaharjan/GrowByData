import json
from urllib.parse import urlparse, parse_qs
import pandas as pd
import requests
from config import items, apiKey

final_list = []


def get_data(ingredient):
    url1 = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient}&number=5&apiKey={apiKey}'
    print(url1)
    response = requests.get(url1)
    response_json = json.loads(response.text)
    parsed_url = urlparse(url1)
    # taking the searched ingredient
    searchquery = parse_qs(parsed_url.query)['ingredients'][0]
    return response_json, searchquery


def data_extract(i, j, ingredient_type, searchquery):
    data = {'search_query': searchquery,
            'id': i['id'],
            'missedIngredientCount': i['missedIngredientCount'],
            'type': ingredient_type,
            'aisle': j['aisle'],
            'usedIngredientCount': i['usedIngredientCount'],
            'title': i['title'],
            'name': j['name'],
            'unit': j['unit'],
            'amount': j['amount']}
    final_list.append(data)


def main():
    c = []
    for i in items:
        # joining the multiple data with '+'
        c.append("+".join(i))
    print(c)
    output = pd.DataFrame()
    for ingredient in c:
        apiData, searchquery = get_data(ingredient)
        for i in apiData:
            for j in i['missedIngredients']:
                ingredient_type = 'missed_ingredients'
                data_extract(i, j, ingredient_type, searchquery)

            for j in i['usedIngredients']:
                ingredient_type = 'used_ingredients'
                data_extract(i, j, ingredient_type, searchquery)

    output = output.append(final_list).reset_index(drop=True)
    print(output)
    output.to_csv('output.csv', index=False)


if __name__ == '__main__':
    main()
