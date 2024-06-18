import pygame
W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
FPS = 60

pygame.init()
window = pygame.display.set_mode((GAME_RES))
clock = pygame.time.Clock()

grid = [pygame.Rect((x * TILE),( y * TILE), TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1,0),(-2,0),(0,0),(1,0)],
               [(0,-1),(-1,-1),(-1,0),(0,0)],
               [(-1,0),(-1,1),(0,0),(0,-1)],
               [(0,0),(-1,0),(0,1),(-1,-1)],
               [(0,0),(0,-1),(0,1),(-1,-1)],
               [(0,0),(0,-1),(0,1),(1,-1)],
               [(0,0),(0,-1),(0,1),(-1,0)],]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]

figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

figure = figures[0]


while True:
    dx = 0
    window.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                dx -= 1
            elif event.key == pygame.K_d:
                dx += 1


    [pygame.draw.rect((window),(40,40,40),i_rect,1,) for i_rect in grid]

    for i in range(4):
        figure[i].x += dx
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE

        pygame.draw.rect(window,pygame.Color("white"),figure_rect)




    pygame.display.update()
    clock.tick()