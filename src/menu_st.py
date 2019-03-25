import os
import pickle
import pygame

from res import button_sound
import states
from common import WIDTH, HEIGHT, clock, no_joystick, joy, switch_state, read_all_controls
from engine.room import MainMenu
from engine.room_item import Button


def load_best_score() -> tuple:
    with open(os.path.join("data", "data.dat"), "rb") as data_file:
        dt = pickle.load(data_file)
        try:
            date_time = "{:04d}/{:02d}/{:02d}-{:02d}:{:02d}".format(dt[1].year, dt[1].month, dt[1].day, dt[1].hour, dt[1].minute)
        except AttributeError:
            date_time = dt[1]
        return int(dt[0]), date_time


def menu_state(window, control):
    flag = True
    flag2 = False
    joy_ctrl = read_all_controls()
    button_font = pygame.font.SysFont("calibri", 55, True)
    best_score = load_best_score()
    best_font = pygame.font.SysFont("calibri", 30, True)
    score_text = best_font.render("Best Score: " + str(best_score[0]), True, (216, 216, 216))
    date_text = pygame.font.SysFont('calibri', 30, True).render(best_score[1], True, (216, 216, 216))
    title_text = pygame.font.SysFont("calibri", 85, True).render("Snakesss...", True, (240, 240, 240))
    joy_text = pygame.font.SysFont("calibri", 27, True).render("You can use a gamepad!", True, (240, 240, 240))
    joy_text = pygame.transform.rotate(joy_text, -26)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 100, (16, 16, 255), button_font, "PLAY", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 - 30, (16, 16, 255), button_font, "OPTIONS", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 40, (16, 16, 255), button_font, "INSTRUCTIONS", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2, HEIGHT // 2 + 110, (16, 16, 255), button_font, "HIGH SCORES", colors, True).set_offset_pos()
    button5 = Button(WIDTH // 2, HEIGHT // 2 + 180, (16, 16, 255), button_font, "QUIT", colors, True).set_offset_pos()
    buttons = (button1, button2, button3, button4, button5)
    menu = MainMenu(title_text, buttons, button_sound, (16, 16, 216))

    while menu.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(menu, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.update_button("up")
                elif event.key == pygame.K_DOWN:
                    menu.update_button("down")
                if menu.button_pressed() == 0:
                    control["state"] = switch_state(menu, states.GAME_START)
                elif menu.button_pressed() == 1:
                    control["state"] = switch_state(menu, states.OPTIONS)
                elif menu.button_pressed() == 2:
                    pass
                elif menu.button_pressed() == 3:
                    pass
                elif menu.button_pressed() == 4:
                    control["state"] = switch_state(menu, states.QUIT)

        if not no_joystick:
            if str(joy.get_hat(0)) == joy_ctrl["up"] and flag:
                menu.update_button("up")
                flag = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and flag:
                menu.update_button("down")
                flag = False
            if joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(joy_ctrl["accept"]) and flag2:
                flag2 = False
                if menu.button_pressed(True) == 0:
                    control["state"] = switch_state(menu, states.GAME_START)
                elif menu.button_pressed(True) == 1:
                    control["state"] = switch_state(menu, states.OPTIONS)
                elif menu.button_pressed(True) == 2:
                    pass
                elif menu.button_pressed(True) == 3:
                    pass
                elif menu.button_pressed(True) == 4:
                    control["state"] = switch_state(menu, states.QUIT)
            elif not joy.get_button(joy_ctrl["accept"]):
                flag2 = True

        menu.show(window, 55, 40)
        window.blit(score_text, (50, HEIGHT // 2 - 155))
        window.blit(date_text, (50, HEIGHT // 2 - 123))
        window.blit(joy_text, (490, 110))
        pygame.display.flip()
        clock.tick(48)
