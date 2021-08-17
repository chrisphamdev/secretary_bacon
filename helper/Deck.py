import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

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
        
        self.shuffle()


    # this method shuffles the deck
    def shuffle(self):
        random.shuffle(self.deck)


    # this simulate a random card draw from the deck (draw from top)
    def draw(self):
        random_card = self.deck[0]
        self.deck.pop(0)
        return random_card


    # this function reinsert a card back into the deck
    def insert(self, card):
        self.deck += [card]
        self.shuffle()



