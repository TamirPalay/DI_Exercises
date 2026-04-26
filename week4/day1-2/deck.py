import random
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"
class Deck:
    def __init__(self):
        self.cards = []
        self.dealt = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
    def shuffle(self):
        # check the deck has all 52 cards before shuffling
        if len(self.cards) != 52:
            self.cards.extend(self.dealt)
            self.dealt = []
        random.shuffle(self.cards)
        print("Deck shuffled.")
    def deal(self):
        if self.cards:
            card = self.cards.pop()
            self.dealt.append(card)
            return card
        else:
            print("Error: The deck is empty.")
            return None

deck= Deck()
deck.shuffle()
print(deck.deal())
