# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s,
    K_a,
    K_d,

)
TEXTCOLOR = (255,255,255)

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# Initialize pygame
pygame.init()

#debug fields
ignorecollision = False
allowaddenemy = False

#screen information
#screenobejct = pygame.display.Info()
#pygame.display.set_mode((screenobejct.current_w, screenobejct.current_h))
#pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# Define constants for the screen width and height
info = pygame.display.Info()
print(info)
SCREEN_WIDTH  = info.current_w
SCREEN_HEIGHT = info.current_h


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self,player2=False):
        super(Player, self).__init__()
        if not player2:
            self.surf = pygame.image.load('image/car1.png').convert()
        if player2:
            self.surf = pygame.image.load('image/car21.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.topleft = (50, 50)

    # Move the sprite based on keypresses
    def update(self, pressed_keys,player2=False):
        if not player2:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
                #move_up_sound.play()
            else:
            # if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
                #move_down_sound.play()
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
        if player2:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, -5)
                #move_up_sound.play()
            else:
            # if pressed_keys[K_s]:
                self.rect.move_ip(0, 5)
                #move_down_sound.play()
            if pressed_keys[K_a]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_d]:
                self.rect.move_ip(5, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load('image/bitcoin1.png'), (20, 20)).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class BitCoin(pygame.sprite.Sprite):
    image = pygame.image.load('image/bitcoin1.png')
    def __init__(self):
        super(BitCoin, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load('image/bitcoin1.png'), (20, 20)).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT-50),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right <0:
            self.kill()


# Setup for sounds, defaults are good
pygame.mixer.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDBITCOIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBITCOIN, 1000)

# Create our 'player'
player = Player()
player2 = Player(player2=True)
# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
benefits = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(player2)
# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
#pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
#pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
#move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
#move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
#collision_sound = pygame.mixer.Sound("Collision.ogg")


# Set the base volume for all sounds
#move_up_sound.set_volume(0.5)
#move_down_sound.set_volume(0.5)
#collision_sound.set_volume(0.5)

# Variable to keep our main loop running
running = True
counter1 =0 
counter2= 0 
# Our main loop
sysfont = pygame.font.get_default_font()
font = font = pygame.font.SysFont(None, 48)
drawText('Score: ', font, screen, (10), (10))
pygame.display.update()

while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY and allowaddenemy:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDBITCOIN:
            # Create the new cloud, and add it to our sprite groups
            new_bitcoin = BitCoin()
            benefits.add(new_bitcoin)
            all_sprites.add(new_bitcoin)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player2.update(pressed_keys,player2=True)
    # Update the position of our enemies and clouds
    enemies.update()
    benefits.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies) and not ignorecollision:
        # If so, remove the player
        player.kill()

        # Stop any moving sounds and play the collision sound
        #move_up_sound.stop()
        #move_down_sound.stop()
        #collision_sound.play()

        # Stop the loop
        running = False
    if(benefits):
        for bit in pygame.sprite.spritecollide(player,benefits,dokill=True):
            counter1+=1
        for bit in pygame.sprite.spritecollide(player2,benefits,dokill=True):
            counter2+=1
    largeFont = pygame.font.SysFont('comicsans', 30) # Font object
    text = largeFont.render('Score: ' + str(counter1), 1, (0,0,0)) # create our text
    screen.blit(text, (0, 0))
    largeFont = pygame.font.SysFont('comicsans', 30) # Font object
    text = largeFont.render('Score: ' + str(counter2), 1, (0,0,0)) # create our text
    screen.blit(text, (0, 500))
    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()