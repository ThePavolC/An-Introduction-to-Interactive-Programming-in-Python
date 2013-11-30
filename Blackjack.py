# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

blink_color = "Green"
message = ""
action_message = ""
score_message = ""

# initialize some useful global variables
in_play = False
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = "Hand contains "
        for c in self.cards:
            s += str(c)
            s += " "
        return s

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        has_ace = False
        for c in self.cards:
            if c.get_rank() == 'A':
                has_ace = True
            value += VALUES[c.get_rank()]
        if has_ace and (value + 10) <= 21:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        x = pos[0]
        for card in self.cards:
            card.draw(canvas,[x,pos[1]])
            x += CARD_SIZE[0] + 5
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for r in RANKS:
            for s in SUITS:
                self.cards.append(Card(s,r))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        s = "Deck contains "
        for card in self.cards:
            s += str(card)
            s += " "
        return s

#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, message, action_message, score_message, score
    
    # if Deal pressed in middle of the game
    if in_play:
        score -= 1
        message = "You lost the round"
        print "You lost the round"

    message = ""
        
    action_message = "Hit or Stand?"
    score_message = "Score:" + str(score)
    
    # Prepare Deck, Player/Dealer and lets play
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    in_play = True

# Add card to player. If more than 21 then busted
def hit():
    global player_hand, deck, score, in_play
    
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            score -= 1
            in_play = False
            show_message(player = True, busted = True)

# If Stand, add cards to Dealer and evaluate the result
def stand():
    global dealer_hand,player_hand,deck,in_play,score
    
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        
        if dealer_hand.get_value() > 21:
            score += 1
            in_play = False
            show_message(player = False, busted = True)
        elif player_hand.get_value() > dealer_hand.get_value():
            score += 1
            in_play = False
            show_message(player = True, busted = False)
        elif dealer_hand.get_value() <= 21:
            score -= 1
            in_play = False
            show_message(player = False, busted = False)

# Method handling messages. 
def show_message(player, busted):
    global message, action_message, score_message
    
    if busted:
        if player:
            score_message = "Score:" + str(score)
            message = "Player Busted, Dealer Wins!"
            action_message = "New Deal?"
        else:
            score_message = "Score:" + str(score)
            message = "Dealer Busted, Player Wins!"
            action_message = "New Deal?"
    else:
        if player:
            score_message = "Score:" + str(score)
            message = "Player Wins!"
            action_message = "New Deal?"
        else:
            score_message = "Score:" + str(score)
            message = "Dealer Wins!"
            action_message = "New Deal?"
    pass

# Scheduler handler a.k.a blinking Blackjack
def change_color_timer():
    global blink_color, message
    
    if blink_color == '#CCFF99':
        blink_color = 'Green'
    else:
        blink_color = '#CCFF99'
            
# draw handler    
def draw(canvas):
      # print Blackjack
    canvas.draw_text('Blackjack Game', (9, 59), 51, blink_color)
    canvas.draw_text('Blackjack Game', (10, 60), 50, 'Black')
    canvas.draw_text('Blackjack Game', (12, 61), 50, 'White')
      # print score
    canvas.draw_text(score_message, (10, 100), 30, 'Black')
    canvas.draw_text(score_message, (12, 101), 30, 'White')
      #print Dealer
    canvas.draw_text('Dealer', (10, 150), 40, 'Black')
    canvas.draw_text('Dealer', (12, 151), 40, 'White')
    dealer_hand.draw(canvas,[10,165])
    if in_play:
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        card_pos = [10 + CARD_BACK_CENTER[0], 165 + CARD_BACK_CENTER[1]]
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, card_pos, CARD_SIZE)
      # print Player
    canvas.draw_text('Player', (10, 300), 40, 'Black')
    canvas.draw_text('Player', (12, 301), 40, 'White')
    player_hand.draw(canvas,[10,315])
      # Action messages
    canvas.draw_text(action_message, (10, 450), 20, 'White')
    canvas.draw_text(message, (10, 470), 20, 'White')
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

timer = simplegui.create_timer(500, change_color_timer)
timer.start()

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()