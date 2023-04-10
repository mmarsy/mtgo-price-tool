import os

from update_prices import update_prices, import_card_definitions
from handle_card_sets import minimize_deck_price
from export_decklist import export_to_dek
from import_cards import import_card_data


def main():
    # diagnostics and updates
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('results'):
        os.mkdir('results')
    if not os.path.isdir('uploaded-decks'):
        os.mkdir('uploaded-decks')
    update_prices()
    import_card_definitions()

    decks = {str(index): file for index, file in enumerate(os.listdir('uploaded-decks'))}
    for key in decks:
        print(f'{key}: {decks[key]}')
    decklist = decks[input('CHOOSE DECKLIST TO HANDLE')]
    price, card_choices = minimize_deck_price(f'uploaded-decks/{decklist}')
    name = decklist
    name = name.replace('.txt', '.dek')
    if 'Deck' in name:
        name = name.replace('Deck', 'DeckOptimal')
    else:
        name = f'DeckOptimal-{name}'

    name = f'results/{name}'
    export_to_dek(card_choices, import_card_data(to_print=False), name)


if __name__ == '__main__':
    main()
