import random

# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        print 'Incorrect number:',number

    
def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print 'Incorrect name:',name

def rpsls(name): 
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    
    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    # print names
    print 'Player chooses',name
    print 'Computer chooses',comp_name
    
    # compute difference of player_number and comp_number modulo five
    winner_number = (player_number - comp_number) % 5
    # use if/elif/else to determine winner
    if (winner_number == 1) or (winner_number == 2):
        print 'Player wins!'
    elif (winner_number == 3) or (winner_number == 4):
        print 'Computer wins!'
    else:
        print 'Player and computer tie!'
    
    print ''

    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric



