# Import the pygame module
import pygame
import time
# Import random for random numbers
import random
import keyboard
import socket
import threading
import Player2Control


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
    KEYUP,
    QUIT,
    K_w,
    K_s,
    K_a,
    K_d,

)

# GLOBAL DEFINES

TEXTCOLOR = (255, 255, 255)
BACKGROUND_COLOR = (135, 206, 250)
COLLIDE_ENEMY_POINTS = 10  # losing points when colliding with an enemy
COLLISION_DELTA = 10  # amount of frames to allow player to not lose points since last collision with ground
GROUND_PENALTY = 10
NUM_OF_PLAYER_IMGS = 10
CLOUDS = True
LOADING_SCREEN = False
BACKGROUND_DELAY = 5

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Initialize pygame
pygame.init()

# debug fields
# global variables:
groundheight = 100
background_time = 0  # current background state running timer.
# debug fields
ignorecollision = False
allowaddenemy = True

# screen information
# screenobejct = pygame.display.Info()
# pygame.display.set_mode((screenobejct.current_w, screenobejct.current_h))
# pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# Define constants for the screen width and height
info = pygame.display.Info()
# print(info)
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

#define server socket
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

#listening thread

def StartServer():
    while not running:
        time.sleep(0.1)
    while running:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]

        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)


def CloseSocket():
    print("closing socket")
    UDPServerSocket.close()

listening_thread = threading.Thread(target=StartServer)
closesocket_thread = threading.Thread(target=CloseSocket)
# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, player2=False):
        self.ground_counter = COLLISION_DELTA
        self.score = 0
        self.alive = True
        self.fire_is_on = True
        super(Player, self).__init__()
        self.state = 0
        if not player2:
            if self.fire_is_on:
                self.surf = player1_on_arr[0]
            else:
                self.surf = player1_off_arr[0]
        if player2:
            if self.fire_is_on:
                self.surf = player2_on_arr[0]
            else:
                self.surf = player2_off_arr[0]
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        # print(self.rect.size)
        self.rect.y = SCREEN_HEIGHT / 2  # for now start from middle
        self.health = 100

    def draw_health(self, surf):
        if (self.health != 0):
            health_rect = pygame.Rect(0, 0, 23, 7)
        else:
            health_rect = pygame.Rect(0, 0, 0, 0)
        health_rect.midbottom = self.rect.centerx, (self.rect.bottom + 10)
        max_health = 100
        if (self.alive):
            draw_health_bar(surf, health_rect.topleft, health_rect.size,
                            (0, 0, 0), (255, 0, 0), (0, 255, 0), self.health / max_health)

    def draw_score(self, surf):
        if (self.health != 0):
            health_rect = pygame.Rect(0, 0, 23, 7)
        else:
            health_rect = pygame.Rect(0, 0, 0, 0)
        health_rect.midbottom = self.rect.centerx, (self.rect.top - 25)
        max_health = 100
        if (self.alive):
            draw_score_text(surf, health_rect.topleft, health_rect.size,
                            (0, 0, 0), (255, 0, 0), (0, 255, 0), self.score)

    # Move the sprite based on keypresses
    def update(self, pressed_keys, player2=False):
        if not player2:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
                self.fire_is_on = True
                # self.state = max(0, self.state - 1)
                self.state = max(0, self.state - 1)

                # move_up_sound.play()
            else:
                # if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
                self.fire_is_on = False
                # self.state = max(9, self.state + 1)
                self.state = min(self.state + 1, NUM_OF_PLAYER_IMGS - 1)
                # print('state is ' + str(self.state))
                # move_down_sound.play()
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
            # update the player surface and rectangle
            if self.fire_is_on:
                self.surf = player1_on_arr[self.state]
            else:
                self.surf = player1_off_arr[self.state]
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        if player2:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, -5)
                self.state = max(0, self.state - 1)
                self.fire_is_on = True

                # move_up_sound.play()
            else:
                # if pressed_keys[K_s]:
                self.rect.move_ip(0, 5)
                self.state = min(self.state + 1, NUM_OF_PLAYER_IMGS - 1)
                self.fire_is_on = False
                # move_down_sound.play()
            if pressed_keys[K_a]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_d]:
                self.rect.move_ip(5, 0)
            # update the player surface and rectangle
            if self.fire_is_on:
                self.surf = player2_on_arr[self.state]
            else:
                self.surf = player2_off_arr[self.state]
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT - groundheight + 10:
            self.rect.bottom = SCREEN_HEIGHT - groundheight + 10


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load('image/angrybird.png'), (20, 20)).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
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

    def __init__(self, bitcoin_size=40):
        super(BitCoin, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load('image/bitcoin1.png'),
                                           (bitcoin_size, bitcoin_size)).convert_alpha()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated
        self.coin_size = bitcoin_size
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(new_coin_size, SCREEN_HEIGHT - groundheight - bitcoin_size),
            )
        )

    def get_coin(self):
        return self.coin_size

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Define the Ground object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Ground(pygame.sprite.Sprite):

    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('image/ground1.png'), (SCREEN_WIDTH, groundheight))
        super(Ground, self).__init__()
        self.surf = self.image.convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - groundheight

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        return


# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("image/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(30, SCREEN_HEIGHT - groundheight - 30),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


def draw_health_bar(surf, pos, size, borderC, backC, healthC, progress):
    pygame.draw.rect(surf, backC, (*pos, *size))
    pygame.draw.rect(surf, borderC, (*pos, *size), 1)
    innerPos = (pos[0] + 1, pos[1] + 1)
    innerSize = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
    pygame.draw.rect(surf, healthC, rect)
    largeFont = pygame.font.SysFont('comicsans', 10)  # Font object
    text = largeFont.render(str(int(progress * 100)), 1, (255, 255, 255))  # create our text
    screen.blit(text, (round(innerPos[0]), round(innerPos[1])))


def draw_score_text(surf, pos, size, borderC, backC, healthC, score):
    largeFont = pygame.font.SysFont('comicsans', 30, bold=True)  # Font object
    text = largeFont.render(str(int(score)), 1, (255, 84 * 256 / 100, 0))  # create our text
    screen.blit(text, (round(pos[0]), round(pos[1]) - 15))


# Setup for sounds, defaults are good
pygame.mixer.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
Player2Control.SendCommand("Go right!")
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.transform.scale(pygame.image.load('image/angrybird.png'), (20, 20)).convert_alpha()
bg = pygame.image.load("image\space.jpg")
opening_bg1 = pygame.transform.scale(pygame.image.load("image\Background_1.png"), (SCREEN_WIDTH,SCREEN_HEIGHT)).convert_alpha()
opening_bg2 = pygame.transform.scale(pygame.image.load("image\Background_2.png"), (SCREEN_WIDTH,SCREEN_HEIGHT)).convert_alpha()
opening_bg3 = pygame.transform.scale(pygame.image.load("image\Background_3.png"), (SCREEN_WIDTH,SCREEN_HEIGHT)).convert_alpha()

# images
player1_off_arr = []
player1_on_arr = []
player2_off_arr = []
player2_on_arr = []
for i in range(NUM_OF_PLAYER_IMGS):
    curr_player1_off_img = pygame.transform.scale(pygame.image.load('image/player1_off' + str(i) + '.png'),
                                                  (50, 100)).convert_alpha()
    player1_off_arr.append(curr_player1_off_img)
    curr_player1_on_img = pygame.transform.scale(pygame.image.load('image/player1_on' + str(i) + '.png'),
                                                 (50, 100)).convert_alpha()
    player1_on_arr.append(curr_player1_on_img)
    curr_player2_off_img = pygame.transform.scale(pygame.image.load('image/player2_off' + str(i) + '.png'),
                                                  (50, 100)).convert_alpha()
    player2_off_arr.append(curr_player2_off_img)
    curr_player2_on_img = pygame.transform.scale(pygame.image.load('image/player2_on' + str(i) + '.png'),
                                                 (50, 100)).convert_alpha()
    player2_on_arr.append(curr_player2_on_img)

    # print(player1_off_arr)

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 2000)
if CLOUDS:
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)
ADDBITCOIN = pygame.USEREVENT + 3
KEYLEFT_EVENT = pygame.USEREVENT + 4
KEYRIGHT_EVENT = pygame.USEREVENT + 5
pygame.time.set_timer(ADDBITCOIN, 1000)

# create needed items

player = Player()
player1_group = pygame.sprite.Group()
player1_group.add(player)
player2 = Player(player2=True)
player2_group = pygame.sprite.Group()
player2_group.add(player2)
ground = Ground()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
ground_group = pygame.sprite.Group()
ground_group.add(ground)
enemies = pygame.sprite.Group()
benefits = pygame.sprite.Group()
if CLOUDS:
    clouds = pygame.sprite.Group()

# enemies.add(ground)
all_sprites = pygame.sprite.Group()
all_sprites.add(ground)
all_sprites.add(player)
all_sprites.add(player2)
# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
# pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
# pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
# move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
# move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
blast_off_sound = pygame.mixer.Sound("music\\1.wav")
collision_sound = pygame.mixer.Sound("music\Collision.ogg")
boom_sound = pygame.mixer.Sound("music//boom.ogg")
# Set the base volume for all sounds
# move_up_sound.set_volume(0.5)
# move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)
boom_sound.set_volume(0.5)
blast_off_sound.set_volume(1)
# Variable to keep our main loop running
running = True

listening_thread.start()



# Our main loop
sysfont = pygame.font.get_default_font()
font = font = pygame.font.SysFont(None, 48)
progress = 1
maxwidth = 20
key_rel = 0
last = None
countdown = 6
if (LOADING_SCREEN):
    completed_right         = False
    completed_left          = False
    completed_up            = False
    check_up_in_progress    = True
    check_right_in_progress = False
    check_left_in_progress  = False
    pygame.event.clear()

    screen.blit(opening_bg1, (0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.blit(opening_bg2, (0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.blit(opening_bg3, (0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)

    while True:
        event = pygame.event.wait()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_RIGHT]:
            pygame.event.post(pygame.event.Event(KEYRIGHT_EVENT))
        if keys_pressed[K_LEFT]:
            pygame.event.post(pygame.event.Event(KEYLEFT_EVENT))
        if completed_right and completed_left and completed_up:
            break
        if event.type == KEYUP and check_up_in_progress:
            completed_up = True
            check_up_in_progress = False
            check_right_in_progress = True
            pygame.event.clear()
            print("check up passed")
        if event.type == KEYRIGHT_EVENT and check_right_in_progress:
            completed_right = True
            check_right_in_progress = False
            check_left_in_progress = True
            print("check right passed")
            pygame.event.clear()
        if event.type == KEYLEFT_EVENT and check_left_in_progress:
            completed_left = True
            check_left_in_progress = False
            print("check left passed")
            pygame.event.clear()



    channel = blast_off_sound.play()
    while channel.get_busy():
        if (countdown >= 0):
            drawText(str(countdown), font, screen, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 4) + 50 * (6 - countdown))
            pygame.display.update()
            countdown -= 1
        else:
            pygame.display.update()
        pygame.time.wait(1000)
# drawText(str("IGNITION!"), font, screen, (SCREEN_WIDTH/2)-100, (SCREEN_HEIGHT/4)+50*(6-countdown))

while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
                closesocket_thread.start()
        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False
            closesocket_thread.start()
        # Should we add a new enemy?
        elif event.type == ADDENEMY and allowaddenemy:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDBITCOIN:
            # Create the new cloud, and add it to our sprite groups
            new_coin_size = random.randint(10, 50)
            new_bitcoin = BitCoin(new_coin_size)
            benefits.add(new_bitcoin)
            all_sprites.add(new_bitcoin)
        elif CLOUDS:
            if (event.type == ADDCLOUD):
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        # Should we add a new cloud?

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    player1_group.update(pressed_keys)
    player2_group.update(pressed_keys, player2=True)

    # Update the position of our enemies and clouds
    enemies.update()
    benefits.update()
    if CLOUDS:
        clouds.update()

    keys = ["a", "w", "d", "a", "a", "d", "d"]
    if key_rel == 2:
        if last:
            keyboard.release(last)
        key_rel = 0
    last = random.choice(keys)
    keyboard.press(last)
    key_rel += 1

    screen.blit(bg, (0, 0))

    # Draw all our sprites
    for entity in enemies:
        screen.blit(entity.surf, entity.rect)
    if CLOUDS:
        for entity in clouds:
            screen.blit(entity.surf, entity.rect)
    for entity in benefits:
        screen.blit(entity.surf, entity.rect)

    for entity in player1_group:
        screen.blit(entity.surf, entity.rect)
    for entity in player2_group:
        screen.blit(entity.surf, entity.rect)
    for entity in ground_group:
        screen.blit(entity.surf, entity.rect)
    # screen.blit(player.surf, player.rect)
    # screen.blit(player2.surf, player2.rect)
    # screen.blit(ground.surf, ground.rect)
    player.draw_health(screen)
    player.draw_score(screen)
    player2.draw_health(screen)
    player2.draw_score(screen)
    ##player 1 collision with enemy##
    if pygame.sprite.spritecollide(player, enemies, dokill=player.alive) and not ignorecollision:
        # If so, remove the player
        # player.score -= COLLIDE_ENEMY_POINTS
        player.health -= 10
        if player.health <= 0 and player.alive:
            player.health = 0
            boom_sound.play()
            player.kill()
            player.alive = False

        # Stop any moving sounds and play the collision sound
        # move_up_sound.stop()
        # move_down_sound.stop()

        # Stop the loop
        # running = False

    if pygame.sprite.spritecollide(player, ground_group, dokill=False):
        player.ground_counter += 1
        if player.ground_counter >= 10:
            # player.score -= GROUND_PENALTY
            player.ground_counter = 0
            player.health -= 10
            if player.health <= 0 and player.alive:
                player.health = 0
                boom_sound.play()
                player.kill()
                player.alive = False

            ##player 2 collision with enemy##
    if pygame.sprite.spritecollide(player2, enemies, dokill=player2.alive) and not ignorecollision:
        # If so, remove from the player counter
        # player2.score -= COLLIDE_ENEMY_POINTS
        player2.health -= 10
        if player2.health <= 0 and player2.alive:
            player2.health = 0
            boom_sound.play()
            player2.kill()
            player2.alive = False

    # Stop any moving sounds and play the collision sound
    # move_up_sound.stop()
    # move_down_sound.stop()
    # collision_sound.play()

    # Stop the loop
    # running = False
    if pygame.sprite.spritecollide(player2, ground_group, dokill=False):
        player2.ground_counter += 1
        if player2.ground_counter >= 10:
            # player2.score -= GROUND_PENALTY
            player2.health -= 10
            player2.ground_counter = 0
            # print(player2.health)
            if player2.health <= 0 and player2.alive:
                player2.health = 0
                boom_sound.play()
                player2.kill()
                player2.alive = False

    if benefits:
        for bit in pygame.sprite.spritecollide(player, benefits, dokill=player.alive):
            if player.alive:
                collision_sound.play()
                player.score += int(bit.get_coin() / 10)
                largeFont = pygame.font.SysFont('comicsans', 20)  # Font object
                text = largeFont.render(str(int(bit.get_coin() / 10)), 1, (124, 252, 0))  # create our text
                screen.blit(text, (bit.rect.center, (bit.rect.topleft[0] - 50, bit.rect.topleft[1] - 50)))
        for bit in pygame.sprite.spritecollide(player2, benefits, dokill=player2.alive):
            if player2.alive:
                collision_sound.play()
                player2.score += int(bit.get_coin() / 10)
                largeFont = pygame.font.SysFont('comicsans', 20)  # Font object
                text = largeFont.render(str(int(bit.get_coin() / 10)), 1, (124, 252, 0))  # create our text
                screen.blit(text, (bit.rect.center, (bit.rect.topleft[0] - 50, bit.rect.topleft[1] - 50)))
    # largeFont = pygame.font.SysFont('comicsans', 30)  # Font object
    # text = largeFont.render('Player 1 Score: ' + str(player.score), 1, (255, 255, 255))  # create our text
    # screen.blit(text, (0, 0))
    # largeFont = pygame.font.SysFont('comicsans', 30)  # Font object
    # text = largeFont.render('Player 2 Score: ' + str(player2.score), 1, (255, 255, 255))  # create our text
    # screen.blit(text, (0, 500))
    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)
closesocket_thread.join()
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()