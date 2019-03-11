import os
import configparser
import pickle
import pygame

def show_fps(window):
    fps_text = fps_font.render("FPS: " + str(round(clock.get_fps())), False, (255, 255, 255))
    window.blit(fps_text, (6, HEIGHT - 25))


def switch_state(from_state, to_state, window=None, control=None) -> int:
    if type(to_state) == int:
        from_state.exit()
        return to_state
    else:
        if to_state(window, control) == 1:
            from_state.exit()
            return -16


def clear_data():
    with open(os.path.join("data", "data.dat"), "wb") as data_file:
        data_to_write = [0, "n/a"]
        pickle.dump(data_to_write, data_file)


def reset_settings():
    with open(os.path.join("data", "settings.ini"), "w") as settings_file:
        settings_file.write("[DEFAULT]\nfullscreen = False\nvolume = 0.7\nleft = (-1, 0)\nright = (1, 0)\nup = (0, 1)\ndown = (0, -1)\naccept = 1\npause = 9\n\n[Settings]\n\n[Joy_controls]\n\n")


def get_fullscreen() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    return config["Settings"].getboolean("fullscreen")


def set_fullscreen(control):
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    config["Settings"]["fullscreen"] = str(not control["fullscreen"])
    with open(os.path.join("data", "settings.ini"), "w") as settings_file:
        config.write(settings_file)


def toggle_fullscreen(control) -> pygame.Surface:
    if not control["fullscreen"]:
        control["fullscreen"] = True
        return pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        control["fullscreen"] = False
        return pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)


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


GRID = 20
WIDTH = 40 * GRID
HEIGHT = 30 * GRID
no_joystick = True
pygame.joystick.init()
pygame.font.init()
joy = init_joystick()
clock = pygame.time.Clock()
fps_font = pygame.font.SysFont("calibri", 16, True)
