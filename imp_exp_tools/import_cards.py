import json
import os

try:
    from card import Card
except ModuleNotFoundError:
    from imp_exp_tools.card import Card


def import_card_data(file='data/card-definitions.txt', to_print=True):
    with open(file, 'r', encoding='utf-8') as cards:
        json_data = json.load(cards)
        if to_print:
            for i in json_data:
                print(f'{i}: {json_data[i]}')
        return json_data


def import_price_data(file=None, to_print=False, cards=None):
    if file is None:
        candidates = [f'data/{item}' for item in os.listdir('data') if 'price-history-' in item]
        file = candidates[0]

    with open(file, 'r', encoding='utf-8') as prices:
        json_data = json.load(prices)
        if cards is not None and to_print:
            for i in json_data:
                print(f'{cards[i]["name"]}: {json_data[i]}')

        return json_data


def transpose_dict(d: dict):
    return_d = {}
    for i in d:
        new_key = d[i]
        if new_key not in return_d:
            return_d[new_key] = []
        return_d[new_key].append(i)

    return return_d


def get_cards(cards=None):
    if cards is None:
        cards = import_card_data(to_print=False)
    names = transpose_dict({_id: cards[_id]['name'] for _id in cards})
    return {name: Card(name, names[name]) for name in names}


def show(cards, prices):
    d = {}
    for card in prices:
        d[cards[card]["name"]] = prices[card]
        print(f'{cards[card]["name"]}: {prices[card]}')

    return d


def test():
    pass


if __name__ == '__main__':
    test()
