# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

# globals for game settings
SHIP_ANGLE_VEL = 0.10
SHIP_ACC = 0.15
SHIP_FRACTION = 0.95
MISSILE_VEL = 10
SCORE_POS_X = 120
SCORE_POS_Y = 50
LIVES_POS_X = 120
LIVES_POS_Y = 80

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
        self.thrust_off = self.image_center[0]
        self.thrust_on = self.image_center[0] + self.image_size[0]
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size ,self.angle)

    def update(self):
        # turn ship
        self.angle += self.angle_vel
        # get angle vector
        angle_vector =  angle_to_vector(self.angle)
        if self.thrust == True:
            # when moving change picture and play sound
            self.image_center[0] = self.thrust_on
            ship_thrust_sound.play()
            # speed up
            self.vel[0] += angle_vector[0] 
            self.vel[1] += angle_vector[1]    
        else:
            # when not moving change picture and stop sound
            self.image_center[0] = self.thrust_off
            ship_thrust_sound.rewind()
            # apply friction to slow down
            self.vel[0] *= SHIP_FRACTION
            self.vel[1] *= SHIP_FRACTION
        
        # change position
        # when out of screen
        """
        This code show ship on other side only when it is completly gone.
        So there is no "jumping" like in current version. But it is not
        same behavior as in video so it is not used. 
        
        if self.pos[0] - self.image_center[0] > WIDTH:
            self.pos[0] %= WIDTH
            self.pos[0] -= 2*self.image_center[0]
        elif self.pos[0] + self.image_center[0] < 0:
            self.pos[0] %= WIDTH
            self.pos[0] += 2*self.image_center[0]
        """
        if self.pos[0] > WIDTH:
            self.pos[0] %= WIDTH
        elif self.pos[0] < 0:
            self.pos[0] %= WIDTH
        else:
            # move according to vector and acceleration constant
            self.pos[0] += (self.vel[0] * SHIP_ACC)        
        
        # when out of screen
        """
        This code show ship on other side only when it is completly gone.
        So there is no "jumping" like in current version. But it is not
        same behavior as in video so it is not used. 
        
        if self.pos[1] - self.image_center[1] > HEIGHT:
            self.pos[1] %= HEIGHT
            self.pos[1] -= 2*self.image_center[1]
        elif self.pos[1] + self.image_center[1] < 0:
            self.pos[1] %= HEIGHT
            self.pos[1] += 2*self.image_center[1]
        """
        if self.pos[1] > HEIGHT:
            self.pos[1] %= HEIGHT
        elif self.pos[1] < 0:
            self.pos[1] %= HEIGHT
        else:
            # move according to vector and acceleration constant
            self.pos[1] += (self.vel[1] * SHIP_ACC)
    
    # turn ship left
    def turn_left(self):
        self.angle_vel -= SHIP_ANGLE_VEL
    
    # turn ship right
    def turn_right(self):
        self.angle_vel += SHIP_ANGLE_VEL
    
    # stop turning. Used when key-up action
    def stop_turning(self):
        self.angle_vel = 0

    # set thrust
    def thrusters(self, t):
        self.thrust = t
    
    # shooting action
    def shoot(self):
        global a_missile
        
        # set missile to top of ship
        vector = angle_to_vector(self.angle)
        x = self.pos[0] + vector[0]*(self.image_size[0]/2)
        y = self.pos[1] + vector[1]*(self.image_size[1]/2)
        
        # fire at this velocity
        vel_x = (self.vel[0]*0.01 + vector[0]) * MISSILE_VEL
        vel_y = (self.vel[1]*0.01 + vector[1]) * MISSILE_VEL
        """
        I believe that in assignemnet they wanted something like this
        but I didn't like how it behave so I modified it little bit.
        
        vel_x = self.vel[0] + vector[0] * MISSILE_VEL
        vel_y = self.vel[1] + vector[1] * MISSILE_VEL
        """
        
        # Fire!!!
        a_missile = Sprite([x,y], [vel_x,vel_y], 0, 0, missile_image, missile_info, missile_sound)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size ,self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        """
        This code show ship on other side only when it is completly gone.
        So there is no "jumping" like in current version. But it is not
        same behavior as in video so it is not used. 
        
        if (self.pos[0] - self.image_center[0] > WIDTH):
            self.pos[0] %= WIDTH 
            self.pos[0] -= 2*self.image_center[0]
        elif (self.pos[0] + self.image_center[0] < 0):
            self.pos[0] %= WIDTH 
            self.pos[0] += 2*self.image_center[0]
        if (self.pos[1] - self.image_center[1] > HEIGHT):
            self.pos[1] %= HEIGHT
            self.pos[1] -= 2*self.image_center[1]
        elif (self.pos[1]+ self.image_center[1] < 0):
            self.pos[1] %= HEIGHT
            self.pos[1] += 2*self.image_center[1]
        """
        if (self.pos[0] > WIDTH):
            self.pos[0] %= WIDTH 
        elif (self.pos[0] < 0):
            self.pos[0] %= WIDTH 
        if (self.pos[1] > HEIGHT):
            self.pos[1] %= HEIGHT
        elif (self.pos[1] < 0):
            self.pos[1] %= HEIGHT

# key down handler
def key_down_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn_left()
    if key == simplegui.KEY_MAP['right']:
        my_ship.turn_right()
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(True)
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

# key up handler
def key_up_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.stop_turning()
    if key == simplegui.KEY_MAP['right']:
        my_ship.stop_turning()
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(False)

def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # Score and Lives text
    canvas.draw_text('Score: ' + str(score), [WIDTH-SCORE_POS_X, SCORE_POS_Y], 30, 'White')
    canvas.draw_text('Lives: ' + str(lives), [WIDTH-LIVES_POS_X, LIVES_POS_Y], 30, 'White')
    
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    
    new_position_x = random.randint(0,WIDTH)
    new_position_y = random.randint(0,HEIGHT)
    new_rot_vel = random.random() * 0.1
    if random.random() > 0.5:
        new_rot_vel *= -1
    new_vel_x = random.random()
    if random.random() > 0.5:
        new_vel_x *= -1
    new_vel_y = random.random()
    if random.random() > 0.5:
        new_vel_y *= -1
    a_rock = Sprite([new_position_x, new_position_y], [new_vel_x, new_vel_y], 0, new_rot_vel, asteroid_image, asteroid_info)
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# set timer for asteroids
timer = simplegui.create_timer(1000, rock_spawner)
timer.start()

# setting key handlers
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0], 0, 0.01, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

