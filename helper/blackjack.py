from Deck import Deck

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.dealer_hand = []
        self.player_hand = []
        
        for i in range(2):
            self.dealer_hand += [self.deck.draw()]
            self.player_hand += [self.deck.draw()]


    def player_draw(self):
        self.player_hand += [self.deck.draw()]


    def dealer_decide(self):
        if sum(self.dealer_hand) <= 16:
            self.dealer_hand += [self.deck.draw()]


    def get_player_hand(self):
        output = []
        suits_dict = {'Spades': '♠', 'Hearts':'♥', 'Clubs':'♣', 'Diamonds':'♦'}

        for card in self.player_hand:
            output += [(suits_dict[card.suit], card.value)]
        return output

    def get_dealer_hand(self):
        output = []
        suits_dict = {'Spades': '♠', 'Hearts':'♥', 'Clubs':'♣', 'Diamonds':'♦'}

        for card in self.player_hand:
            output += [(suits_dict[card.suit], card.value)]

        return output