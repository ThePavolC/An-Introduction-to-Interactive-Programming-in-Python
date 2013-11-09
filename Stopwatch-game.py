# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
total_stops = 0
suc_stops = 0

# Variables used for line under text
line_x = 70
show_line = False
line_color = 'Blue'

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    milisec_num = t % 10
    sec1_num = (t / 10) % 10
    sec2_num = (t / 100) % 6
    minute_num = t / 600
    
    milisec = str(milisec_num)
    sec1 = str(sec1_num)
    sec2 = str(sec2_num)
    minute = str(minute_num)
    
    return minute + ':' + sec2 + sec1 + '.' + milisec
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    # Start timer and change color of line to blue
    global line_color
    
    timer.start()
    line_color = 'Blue'

def stop_handler():
    # Stop timer and if stopped at correct time 
    # increase successful counter.
    # Change color of line to green/red
    global time
    global total_stops
    global suc_stops
    global line_color
    
    if timer.is_running():
        timer.stop()
        total_stops = total_stops + 1
        if (time % 10) == 0:
            suc_stops = suc_stops + 1
            line_color = 'Green'
        else:
            line_color = 'Red'
    else:
        pass
    
def reset_handler():
    # Reset all global variables to default
    global time
    global total_stops
    global suc_stops
    global line_x
    
    total_stops = 0
    suc_stops = 0
    time = 0
    line_x = 70
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    # Increase time counter and size of line
    global time
    global line_x
    
    if line_x == 250:
        line_x = 70
    line_x = line_x + 18
    time = time + 1

def line_handler():
    # Toggle visibilty of line and change text on button
    global show_line
    global line_button_text
    
    if show_line:
        show_line = False
        line_button.set_text('Show line')
    else:
        show_line = True
        line_button.set_text('Hide line')
    
# define draw handler
def draw_handler(canvas):
    # Draw all stuff on canvas
    global timem
    global line_x
    global line_color
    
    canvas.draw_text(format(time),(70,150),70,'White')
    score_board = str(suc_stops) + '/' + str(total_stops)
    canvas.draw_text(score_board, (250,50),30,'White')
    
    if show_line:
        canvas.draw_line([70, 160], [line_x, 160], 10, line_color)
    else:
        canvas.draw_line([70, 160], [line_x, 160], 10, 'Black')
    
    

# create frame
frame = simplegui.create_frame('Testing', 300, 300)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.add_button('Start', start_handler, 200)
frame.add_button('Stop', stop_handler, 200)
frame.add_button('Reset', reset_handler, 200)
line_button = frame.add_button('Show line', line_handler, 200)

frame.set_draw_handler(draw_handler)

# start frame
frame.start()

