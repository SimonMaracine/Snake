import pygame

WIDTH = 800
HEIGHT = 600
running = True


class Player(object):
    def __init__(self, width, height):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.width = width
        self.height = height


def show_fps():
    fps_text = fps_font.render("FPS: " + str(round(clock.get_fps())), False, (255, 255, 255))
    window.blit(fps_text, (6, HEIGHT - 25))


def main():
    global running
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False

        window.fill((0, 0, 0))
        show_fps()
        pygame.display.flip()
        clock.tick(60)


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

fps_font = pygame.font.SysFont("calibri", 16, True)

while running:
    main()

pygame.quit()
