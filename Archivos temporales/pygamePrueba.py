import pygame
import pygame.freetype as ft  # Import the freetype module.


pygame.init()
screen = pygame.display.set_mode((800, 600))
GAME_FONT = ft.SysFont("Sans", 36)
clock = pygame.time.Clock()
running =  True
counter = 0

currTime = 0
timePressed = 0
enable = False


oldColor = (120,255,120)
newColor = (0, 180, 75)
color = oldColor

speed = 100 / 5 #pix/s
xpos = 200 #pix

prevTime = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            enable = True
            timePressed = pygame.time.get_ticks()

    prevTime = currTime
    currTime = pygame.time.get_ticks()
    print((currTime - prevTime) / 1000)

    if enable and currTime - timePressed > 10000:
        color = newColor



    screen.fill(color)
    # You can use `render` and then blit the text surface ...
    text_surface, rect = GAME_FONT.render("Hello World!", (0, 0, 0))

    screen.blit(text_surface, (xpos, 300))
    xpos += speed / 60
    # # or just `render_to` the target surface.
    # GAME_FONT.render_to(screen, (40, 350), "Hello World!", (0, 0, 0))
    counter += 1

    pygame.draw.line(screen, (0,0,0), (200, 250), (300, 250), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()