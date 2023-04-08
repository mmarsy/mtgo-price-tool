import os

from handle_card_sets import minimize_deck_price
from export_decklist import export_to_dek
from import_cards import import_card_data


def main():
    decks = {str(index): file for index, file in enumerate(os.listdir('uploaded-decks'))}
    for key in decks:
        print(f'{key}: {decks[key]}')
    decklist = decks[input('CHOOSE DECKLIST TO HANDLE')]
    price, card_choices = minimize_deck_price(f'uploaded-decks/{decklist}')
    name = decklist
    if 'Deck' in name:
        name = name.replace('Deck', 'DeckOptimal')
        name = name.replace('.txt', '.dek')
    export_to_dek(card_choices, import_card_data(to_print=False), name)


if __name__ == '__main__':
    main()
