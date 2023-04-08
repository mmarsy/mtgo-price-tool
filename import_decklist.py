import warnings

from import_cards import get_cards


class DeckReader:
    # this class import decks from file
    def __init__(self, decklist):
        # set up
        mode = 'main'
        deck = {'main': {}, 'side': {}}

        with open(decklist, 'r', encoding='utf-8') as file:
            for line in file:
                temp_line = line[:line.find('\n')]
                if not temp_line:
                    mode = 'side'
                else:
                    count = temp_line[:temp_line.find(' ')]
                    name = temp_line[temp_line.find(' ') + 1:]
                    deck[mode][name] = int(count)
        cards = get_cards()

        # return
        self.main = {}
        self.side = {}
        for name in deck['main']:
            try:
                self.main[cards[name]] = deck['main'][name]
            except KeyError:
                warnings.warn(UserWarning(f'Card Missing: {name}'))

        for name in deck['side']:
            try:
                self.side[cards[name]] = deck['side'][name]
            except KeyError:
                warnings.warn(UserWarning(f'Card Missing: {name}'))


def test():
    pass


if __name__ == '__main__':
    test()
