# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
num_range = 100
rand_num = 0
number_of_guesses = 0

# helper function to start and restart the game
def new_game():
    global number_of_guesses
    global num_range
    global rand_num
    
    print ''
    print 'New game. Range is 0 to',num_range
    
    # generating random number in range
    rand_num = random.randrange(0, num_range)
    
    # determining number of guesses
    # 2 ** n >= high - low + 1
    n = math.log(num_range + 1, 2)
    number_of_guesses = int (math.ceil(n) + 1)

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    guess_num = int(guess)
    global number_of_guesses
    global rand_num
    
    print ''
    print 'Guess was', guess_num
    
    # check if player run out of guesses
    if number_of_guesses > 0:
        number_of_guesses = number_of_guesses - 1
        print 'Number of remaining guesses is', number_of_guesses
    else:
        print 'You lost!.'
        print 'Number was', rand_num
        new_game()
        return

    # give player the hints and check if he/she won
    if rand_num > guess_num:
        print 'Higher!'
    if rand_num < guess_num:
        print 'Lower!'
    if guess_num == rand_num:
        print 'Correct!'
        new_game()
    

# create frame
frame = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements
frame.add_button("Range is [0,100]",range100,200)
frame.add_button("Range is [0,1000]",range1000,200)
frame.add_input("Enter a guess",input_guess,200)
frame.add_button("Restart game",new_game,200)

# call new_game and start frame
new_game()
frame.start()

# always remember to check your completed program against the grading rubric

