import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.points = self.calculate_points()

    def calculate_points(self):
        if self.value == 'Joker':
            return 50
        elif self.value in ['Jack', 'Queen', 'King']:
            return 10 + ['Jack', 'Queen', 'King'].index(self.value) + 1
        else:
            return int(self.value)

    def __str__(self):
        return f"{self.value} of {self.suit} ({self.points} points)"

class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []
        self.populate()

    def populate(self):
        for _ in range(2): ## Two decks
            for suit in ["Spades", "Clubs", "Diamonds", "Hearts", "Stars"]:
                for value in range(3, 11):
                    self.cards.append(Card(str(value), suit))
                self.cards.append(Card("Jack", suit))
                self.cards.append(Card("Queen", suit))
                self.cards.append(Card("King", suit))

        for i in range(6): self.cards.append(Card("Joker", suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, round, players):
        for _ in range(round+3): ## Deal the appropriate number of cards
            for start_deal in range(len(players)): ## Move the dealer each round
                players[(start_deal+round)%len(players)].draw_card(self)

        ## Move the top card to the discard pile
        self.discard_pile.append(self.cards.pop())
        
    def __str__(self):
        return f"Deck with {len(self.cards)} cards remaining and {len(self.discard_pile)} cards in the discard pile."

class Player:
    def __init__(self):
        self.hand = []

    def draw_card(self, deck):
        self.hand.append(deck.cards.pop())

    def discard(self, card, deck):
        deck.discard_pile.append(card)
        self.hand.remove(card)

    def make_move(self):
        # Placeholder for now
        return -1 ## Return value of going out if out, otherwise -1

deck = Deck()

numPlayers = int(input("How many players? "))
players = [Player() for _ in range(numPlayers)]

for round in range(11): ## Note that the wild card is round + 3

    ## Setup
    deck.shuffle()
    deck.deal(round, players)

    ## Play
    out = False ## Set to True when someone goes out
    while out < 0: ## While no one has gone out
        for start_player in range(len(players)):
            ## This keeps checking out, and sets it to allow for points stuff if someone goes out. I'll add that logic later.
            out = players[(start_player+round)%len(players)].make_move() ## Player to the left of the dealer goes first

    ## Scoring

    ## Cleanup
    
