import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.points = self.calculate_points()

    def calculate_points(self): ## Note that the value of a wild card is handled separately, since I want the cards to be immutable
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
        
        self.cards = [] ## Players draw from deck.cards, also how dealing works
        self.discard_pile = []
        self.populate() ## Fill the deck with cards

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
                players[(start_deal+round)%len(players)].draw_card(self.cards)

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
        self.wild = None ## Current wild value for internal use
        self.num_wilds = 0 ## Number of wilds in the hand

    def draw_card(self, pile):
        ## Put cards in order as you are given them
        card = pile.pop()

        ## Wilds and jokers are always at the end for ease of parsing and inserting (note self.num_wilds)
        if card.value == self.wild or card.value == "Joker":
            ## Put at end of hand
            self.hand.append(card)
            self.num_wilds += 1
            return card

        if len(self.hand) == 0:
            self.hand.append(card)
            return card

        insert_index = 0
        while (insert_index < len(self.hand)-self.num_wilds and self.hand[insert_index].points < card.points):
            insert_index += 1
        self.hand.insert(insert_index, card)
        return card

    def discard(self, card, deck):
        deck.discard_pile.append(card)
        self.hand.remove(card)

    def make_move(self, deck, wild):
        ## Pick up a card
        ## Keep it if it's wild
        if deck.discard_pile[-1] == "Joker" or deck.discard_pile[-1].value == wild:
            self.draw_card(deck.discard_pile)

        ## Check if it's helpful
        card = self.draw_card(deck.discard_pile)
        card_index = self.hand.index(card)
        ## Determine if the card is in a run
        run_size = 0
        ## Check left
        l = card_index ## Index will move to the left in hand, checking adjacent cards
        run_left_val = card.points ## This will decrement according to ensure decrease by one
        while l>=0 and self.hand[l].points >= run_left_val - 1: ## ^ continue while no jumps >1
            if self.hand[l].suit == card.suit:
                run_size += 1 
            if self.hand[l].points == run_left_val - 1: ## Adjust left val as moving
                run_left_val -= 1
            l -= 1

        ## Do the same for the right side
        r = card_index + 1 ## Start right of the pulled card so it is not double-counted
        run_right_val = card.points
        while r < len(self.hand)-self.num_wilds and self.hand[r].points <= run_right_val + 1:
            if self.hand[r].suit == card.suit:
                run_size += 1 
            if self.hand[r].points == run_right_val + 1:
                run_right_val += 1
            r += 1

        return False ## Return true if the player goes out, false otherwise

    def go_out(self):
        return sum([card.points for card in self.hand])

    def __str__(self):
        res = ""
        res += "Hand:\n"
        for card in self.hand:
            res += str(card) + "\n"
        return res

deck = Deck()

num_players = int(input("How many players? "))
players = [Player() for _ in range(num_players)]
scores = [0 for _ in range(num_players)]

for round in range(11):

    ## Setup
    wild = str(round + 3) ## Rounds are zero indexed, 3 is wild on the first round
    if wild == 11: wild = "Jack"
    elif wild == 12: wild = "Queen"
    elif wild == 13: wild = "King"
    for player in players: player.wild = wild
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

    ## Put all cards back in the deck
    for _ in range(len(deck.discard_pile)): deck.cards.append(deck.discard_pile.pop())
        
