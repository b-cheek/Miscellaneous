import random

class Card:
    def __init__(self, points, suit):
        self.value = value
        self.suit = suit
        self.points = self.calculate_points()

    def calculate_points(self):
        if self.value == 'Joker':
            return 50
        elif self.value in ['Jack', 'Queen', 'King']:
            return 10 + ['Jack', 'Queen', 'King'].index(self.value)
        else:
            return int(self.value)

    def __str__(self):
        return f"{self.value} of {self.suit} ({self.points} points)"

class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []
        self.populate()
        self.shuffle()

    def populate(self):
        for suit in ["Spades", "Clubs", "Diamonds", "Hearts", "Stars"]:
            for value in range(3, 10):
                self.cards.append(Card(str(value), suit))
            self.cards.append(Card("Jack", suit))
            self.cards.append(Card("Queen", suit))
            self.cards.append(Card("King", suit))

        for i in range(6): self.cards.append(Card("Joker", suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_players):
        hands = [[] for _ in range(num_players)]
        for i in range(9):
            for j in range(num_players):
                hands[j].append(self.cards.pop())
        return hands

    def draw_card(self):
        if len(self.cards) == 0:
            self.cards = self.discard_pile.copy()
            self.discard_pile = []
            self.shuffle()
        return self.cards.pop()

    def discard(self, card):
        self.discard_pile.append(card)

    def __str__(self):
        return f"Deck with {len(self.cards)} cards remaining and {len(self.discard_pile)} cards in the discard pile."

class Player:
    def __init__(self):
        self.hand = []

    def make_move(self):
        # Placeholder for now
        pass