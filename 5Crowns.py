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

        else:
            ## Check if it's helpful
            card = self.draw_card(deck.discard_pile)
            card_index = self.hand.index(card)

            ## These variables show the size of the run or book the card is in
            run_size = self.find_run(card, card_index)
            book_size = self.find_book(card, card_index)

            if run_size + book_size < 2: ## The discard isn't valuable, pick up from cards instead
                deck.discard_pile.append(hand.pop(card_index))
                ## No need to check if it's helpful, because we can't see it until we pick it up
                self.draw_card(deck.cards) ## Draw a card from the deck

        ## Determine what card to discard
        ## Discard something with the most points;
        ## Descend through hand until not in a run or book
        temp_index = len(self.hand) - self.num_wilds - 1
        temp_card = self.hand[temp_index]

        ## Note: Add some code to start accounting for wild cards
        while temp_index >= 0:
            run_size = self.find_run(temp_card, temp_index)
            book_size = self.find_book(temp_card, temp_index)
            if run_size + book_size > 2: ## If it has at least one other card in same book/run, keep it
                ## Traverse through the hand, skipping cards in the same book/run whichever is larger
                ## Note: Check correctness of getting the max book/run instead of the min
                temp_index -= max(self.find_run_1d(temp_card, temp_index, -1), self.find_run_1d(temp_card, temp_index, 1))
            else:
            ## If the loop finds a card that isn't in any book or run, discard it
                deck.discard_pile.append(self.hand.pop(temp_index))
                return False

        ## Note that if you have a bunch of pairs, it would consider all of them valuable
        ## I need to add some sort of logic to consider this, and also to go out if possible


        ## Otherwise do the same except with runs/books of 3 instead of two
        ## I'd make it a function, but the logic changes since I can't just do >2 like above
        temp_index = len(self.hand) - self.num_wilds - 1
        temp_card = self.hand[temp_index]

        ## Note: Modify to account for overlapping runs and books
        while temp_index >= 0:
            run_size = self.find_run(temp_card, temp_index)
            book_size = self.find_book(temp_card, temp_index)
            if run_size>2 or book_size>2: ## If it is in a run/book that can go out
                ## Traverse through the hand, skipping cards in the same book/run whichever is larger
                temp_index -= max(self.find_run_1d(temp_card, temp_index, -1), self.find_run_1d(temp_card, temp_index, 1))
            else:
            ## If the loop finds a card that isn't in any book or run, discard it
                deck.discard_pile.append(self.hand.pop(temp_index))
                return False

        ## If the loop finishes, then the player has gone out
        return True ## There is no need to call the go_out function, since the player won't accumulate any points

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

    def go_out(self): ## Note: This needs to change since no out_hand variable
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