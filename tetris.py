import pygame
from copy import deepcopy
from random import choice

# Initialize Pygame
pygame.init()

# Constants
W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
FPS = 60

# Initialize Pygame display
window = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()

# Grid setup
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# Define figure positions
figures_pos = [
    [[-1, 0], [-2, 0], [0, 0], [1, 0]],     # I shape
    [[0, -1], [-1, -1], [-1, 0], [0, 0]],  # J shape
    [[-1, 0], [-1, 1], [0, 0], [0, -1]],   # L shape
    [[0, 0], [-1, 0], [0, 1], [-1, -1]],   # O shape
    [[0, 0], [0, -1], [0, 1], [-1, -1]],   # S shape
    [[0, 0], [0, -1], [0, 1], [1, -1]],    # T shape
    [[0, 0], [0, -1], [0, 1], [-1, 0]],    # Z shape
]

# Create figure instances
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for _ in range(W)] for _ in range(H)]

# Game variables
anim_count, anim_speed, anim_limit = 0, 40, 2000
move_speed = 1  # Adjust move_speed for immediate response
move_count, move_limit = 0, 3  # Adjust move_limit for controlling movement frequency

# Initialize figure
figure = deepcopy(choice(figures))

# Function to check if figure is within borders
def check_borders():
    for rect in figure:
        if rect.x < 0 or rect.x >= W or rect.y >= H or field[rect.y][rect.x]:
            return False
    return True



# Main game loop
run = True
while run:
    keys = pygame.key.get_pressed()
    dy, dx, rotate = 0, 0, False
    window.fill(pygame.Color("black"))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                anim_limit = 0
            elif event.key == pygame.K_w:
                rotate = True

    # Continuous movement handling
    if keys[pygame.K_a]:
        dx -= move_speed
    elif keys[pygame.K_d]:
        dx += move_speed
    elif keys[pygame.K_s]:
        dy += move_speed

    # Apply movement within move_limit
    move_count += 1
    if move_count > move_limit:
        move_count = 0
        if dx != 0:
            figure_old = deepcopy(figure)
            for rect in figure:
                rect.x += dx
            if not check_borders():
                figure = deepcopy(figure_old)

        if dy != 0:
            figure_old = deepcopy(figure)
            for rect in figure:
                rect.y += dy
            if not check_borders():
                figure = deepcopy(figure_old)


    # Rotation handling
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # Drawing code
    for rect in grid:
        pygame.draw.rect(window, (40, 40, 40), rect, 1)
    for rect in figure:
        figure_rect.x = rect.x * TILE
        figure_rect.y = rect.y * TILE
        pygame.draw.rect(window, pygame.Color("white"), figure_rect)
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col:
                figure_rect.x = x * TILE
                figure_rect.y = y * TILE
                pygame.draw.rect(window, col, figure_rect)
        # Function to rotate figure
    def rotate_figure():
        center = figure[0]
        figure_old = deepcopy(figure)
        for rect in figure:
            x = rect.y - center.y
            y = rect.x - center.x
            rect.x = center.x + x
            rect.y = center.y - y
            if not check_borders():
                figure = deepcopy(figure_old)
                return
    # Update animation count
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for rect in figure:
            rect.y += 1
        if not check_borders():
            for rect in figure_old:
                field[rect.y][rect.x] = pygame.Color("white")
            figure = deepcopy(choice(figures))
            anim_limit = 2000
    #check Lines
    line = H - 1
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
