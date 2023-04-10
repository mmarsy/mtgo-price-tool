import os
from xml.dom import minidom
from handle_card_sets import minimize_deck_price
from import_cards import import_card_data


def export_to_dek(choice_of_cards, dictionary_of_cards, name=None):
    # choice_of_cards contains of two dictionaries whose key are ids of cards and values are number of copies
    # particular card.

    # diagnostics
    if set(choice_of_cards.keys()) != {'main', 'side'}:
        raise KeyError('MAIN OR SIDE ERROR')

    # set up
    if name is None:
        name = 'Deck-optimized.dek'

    root = minidom.Document()

    xml = root.createElement('Deck')
    xml.setAttribute('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    xml.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.appendChild(xml)

    # iterating
    for card in choice_of_cards['main']:
        temp_card = root.createElement('Cards')
        temp_card.setAttribute('CatID', str(card))
        temp_card.setAttribute('Quantity', str(choice_of_cards['main'][card]))
        temp_card.setAttribute('Sideboard', "false")
        temp_card.setAttribute('Name', str(dictionary_of_cards[card]['name']))
        temp_card.setAttribute('Annotation', "0")
        xml.appendChild(temp_card)

    for card in choice_of_cards['side']:
        temp_card = root.createElement('Cards')
        temp_card.setAttribute('CatID', str(card))
        temp_card.setAttribute('Quantity', str(choice_of_cards['side'][card]))
        temp_card.setAttribute('Sideboard', "true")
        temp_card.setAttribute('Name', str(dictionary_of_cards[card]['name']))
        temp_card.setAttribute('Annotation', "0")
        xml.appendChild(temp_card)

    xml_str = root.toprettyxml(indent="  ")

    save_path_file = name
    try:
        os.remove(save_path_file)
        print('OLD DECKFILE REMOVED')
    except OSError:
        pass
    with open(save_path_file, "w") as f:
        f.write(xml_str)


def test():
    price, choice = minimize_deck_price('uploaded-decks/Deck - Naya Depths.txt')
    export_to_dek(choice, import_card_data(to_print=False))


if __name__ == '__main__':
    test()
