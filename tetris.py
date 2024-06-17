import pygame
W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
FPS = 60

pygame.init()
window = pygame.display.set_mode((GAME_RES))
clock = pygame.time.Clock()

grid = [pygame.Rect((x * TILE),( y * TILE), TILE, TILE) for x in range(W) for y in range(H)]

while True:
    window.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    [pygame.draw.rect((window),(40,40,40),i_rect,1,) for i_rect in grid]



    pygame.display.update()
    clock.tick()