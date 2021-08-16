from Deck import Deck

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.dealer_hand = []
        self.player_hand = []
        
        for i in range(2):
            self.dealer_hand += [deck.draw()]
            self.player_hand += [deck.draw()]


    def player_draw(self):
        self.player_hand += [deck.draw()]


    def dealer_decide(self):
        if sum(self.dealer_hand) <= 16:
            self.dealer_hand += [deck.draw()]
