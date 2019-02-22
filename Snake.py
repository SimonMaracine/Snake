import states
import pygame


GRID = 20  # todo make fullscreen option
WIDTH = 40 * GRID
HEIGHT = 30 * GRID
running = True
no_joystick = True


def show_score(score):
    score_text = score_font.render("SCORE: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (WIDTH / 2 - 64, 40))


def show_fps():
    fps_text = fps_font.render("FPS: " + str(round(clock.get_fps())), False, (255, 255, 255))
    window.blit(fps_text, (6, HEIGHT - 25))


def init_joystick() -> pygame.joystick.Joystick:
    global no_joystick

    if pygame.joystick.get_count() > 0:
        print("Joystick found.")
        no_joystick = False
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        print("Joystick not found.")
        joystick = None
    return joystick


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

fps_font = pygame.font.SysFont("calibri", 16, True)
score_font = pygame.font.SysFont("calibri", 30, True)

joy = init_joystick()

current_state = states.game_state

while running:
    current_state()

pygame.quit()
