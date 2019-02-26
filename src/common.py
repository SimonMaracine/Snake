import pygame
import os
import configparser
import pickle

def show_fps():
    fps_text = fps_font.render("FPS: " + str(round(clock.get_fps())), False, (255, 255, 255))
    window.blit(fps_text, (6, HEIGHT - 25))


def switch_state(from_state, to_state, mode="exit"):
    if mode == "exit":
        pass

    elif mode == "on_top":
        pass


def clear_data():
    with open(os.path.join("data", "data.dat"), "wb") as data_file:
        data_to_write = [0, "n/a"]
        pickle.dump(data_to_write, data_file)


def get_fullscreen() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    return config["Settings"].getboolean("fullscreen")


def set_fullscreen():
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    config["Settings"]["fullscreen"] = str(not fullscreen)
    with open(os.path.join("data", "settings.ini"), "w") as settings_file:
        config.write(settings_file)


def toggle_fullscreen() -> pygame.Surface:
    global fullscreen

    if not fullscreen:
        fullscreen = True
        return pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        fullscreen = False
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


pygame.display.init()
pygame.joystick.init()
pygame.font.init()

game_st = 0
menu_st = 1
options_st = 2
set_controls_st = 3
game_over_st = 4
pause_st = 5
ask_clear_st = 6
quit_st = -1

GRID = 20
WIDTH = 40 * GRID
HEIGHT = 30 * GRID
no_joystick = True
fullscreen = get_fullscreen()
window = toggle_fullscreen()
joy = init_joystick()
clock = pygame.time.Clock()
fps_font = pygame.font.SysFont("calibri", 16, True)
current_state = menu_st
