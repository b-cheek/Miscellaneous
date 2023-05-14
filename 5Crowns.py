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

        ## Option 1: determine value of the discard based on the runs/books it joins
        run_size = self.find_run(card, card_index)
        book_size = self.find_book(card, card_index)

        ## Option 2: check value from a preset list of value cards

        ## Return the card to the discard pile
        deck.discard_pile.append(hand.pop(card_index)) 

        return False ## Return true if the player goes out, false otherwise

    def find_run(self, card, card_index):
        ## Determine if the card is in a run
        run_size = self.find_run_1d(card, card_index, -1) ## Add left run
        run_size += self.find_run_1d(card, card_index, 1) - 1 ## Account for duplicate "card"

        return run_size
        
    def find_run_1d(self, card, card_index, direction):
        run_size = 1
        temp = card_index + direction ## Index will move either left or right in hand, (direction = -1 or 1)
        run_end_val = card.points ## This will decrement/increment accordingly to ensure adjacent value
        while temp>=0 and temp<len(self.hand) - self.num_wilds \
            and (self.hand[temp].points - run_end_val)/direction <= 1: ## ^ continue while no jumps >direction
            ## Note that we can't multiply both sides by direction since it is not always the same sign
            ## /direction basically is like using abs(), while also scaling the difference to direction
            if self.hand[temp].suit == card.suit and self.hand[temp].points == run_end_val + direction:
                ## If it's the same suit and the next value, it's a run
                run_size += 1
                run_end_val += direction
            temp += direction
        
        return run_size

    def find_book(self, card, card_index): ## This one's easier because books are sorted together
        ## Determine if the card is in a book
        book_size = self.find_book_1d(card, card_index, -1) ## Add left book
        book_size += self.find_book_1d(card, card_index, 1) - 1 ## Account for duplicate "card"

        return book_size

    def find_book_1d(self, card, card_index, direction):
        book_size = 1
        temp = card_index + direction
        while temp>=0 and temp < len(self.hand) + self.num_wilds \
            and self.hand[temp].points == card.points:
            book_size += 1
            temp += direction

        return book_size

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