import os
import pygame

from src import states, game_st, menu_st, options_st, set_controls_st, game_over_st, quit_st
from src.common import clear_data, reset_settings, get_fullscreen, toggle_fullscreen

def check_files():
    try:
        open(os.path.join("data", "data.dat"), "rb")
    except FileNotFoundError:
        clear_data()
        print("Data file not found; created a new one.")

    try:
        open(os.path.join("data", "settings.ini"), "r")
    except FileNotFoundError:
        reset_settings()
        print("Settings file not found; created a new one.")


if __name__ == "__main__":
    check_files()
    fullscreen = get_fullscreen()
    control = {"running": True, "state": states.MENU, "fullscreen": fullscreen}  # dict object; passed by reference
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.init()
    window = toggle_fullscreen(control)
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(pygame.image.load("gfx\\snake.png").convert_alpha())

    while True:
        state = control["state"]
        if state == 0:
            game_st.game_state(window, control)
        elif state == 1:
            menu_st.menu_state(window, control)
        elif state == 2:
            options_st.options_state(window, control)
        elif state == 3:
            set_controls_st.set_controls_state(window, control)
        elif state == 4:
            game_over_st.game_over_state(window, control)
        elif state == -1:
            quit_st.quit_state()
