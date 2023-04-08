from import_cards import import_price_data
from import_decklist import DeckReader


def merge_number_dicts(dict1, dict2):
    # we assume that values are numbers
    result_dict = {key: dict1.get(key, 0) + dict2.get(key, 0)
                   for key in set(dict1.keys()) | set(dict2.keys())}
    return result_dict


def minimize_deck_price(decklist):
    # set up
    deck = DeckReader(decklist)
    deck = merge_number_dicts(deck.main, deck.side)
    prices = import_price_data(to_print=False)
    deck_price = 0
    choices = {}

    # main part
    for card in deck:
        card_prices = {_id: prices[_id] for _id in card.ids}
        card_id = min(card_prices, key=card_prices.get)

        choices[card_id] = deck[card]
        deck_price += card_prices[card_id] * deck[card]

    # return
    print(deck_price)
    for i in choices:
        print(f'{i}: {choices[i]}')
    return deck_price, choices


def main():
    minimize_deck_price('Deck - Naya Depths.txt')


if __name__ == '__main__':
    main()
