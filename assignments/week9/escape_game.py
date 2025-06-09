import pygame
import sys
import random

# Game Constants
TILE_SIZE = 32
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
FPS = 60
MIN_ENEMY_DISTANCE = 2  # Minimum distance from player spawn

# Here is my map layout
level_map = [
    "##################",
    "#P..............X#",
    "#...........#....#",
    "#....###..###....#",
    "#................#",
    "#....##....##....#",
    "#.....#..........#",
    "#...E.......E....#",
    "#........##......#",
    "##################"
]

# Base class
class GameObject:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_position(self):
        return self._x, self._y

    def set_position(self, x, y):
        self._x = x
        self._y = y

# Player class with movement (drawn in green)
class Player(GameObject):
    def move(self, dx, dy, walls):
        new_x = self._x + dx
        new_y = self._y + dy
        if (new_x, new_y) not in walls:
            self.set_position(new_x, new_y)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self._x * TILE_SIZE, self._y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Wall class
class Wall(GameObject):
    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, (self._x * TILE_SIZE, self._y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Enemy logic (drawn in red)
class Enemy(GameObject):
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self._x * TILE_SIZE, self._y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def move_toward_player(self, target_pos, walls, other_enemies):
        target_x, target_y = target_pos
        dx = 1 if self._x < target_x else -1 if self._x > target_x else 0
        dy = 1 if self._y < target_y else -1 if self._y > target_y else 0

        # I decided to prioritise horizontal movement of the enemies
        if dx and (self._x + dx, self._y) not in walls and (self._x + dx, self._y) not in other_enemies:
            self.set_position(self._x + dx, self._y)
        elif dy and (self._x, self._y + dy) not in walls and (self._x, self._y + dy) not in other_enemies:
            self.set_position(self._x, self._y + dy)

# Decoy object (drawn as yellow square)
class Decoy(GameObject):
    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, (self._x * TILE_SIZE, self._y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Loops through the level map so the game knows where to put the player, walls, enemies, and exits
def load_level(level_map):
    walls, exits, empty_spaces = set(), set(), set()
    player_start, enemy_positions = None, set()
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            pos = (x, y)
            if tile == '#': walls.add(pos)
            elif tile == 'P': player_start = pos; empty_spaces.add(pos)
            elif tile == 'E': enemy_positions.add(pos); empty_spaces.add(pos)
            elif tile == 'X': exits.add(pos); empty_spaces.add(pos)
            else: empty_spaces.add(pos)
    return walls, exits, empty_spaces, player_start, enemy_positions

# I stumbled upon the concept of "Manhattan distance" in grid-based games so I had ChatGPT help me with writing a function for the initial distance of enemies/player
def initial_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# random spawnpoint in "empty" places
def get_random_spawn(empty_spaces, exclude=set()):
    return random.choice(list(empty_spaces - exclude))

pygame.init()
screen = pygame.display.set_mode((TILE_SIZE * len(level_map[0]), TILE_SIZE * len(level_map)))
pygame.display.set_caption("Escape Game (Time Freeze Edition)")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 35)

# function for instruction screen
def show_instructions():
    showing = True
    while showing:
        screen.fill(BLACK)
        texts = [
            "ESCAPE - TIME FREEZE",
            "Enemies chase you each turn",
            "Move player with arrow keys",
            "Click to place up to 2 decoys",
            "Enemies follow decoys for 1 turn",
            "Reach the orange exit to win",
            "Avoid enemies!",
            "Press SPACE to start",
        ]

        # ChatGPT helped me with centering the text and making it align vertically
        line_height = font_small.get_height() + 5

        for i, line in enumerate(texts):
            rendered = font_small.render(line, True, WHITE)
            rect = rendered.get_rect(center=(screen.get_width() // 2, 60 + i * line_height))
            screen.blit(rendered, rect)
        pygame.display.flip()

    # Spacebar to exit instruction screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                showing = False

show_instructions()

# Game Setup
walls, exit_positions, empty_spaces, player_spawn, enemy_positions = load_level(level_map)

# Spawn enemies randomly (again I had ChatGPT help me combine with the Manhattan distance function above)
enemy_spawns = set()
while len(enemy_spawns) < len(enemy_positions):
    c = get_random_spawn(empty_spaces, enemy_spawns | {player_spawn})
    if c and initial_dist(c, player_spawn) >= MIN_ENEMY_DISTANCE:
        enemy_spawns.add(c)

player = Player(*player_spawn)
enemies = [Enemy(x, y) for x, y in enemy_spawns]
walls_objs = [Wall(x, y) for x, y in walls]
decoys = []
decoy_used_by = {}


running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    moved = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            old = player.get_position()
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                dx, dy = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}[event.key]
                player.move(dx, dy, walls)
                moved = old != player.get_position()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // TILE_SIZE, my // TILE_SIZE
            if len(decoys) < 2 and (gx, gy) in empty_spaces and (gx, gy) != player.get_position():
                if all(decoy.get_position() != (gx, gy) for decoy in decoys):
                    decoys.append(Decoy(gx, gy))

    # Enemy Movement Logic
    if moved:
        enemy_positions_set = {e.get_position() for e in enemies}
        for i, enemy in enumerate(enemies):
            others = enemy_positions_set - {enemy.get_position()}
            used = False
            for j, decoy in enumerate(decoys):
                if (i, j) not in decoy_used_by:
                    target = decoy.get_position()
                    decoy_used_by[(i, j)] = True
                    used = True
                    break
            if not used:
                target = player.get_position()
            enemy.move_toward_player(target, walls, others)

    if player.get_position() in exit_positions:
        screen.blit(font_big.render("You Win!", True, WHITE), font_big.render("You Win!", True, WHITE).get_rect(center=screen.get_rect().center))
        pygame.display.flip(); pygame.time.wait(3000);
        break

    for enemy in enemies:
        if enemy.get_position() == player.get_position():
            screen.blit(font_big.render("Game Over!", True, RED), font_big.render("Game Over!", True, RED).get_rect(center=screen.get_rect().center))
            pygame.display.flip(); pygame.time.wait(3000);
            break

    for wall in walls_objs: wall.draw(screen)
    for ex, ey in exit_positions:
        pygame.draw.rect(screen, ORANGE, (ex * TILE_SIZE, ey * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for decoy in decoys: decoy.draw(screen)
    for enemy in enemies: enemy.draw(screen)
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()

"""
=== Game Instructions ===
Escape (Time Freeze Edition)

Objective:
- You need to reach the orange exit tile while avoiding red enemies

Controls:
- Arrow Keys: Move your player left/right/up/down (green square)
- Mouse Left Click: Place up to 2 decoys (yellow squares) to distract enemies

Rules:
- Enemies chase decoys for one turn if placed; otherwise they chase the player
- You lose if an enemy catches you
- You win if you reach an orange exit
- Walls (gray) block movement
- The game starts when you press SPACE at the instruction screen
"""
