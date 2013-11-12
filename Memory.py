# implementation of card game - Memory

import simplegui
import random

NUMBERS = []
EXPOSED = []
CARD_POS = []
TURNS = 0
CARD_WIDTH = 40
time = 0
num_exposed_pairs = 0
is_finished = False

# Generates the list with 8 pairs of shuffled numbers
def create_list_numbers():
    list_of_numbers = []
    list_of_numbers.extend(range(0,8))
    list_of_numbers.extend(range(0,8))
    
    random.shuffle(list_of_numbers)
    
    return list_of_numbers

# Initialize variables and lists
def new_game():
    global NUMBERS, EXPOSED, TURNS, STATE, time, num_exposed_pairs, is_finished
    
    STATE = 0
    TURNS = 0
    label.set_text("Turns: " + str(TURNS))
    NUMBERS = create_list_numbers()
    
    time = 0
    timer.stop()
    num_exposed_pairs = 0
    is_finished = False
    
    # Set all cards as unexposed
    l = []
    for x in range(16):
        l.append(False)
    EXPOSED = l

# On click it will expose numbers and if they match
# then they stay exposed. It also adds turns
def mouseclick(pos):
    global EXPOSED,NUMBERS, STATE, TURNS, card1, card2, num_exposed_pairs, is_finished
    
    # Start timer with first click. If finished just ignore
    if timer.is_running():
        pass
    else:
        if is_finished:
            pass
        else:
            timer.start()
    
    x = 20
    for i in range(0,len(NUMBERS)):
        # At position 'x' is middle of card, so click position 
        # should be around middle of selected card
        if (pos[0] >= (x - (CARD_WIDTH/2))) and (pos[0] < (x + (CARD_WIDTH/2))):
            # user haven't clicked on card so no point of trying to do anything
            if ((pos[1] < 5) or (pos[1] > 95)):
                break
            if EXPOSED[i]:
                # If already exposed card, then we ignore
                pass
            else:
                EXPOSED[i] = True
                if STATE == 0:
                    # All cards are unexposed
                    STATE = 1
                    card1 = i
                    EXPOSED[i] = True
                elif STATE == 1:
                    # First card exposed
                    STATE = 2
                    card2 = i
                    EXPOSED[i] = True
                    TURNS = TURNS + 1
                    label.set_text("Turns: " + str(TURNS))
                    # if all pairs exposed, stop timer and finish
                    if num_exposed_pairs == ((len(NUMBERS)/2)-1):
                            timer.stop()
                            is_finished = True         
                else:
                    # Second card exposed
                    if NUMBERS[card1] == NUMBERS[card2]:
                        EXPOSED[card1] = True
                        EXPOSED[card2] = True
                        # another pair found
                        num_exposed_pairs = num_exposed_pairs + 1
                    else:
                        EXPOSED[card1] = False
                        EXPOSED[card2] = False
                    STATE = 1
                    card1 = i
        # Middle of next card is just 50 points to right
        x = x + 50

# Timer method
def timer_handler():
    global time
    time = time + 1
    
# Draw all good stuff
def draw(c):
    num_x_pos = 5
    card_x_pos = 20

    # Draw all numbers and lines(cards) above them if unexposed
    for n in range(len(NUMBERS)):
        c.draw_text(str(NUMBERS[n]),[num_x_pos,70],70,"White")
        num_x_pos += 50
        if EXPOSED[n]:
            pass
        else:
            c.draw_line([card_x_pos,5],[card_x_pos,95],CARD_WIDTH, "Blue")
        card_x_pos += 50
    
    # Print time
    time_label.set_text("Time: " + str(time) + " seconds")
    # If game finished, print message
    if is_finished:
        c.draw_text("Congratulations, you finished with " 
                    + str(TURNS) + " turns in " 
                    + str(time) + " seconds",(10,140),30,"White")

frame = simplegui.create_frame("Memory", 793, 150)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns: " + str(TURNS))

time_label = frame.add_label("Time: " + str(time) + " seconds")
timer = simplegui.create_timer(1000, timer_handler)

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()