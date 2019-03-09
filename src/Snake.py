from src.common import clear_data, state, window
from src.game_state import game_state
from src.menu_state import menu_state
from src.options_state import options_state
from src.set_controls_state import set_controls_state
from src.game_over_state import game_over_state
from src.quit_state import quit_state

import pygame
import os

def check_data_file():
    try:
        open(os.path.join("data", "data.dat"), "rb")
    except FileNotFoundError:
        clear_data()
        print("Data file not found; created a new one.")


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load("gfx\\snake.png").convert_alpha())

check_data_file()

while True:
    if state == 0:
        state = game_state(window)
    elif state == 1:
        state = menu_state(window)
    elif state == 2:
        state = options_state(window)
    elif state == 3:
        state = set_controls_state(window)
    elif state == 4:
        state = game_over_state(window)
    elif state == -1:
        quit_state()
