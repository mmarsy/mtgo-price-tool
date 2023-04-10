from import_cards import import_price_data
from import_decklist import DeckReader

import xml.etree.ElementTree as ElementTree


def merge_number_dicts(dict1, dict2):
    # we assume that values are numbers
    result_dict = {key: dict1.get(key, 0) + dict2.get(key, 0)
                   for key in set(dict1.keys()) | set(dict2.keys())}
    return result_dict


def import_full_collection(to_print=False):
    tree = ElementTree.parse('data/Full Trade List.dek')
    root = tree.getroot()
    cards = {}

    for item in root.findall('Cards'):
        cards[item.attrib['CatID']] = {'name': item.attrib['Name'], 'quantity': item.attrib['Quantity']}

    if to_print:
        for card in cards:
            print(f'{card}: {cards[card]}')

    return cards


class Collection:
    def __init__(self):
        self.full = import_full_collection(False)
        self.simplified = {}
        for card in self.full:
            self.simplified[self.full[card]['name']] = self.simplified.get(self.full[card]['name'], 0) + int(self.full[card]['quantity'])


def minimize_deck_price(decklist):
    # set up
    deck_divided = DeckReader(decklist)
    collection_uploaded = True
    collection = None
    try:
        collection = Collection().simplified
    except FileNotFoundError:
        collection_uploaded = False

    if collection_uploaded:
        missing_cards = {'main': {}, 'side': {}}
        for card in deck_divided.main:
            if card in collection:
                number = collection[card]
                collection[card] -= deck_divided.main[card]
                change = deck_divided.main[card] - max(0, deck_divided.main[card] - number)
                deck_divided.main[card] = max(0, deck_divided.main[card] - number)
                missing_cards['main'][card] = missing_cards['main'].get(card, 0) + change
        for card in deck_divided.side:
            if card in collection:
                number = collection[card]
                collection[card] -= deck_divided.side[card]
                change = deck_divided.side[card] - max(0, deck_divided.side[card] - number)
                deck_divided.side[card] = max(0, deck_divided.side[card] - number)
                missing_cards['side'][card] = missing_cards['side'].get(card, 0) + change

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

    choices_main = {}
    choices_side = {}
    for card in deck_divided.main:
        chosen_id = list(set(card.ids) & set(choices))[0]
        choices_main[chosen_id] = deck_divided.main[card]
    for card in deck_divided.side:
        chosen_id = list(set(card.ids) & set(choices))[0]
        choices_side[chosen_id] = deck_divided.side[card]

    # add already owned cards
    if collection_uploaded:
        # gather ids of missing cards
        replacements = {'main': {}, 'side': {}}
        collection = Collection().full
        for card in missing_cards['main']:
            missing = missing_cards['main'][card]
            possible_replacements = {_id: collection[_id]['quantity'] for _id in collection if collection[_id]['name'] == card}
            for _id in possible_replacements:
                replacements['main'][_id] = min(int(missing), int(possible_replacements[_id]))
                missing_cards['main'][card] -= replacements['main'][_id]
                if missing_cards['main'][card] <= 0:
                    break
        for card in missing_cards['side']:
            missing = missing_cards['side'][card]
            possible_replacements = {_id: collection[_id]['quantity'] for _id in collection if collection[_id]['name'] == card}
            for _id in possible_replacements:
                replacements['side'][_id] = min(int(missing), int(possible_replacements[_id]))
                missing_cards['side'][card] -= replacements['side'][_id]
                if missing_cards['side'][card] <= 0:
                    break

    # return
    print(f'DECK PRICE: {deck_price}')
    choices = {'main': choices_main, 'side': choices_side}
    if collection_uploaded:
        for key in choices:
            choices[key] = merge_number_dicts(choices[key], replacements[key])
    else:
        print('CONSIDER UPLOADING YOUR COLLECTION FOR BETTER RESULTS (IN .dek FORMAT)')
        print('DOWNLOAD IT FROM MRGO CLIENT AND PASTE INTO data/ DIRECTORY')
    return deck_price, choices


def test():
    d = Collection().full
    for i in d:
        print(i, d[i])


if __name__ == '__main__':
    test()
