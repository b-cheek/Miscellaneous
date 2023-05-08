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
        if self.suit == "Special":
            return f"{self.value}"
        return f"{self.value} of {self.suit}"

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

        for i in range(6): self.cards.append(Card("Joker", "Special"))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, round, players):
        for _ in range(round+3): ## Deal the appropriate number of cards
            for start_deal in range(len(players)): ## Move the dealer each round
                players[(start_deal+round)%len(players)].draw_card(self)

        ## Move the top card to the discard pile
        self.discard_pile.append(self.cards.pop())

    def __str__(self):
        res = ""
        res += "Cards:\n"
        for card in self.cards:
            res += str(card) + "\n"
        res += "\nDiscard Pile:\n"
        for card in self.discard_pile:
            res += str(card) + "\n"
        return res

class Player:
    def __init__(self):
        self.hand = []
        self.out_hand = []

    def draw_card(self, deck):
        self.hand.append(deck.cards.pop())

    def discard(self, card, deck):
        deck.discard_pile.append(card)
        self.hand.remove(card)

    def make_move(self, deck, wild):
        # Placeholder for now
        return False ## Return true if the player goes out, false otherwise

    def go_out(self):
        ## Move books and runs into the out hand, and return the points of other cards
        return sum([card.points for card in self.hand])

    def __str__(self):
        res = ""
        res += "Hand:\n"
        for card in self.hand:
            res += str(card) + "\n"
        res += "\nOut Hand:\n"
        for card in self.out_hand:
            res += str(card) + "\n"
        return res

deck = Deck()

numPlayers = int(input("How many players? "))
players = [Player() for _ in range(numPlayers)]
scores = [0 for _ in range(numPlayers)]

for round in range(11):

    ## Setup
    wild = round + 3 ## Rounds are zero indexed, 3 is wild on the first round
    if wild == 11: wild = "Jack"
    elif wild == 12: wild = "Queen"
    elif wild == 13: wild = "King"
    deck.shuffle()
    deck.deal(round, players)

    ## Play
    out = False ## Set to True when someone goes out
    while not out:
        for i in range(len(players)):
            start_player = (i+round)%len(players) ## Make start player left of the dealer
            ## This line makes a move for each player and checks if they went out
            out = players[start_player].make_move(deck, wild)
            
            if out == True:
                ## Scoring
                for j in range (1, len(players)): ## loop through remaining players once
                    remaining_player = (start_player+j)%len(players)
                    scores[remaining_player] += players[remaining_player].go_out()
                break

    ## Cleanup
    for player in players: ##Put all cards in the discard pile
        for _ in range(len(player.hand)): deck.discard_pile.append(player.hand.pop())
        for out_group in player.out_hand:
            for _ in range(out_group): deck.discard_pile.append(player.out_hand.pop())

    ## Put all cards back in the deck
    for _ in range(len(deck.discard_pile)): deck.cards.append(deck.discard_pile.pop())
        
