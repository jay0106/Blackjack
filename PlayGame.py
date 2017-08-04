import random
import sys


class Player(object):

    def __init__(self, amount=100):
        self.player_cards = []
        self.amount = amount
        self.user_bet = 0

    def clear_player_cards(self):
        del self.player_cards[:]

    def set_amount(self, new_amount):
        self.amount = new_amount

    def get_amount(self):
        return float(self.amount)

    def add_amount(self, amount_to_add):
        self.amount += amount_to_add

    def subtract_amount(self, amount_to_subtract):
        self.amount -= amount_to_subtract

    def current_card_value(self, value):
        self.player_cards.append(value)
        return self.player_cards

    def current_bet(self, bet):
        self.user_bet = bet


class Dealer(object):

    # full deck to be loaded
    deck = []

    def __init__(self):
        self.clear_deck()
        self.dealer_cards = []

    def clear_deck(self):
        del Dealer.deck[:]
        self.make_deck()

    def clear_dealer_cards(self):
        del self.dealer_cards[:]

    def make_deck(self):
        cards = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
        for i in range(len(cards)):
            Dealer.deck.append(('clubs', cards[i]))
            Dealer.deck.append(('diamonds', cards[i]))
            Dealer.deck.append(('hearts', cards[i]))
            Dealer.deck.append(('spades', cards[i]))

    def random_card(self):
        random_card_index = random.choice(range(len(Dealer.deck)))
        random_card_value = Dealer.deck[random_card_index]
        return random_card_value, random_card_index

    def remove_card(self, card_index):
        Dealer.deck.pop(card_index)

    def current_card_value(self, value):
        self.dealer_cards.append(value)
        return self.dealer_cards

    def __len__(self):
        return len(Dealer.deck)

    def __str__(self):
        card = []
        for i in range(len(Dealer.deck)):
            card.append(Dealer.deck[i])
        return str(card)


# Time to play the game

def check_balance():
    if p1.get_amount() <= 0:
        while True:
            try:
                add_money = int(raw_input("Your balance is low, You must add in money. "
                                          "Enter your amount: "))
                if add_money <= 0:
                    print "Enter in valid number"
            except:
                print "Enter in valid number"
            else:
                p1.add_amount(add_money)
                break


def clear_for_next_round():
    d1.clear_deck()
    p1.clear_player_cards()
    d1.clear_dealer_cards()


def draw_player():
    (card_value, card_index) = d1.random_card()

    current_player_card = p1.current_card_value(card_value[1])
    print "Current Player's Cards: {}".format(current_player_card)
    d1.remove_card(card_index)
    player_total = 0
    for i in range(len(current_player_card)):
        if current_player_card[i] == "Ace" or current_player_card[i] == "Jack" or\
                        current_player_card[i] == "Queen" or current_player_card[i] == "King":
            real_card_value = 11
        else:
            real_card_value = current_player_card[i]
        player_total += real_card_value

    if player_total > 21:
        print "Player Busted"
        p1.subtract_amount(p1.user_bet)
        print "Current Balance: $%1.2f" % p1.get_amount()
        clear_for_next_round()
        play()
    return player_total


def draw_dealer():
    (dealer_card_value, dealer_card_index) = d1.random_card()
    current_dealer_card = d1.current_card_value(dealer_card_value[1])
    print "Current Dealer's Cards: {}".format(current_dealer_card)
    d1.remove_card(dealer_card_index)

    player_total = draw_player()
    dealer_total = 0
    for i in range(len(current_dealer_card)):
        if current_dealer_card[i] == "Ace" or current_dealer_card[i] == "Jack" or\
                        current_dealer_card[i] == "Queen" or current_dealer_card[i] == "King":
            real_card_value = 11
        else:
            real_card_value = current_dealer_card[i]
        dealer_total += real_card_value

        if dealer_total > 21:
            print "Dealer Busted"
            p1.add_amount(p1.user_bet)
            clear_for_next_round()
            play()
        if dealer_total == player_total:
            print "Push"
            clear_for_next_round()
            play()
        if dealer_total > player_total:
            print "Dealer Win"
            p1.subtract_amount(p1.user_bet)
            clear_for_next_round()
            play()
        if dealer_total < player_total:
            print "Player Win"
            p1.add_amount(p1.user_bet)
            clear_for_next_round()
            play()

def all_bets_in():
    draw_dealer()
    draw_player()

    while True:
        print "\nh - hit\ns - stand"
        player_decision = ""
        while not(player_decision == 'H' or player_decision == "S"):
            player_decision = raw_input("Make a choice: ")[0].upper()

        if player_decision == 'H':
            draw_player()
            continue
        else:
            draw_dealer()


def play():
    while True:
        check_balance()
        print 'v - View Balance'
        print 'p - Place Bet'
        print 'q - Quit Game'
        player_choice = ''

        while not (player_choice == 'V' or player_choice == 'Q' or player_choice == 'P'):
            player_choice = raw_input("Enter your Choice: ").upper()

        if player_choice == 'V':
            print "Balance: $%1.2f" % (p1.get_amount())
        elif player_choice == 'Q':
            sys.exit()
        else:
            while True:
                try:
                    player_bet = int(raw_input("How much would you like to bet?: "))
                    if player_bet <= 0 or player_bet > p1.get_amount():
                        print "Enter in valid bet"
                        continue
                except:
                    print 'Enter in valid bet'
                    continue
                else:
                    p1.current_bet(player_bet)
                    break
            print "Time To Draw cards. Good Luck!"
            all_bets_in()

while True:
    try:
        player_amount = int(raw_input("Enter in your Amount: "))
    except:
        continue
    else:
        p1 = Player(player_amount)
        d1 = Dealer()
        print "Let's Play!"
        play()
        break


