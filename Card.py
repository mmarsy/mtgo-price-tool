class Card:
    # this class represents a class of cards, that are the same in game.
    # in one such class we should find lightning bolt from alpha and lightning bolt from m12
    # this is strictly deck-building object
    def __init__(self, name, ids=None):
        if ids is None:
            ids = []
        self.name = name
        self.ids = ids

    def __repr__(self):
        return f'<{self.name}: {self.ids}>'

    # this definition of hash means that name is only distinguishing property od Card
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)


def test():
    a = Card('a', [])
    b = Card('a', [])
    a.ids.append('1')
    print({a: 'foo}', b: 'bar'})


if __name__ == '__main__':
    test()
