from import_cards import import_price_data
from import_decklist import DeckReader


def merge_number_dicts(dict1, dict2):
    # we assume that values are numbers
    result_dict = {key: dict1.get(key, 0) + dict2.get(key, 0)
                   for key in set(dict1.keys()) | set(dict2.keys())}
    return result_dict


def minimize_deck_price(decklist, looks='0'):
    # set up
    deck_divided = DeckReader(decklist)
    try:
        collection = DeckReader('data/Full Trade List.txt').main
        if looks == '0':
            for card in deck_divided.main:
                if card in collection:
                    number = collection[card]
                    collection[card] -= deck_divided.main[card]
                    deck_divided.main[card] = max(0, deck_divided.main[card] - number)
            for card in deck_divided.side:
                if card in collection:
                    number = collection[card]
                    collection[card] -= deck_divided.side[card]
                    deck_divided.side[card] = max(0, deck_divided.side[card] - number)
    except OSError:
        print('NO COLLECTION UPLOADED')

    deck = merge_number_dicts(deck_divided.main, deck_divided.side)
    prices = import_price_data(to_print=False)
    deck_price = 0
    choices = []

    # main part
    for card in deck:
        card_prices = {_id: prices[_id] for _id in card.ids}
        card_id = min(card_prices, key=card_prices.get)

        choices.append(card_id)
        deck_price += card_prices[card_id] * deck[card]

    # return
    print(f'DECK PRICE: {deck_price}')

    choices_main = {}
    choices_side = {}
    for card in deck_divided.main:
        chosen_id = list(set(card.ids) & set(choices))[0]
        choices_main[chosen_id] = deck_divided.main[card]
    for card in deck_divided.side:
        chosen_id = list(set(card.ids) & set(choices))[0]
        choices_side[chosen_id] = deck_divided.side[card]

    choices = {'main': choices_main, 'side': choices_side}
    return deck_price, choices

