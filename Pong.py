# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = [0 , HEIGHT / 2]
paddle2_pos = [WIDTH, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
paddle_acc = 4


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    horizontal = random.randrange(120, 240) / 60
    vertical = random.randrange(60, 180) / 60
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    if direction == RIGHT:
        ball_vel[0] = horizontal
        ball_vel[1] = - vertical
    elif direction == LEFT:
        ball_vel[0] = - horizontal
        ball_vel[1] = - vertical


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2
    
    # reset paddles to center
    paddle1_pos = [0 , (HEIGHT / 2) - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT]
    
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    # randomly pick which side ball goes first
    direction = random.randint(0,1)
    if direction == 1:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    
    # draws field
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # calculate ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #####################################
    # Decide what to do on sides of field
    #####################################
    # left side
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        """
        if ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= (paddle1_pos[1] + PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0] * 1.1
        """
        # added BALL_RADIUS/2 which kind of extend paddle. It looks more realistic :-D
        if ball_pos[1] >= (paddle1_pos[1] - BALL_RADIUS/2) and ball_pos[1] <= (paddle1_pos[1] + PAD_HEIGHT + BALL_RADIUS/2):
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            spawn_ball(RIGHT)
            score2 += 1
    # right side
    elif ball_pos[0] >= (WIDTH - (BALL_RADIUS + PAD_WIDTH)):
        """
        if ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= (paddle2_pos[1] + PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0] * 1.1
        """
        # added BALL_RADIUS/2
        if ball_pos[1] >= (paddle2_pos[1] - BALL_RADIUS/2) and ball_pos[1] <= (paddle2_pos[1] + PAD_HEIGHT + BALL_RADIUS/2):
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            spawn_ball(LEFT)
            score1 += 1
    # top side
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]        
    # bottom side
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")        

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    # this make sure that paddles stay in screen
    if paddle1_pos[1] <= 0:
        paddle1_pos[1] = 0
    if paddle1_pos[1] + PAD_HEIGHT >= HEIGHT:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    if paddle2_pos[1] <= 0:
        paddle2_pos[1] = 0
    if paddle2_pos[1] + PAD_HEIGHT >= HEIGHT:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
        
    # draw paddles
    c.draw_line([paddle1_pos[0],paddle1_pos[1]],[paddle1_pos[0],paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH , "White")
    c.draw_line([paddle2_pos[0],paddle2_pos[1]],[paddle2_pos[0],paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH , "White")
    
    # draw scores
    c.draw_text(str(score1), [WIDTH / 2 - 90, 80], 50, 'White')
    c.draw_text(str(score2), [WIDTH / 2 + 70, 80], 50, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle_acc
    
    acc = paddle_acc
    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel, paddle_acc
    
    acc = paddle_acc
    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel -= acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel += acc

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', new_game, 200)

# start frame
new_game()
frame.start()

