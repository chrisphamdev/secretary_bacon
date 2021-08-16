class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return '{} {}'.format(self.suit, self.value)

    def __repr__(self):
        return '{} {}'.format(self.suit, self.value)

class Deck:
    def __init__(self):
        self.deck = []

        for suit in ['Diamonds', 'Clubs', 'Hearts', 'Spades']:
            for num in range(1, 14):
                self.deck += [Card(num, suit)]
        
        print(self.deck)