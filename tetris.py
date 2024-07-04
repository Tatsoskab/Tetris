import pygame
from copy import deepcopy
from random import choice, randrange

# Initialize Pygame
pygame.init()

# Constants
W, H = 10, 20
TILE = 40
GAME_RES = W * TILE, H * TILE
RES = 1090, 815

FPS = 60

# Initialize Pygame display
sc = pygame.display.set_mode(RES)
window = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")

# Grid setup
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# Define figure positions
figures_pos = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],     # I shape
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],  # J shape
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],   # L shape
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],   # O shape
    [(0, 0), (0, -1), (0, 1), (-1, -1)],   # S shape
    [(0, 0), (0, -1), (0, 1), (1, -1)],    # T shape
    [(0, 0), (0, -1), (0, 1), (-1, 0)],    # Z shape
]
#score
score, lines = 0, 0
scores = {0:0,1:100,2:300,3:700, 4: 1500}
# Images
bg = pygame.image.load("images/background.jpg").convert()
bg = pygame.transform.scale(bg, RES)
game_bg = pygame.image.load("images/res.jpg").convert()

# Colors for the figures
colors = ["#26549e", "#2e8abf", "#b82c2c", "#44b521", "#1f1db3", "#d6991e", "#522cc9"]

# Create figure instances with colors
figures = [
    ([pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos], color)
    for fig_pos, color in zip(figures_pos, colors)
]

figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for _ in range(W)] for _ in range(H)]

# Game Title
main_font = pygame.font.Font("font/font.ttf", 150)
font = pygame.font.Font("font/font.ttf", 45)
title_tetris = main_font.render("TETRIS", True, pygame.Color("black"))
title_score = font.render("score:", True, pygame.Color("green"))
title_record = font.render("record:", True, pygame.Color("purple"))
# Game variables
anim_count, anim_speed, anim_limit = 0, 70, 2000
move_speed = 1  # Adjust move_speed for immediate response
move_count, move_limit = 0, 5  # Adjust move_limit for controlling movement frequency

# Initialize figure and next figure
figure, color = deepcopy(choice(figures))
next_figure, next_color = deepcopy(choice(figures))

# Function to check if figure is within borders
def check_borders():
    for rect in figure:
        if rect.x < 0 or rect.x >= W or rect.y >= H or field[rect.y][rect.x]:
            return False
    return True

# Function to draw the next figure
def draw_next_figure(screen, next_figure, next_color):
    next_grid_x, next_grid_y = 340 , 130  # Position for the next shape grid
    for rect in next_figure:
        next_rect = pygame.Rect(
            rect.x * TILE + next_grid_x, 
            rect.y * TILE + next_grid_y, 
            TILE - 2, TILE - 2
        )
        pygame.draw.rect(screen, next_color, next_rect)
def get_record():
    try:
        with open("record") as f:
            return f.readline()
    except FileNotFoundError:
        with open("record", "w") as f:
            f.write("0")

def set_record(record, score):
    rec = max(int(record), score)
    with open("record", "w") as f:
        f.write(str(rec))
# Main game loop
run = True
while run:
    record = get_record()
    sc.blit(bg, (0, 0))
    sc.blit(window, (50, 10))
    window.fill((0,0,0))
    window.blit(game_bg, (0, 0))
    keys = pygame.key.get_pressed()
    dy, dx, rotate = 0, 0, False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                anim_limit = 0
            elif event.key == pygame.K_w:
                rotate = True

    # Continuous movement
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

    # Rotation
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
        pygame.draw.rect(window, ("#292828"), rect, 1)
    for rect in figure:
        figure_rect.x = rect.x * TILE
        figure_rect.y = rect.y * TILE
        pygame.draw.rect(window, color, figure_rect)
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col:
                figure_rect.x = x * TILE
                figure_rect.y = y * TILE
                pygame.draw.rect(window, col, figure_rect)

    # Draw next figure
    #pygame.draw.rect(sc,("#080808"),(470,80, TILE * 5,TILE * 5))
    draw_next_figure(sc, next_figure, next_color)

    # Update animation count
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for rect in figure:
            rect.y += 1
        if not check_borders():
            for rect in figure_old:
                field[rect.y][rect.x] = color
            figure, color = next_figure, next_color
            next_figure, next_color = deepcopy(choice(figures))
            anim_limit = 2000

    # Check Lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    score += scores[lines]


    sc.blit(title_tetris, (600, 0))
    sc.blit(title_score, (535, 750))
    sc.blit(font.render(str(score), True,pygame.Color("white")), (645, 750))
    sc.blit(title_record,(525, 650))
    sc.blit(font.render(str(record), True,pygame.Color("white")), (645, 650))
    for i in range(W):
        if field[0][i]:
            set_record(record,score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 70, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(window,color,i_rect)
                sc.blit(window,(50,10))
                pygame.display.flip()
                clock.tick(1000)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
