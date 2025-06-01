# Assignment 8 Pygame Animation with Class/Object
# My Game: Luffy Spawner

# img source: https://www.pngmart.com/image/21292
# audio source: https://pixabay.com/sound-effects/bloop-2-186531/

import random
import pygame
import time

# constants
last_click_time = 0
DOUBLE_CLICK_DELAY = 400
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (255,255,255)
IMAGE_SIZE = 200

TINT_COLORS = [
    (100, 0, 0, 80),     # Dark Red
    (0, 100, 0, 80),     # Dark Green
    (0, 0, 100, 80),     # Dark Blue
    (100, 100, 0, 80),   # Olive
    (100, 0, 100, 80),   # Dark Magenta
    (0, 100, 100, 80)    # Teal
]

class Luffy:
    def __init__(self):
        self.original_img = pygame.transform.scale(pygame.image.load('Luffy.png'), (IMAGE_SIZE, IMAGE_SIZE))
        self.img = self.original_img.copy()

        # random initial position
        self.pos_x = random.randint(0, SCREEN_WIDTH - IMAGE_SIZE)
        self.pos_y = random.randint(0, SCREEN_HEIGHT - IMAGE_SIZE)

        # random movement speed
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-3, 3)

        # random tint from list above
        self.tint_color = random.choice(random.sample(TINT_COLORS, 2))
        self.img.fill(self.tint_color, special_flags=pygame.BLEND_ADD)

        # for spin effect
        self.angle = 0
        self.spinning = False
        self.rotation_progress = 0

        # for drag effect
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def animate(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        # i want the img to bounce off edges by reversing the speed
        if self.pos_x < 0 or self.pos_x > SCREEN_WIDTH - IMAGE_SIZE:
            self.speed_x *= -1
        if self.pos_y < 0 or self.pos_y > SCREEN_HEIGHT - IMAGE_SIZE:
            self.speed_y *= -1

        # for rotation animation (I used ChatGPT to aid me in constructing these lines of code)
        if self.spinning:
            self.angle = (self.angle + 10) % 360
            self.rotation_progress += 10
            rotated = pygame.transform.rotate(self.original_img, self.angle)
            self.img = rotated.copy()

            if self.rotation_progress >= 360:
                self.spinning = False
                self.angle = 0
                self.img = self.original_img.copy()

    def start_rotation(self):
        if not self.spinning:
            self.spinning = True
            self.rotation_progress = 0

    # returns True if the user clicks on the rectangle on/around Luffy
    def is_clicked(self, mouse_pos):
            rect = self.img.get_rect(center=(self.pos_x + IMAGE_SIZE // 2, self.pos_y + IMAGE_SIZE // 2))
            return rect.collidepoint(mouse_pos)

    def draw(self):
        # draws the Luffy image on the screen (making sure it stays centered even if it's rotated)
        rect = self.img.get_rect(center=(self.pos_x + IMAGE_SIZE//2, self.pos_y + IMAGE_SIZE//2))
        screen.blit(self.img, rect.topleft)

instructions = """
Welcome to the Luffy Spawner!
fyi: Luffy is the main protagonist in the anime series "One Piece"

--- You choose how many times Luffy appears on the screen!
--- Luffy will appear in random colors!
--- Click and drag to move a Luffy around the screen.
--- Double-click to make Luffy spin and make him turn back into his orginal color!
--- Enjoy a fun sound effect each time you trigger a spin.

Have fun!
"""

print(instructions)

while True:
    try:
        num_luffys = int(input("How many Luffys do you want? (1–10): "))
        if 1 <= num_luffys <= 10:
            break
        else:
            print("Please enter a number between 1 and 10.")
    except ValueError:
        print("That's not a valid number. Please enter an integer.")

pygame.init()
click_sound = pygame.mixer.Sound('bloop.mp3')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Multiple Luffys!')
clock = pygame.time.Clock()

luffys = [Luffy() for _ in range(num_luffys)]

flag = True
while flag:
    clock.tick(60)

    screen.fill(BACKGROUND_COLOR)


    for luffy in luffys:
        luffy.animate()
        luffy.draw()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False


        # rotates on double-click (simulated by last_click_time <= DOUBLE_CLICK_DELAY)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            if current_time - last_click_time <= DOUBLE_CLICK_DELAY:
                for luffy in luffys:
                    if luffy.is_clicked(event.pos):
                        luffy.start_rotation()
                        click_sound.play()
            else:
                for luffy in luffys:
                    # hold single click for dragging effect
                    if luffy.is_clicked(event.pos):
                        luffy.dragging = True
                        # calculates the current offset of the image
                        mouse_x, mouse_y = event.pos
                        luffy.drag_offset_x = mouse_x - luffy.pos_x
                        luffy.drag_offset_y = mouse_y - luffy.pos_y

            last_click_time = current_time

        elif event.type == pygame.MOUSEBUTTONUP:
            for luffy in luffys:
                luffy.dragging = False

        # changes the position by dragging
        elif event.type == pygame.MOUSEMOTION:
            for luffy in luffys:
                if luffy.dragging:
                    mouse_x, mouse_y = event.pos
                    luffy.pos_x = mouse_x - luffy.drag_offset_x
                    luffy.pos_y = mouse_y - luffy.drag_offset_y
pygame.quit()
exit(0)