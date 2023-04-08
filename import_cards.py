import json


def import_cards(to_print=True):
    with open('card-definitions.txt', 'r', encoding='utf-8') as cards:
        json_data = json.load(cards)
        if to_print:
            for i in json_data:
                print(f'{i}: {json_data[i]}')
        return json_data


def import_prices(to_print=False, cards=None):
    with open('price-history-2023-04-06.txt', 'r', encoding='utf-8') as prices:
        json_data = json.load(prices)
        if cards is not None and to_print:
            for i in json_data:
                print(f'{cards[i]["name"]}: {json_data[i]}')

        return json_data


def show(cards, prices):
    d = {}
    for card in prices:
        d[cards[card]["name"]] = prices[card]
        print(f'{cards[card]["name"]}: {prices[card]}')

    return d


def test():
    # import
    cards = import_cards(False)
    prices = import_prices(False)

    # filtering
    cards = {card: cards[card] for card in cards if cards[card]['rarity'] != 'Booster'}
    prices = {card: prices[card] for card in prices if prices[card] > 0.5 and card in cards}

    # return
    show(cards, prices)
    print(len(prices))


if __name__ == '__main__':
    test()
