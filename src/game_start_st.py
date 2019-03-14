import pygame

from src.res import button_sound
from src import states
from src.common import WIDTH, HEIGHT, clock, no_joystick, joy, switch_state, read_all_controls
from engine.room import MainMenu
from engine.room_item import Button

def game_start_state(window, control):
    flag = True
    flag2 = False
    joy_ctrl = read_all_controls()
    button_font = pygame.font.SysFont("calibri", 55, True)
    title_text = pygame.font.SysFont("calibri", 65, True).render("Choose a difficulty:", True, (240, 240, 240))
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2 - 300, HEIGHT // 2 + 60, (16, 16, 255), button_font, "EASY", colors, True).set_offset_pos()
    button2 = Button(WIDTH // 2 - 110, HEIGHT // 2 + 60, (16, 16, 255), button_font, "NORMAL", colors, True).set_offset_pos().set_selected()
    button3 = Button(WIDTH // 2 + 90, HEIGHT // 2 + 60, (16, 16, 255), button_font, "HARD", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2 + 280, HEIGHT // 2 + 60, (16, 16, 255), button_font, "<None>", colors, True).set_offset_pos()
    button5 = Button(WIDTH // 2, HEIGHT // 2 + 180, (16, 16, 255), button_font, "BACK", colors, True).set_offset_pos()
    buttons = (button1, button2, button3, button4, button5)
    start = MainMenu(title_text, buttons, button_sound, (16, 16, 216))

    while start.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(start, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    start.update_button("up")
                elif event.key == pygame.K_DOWN:
                    start.update_button("down")
                if start.button_pressed() == 0:
                    control["state"] = switch_state(start, states.GAME_2)
                    control["game_mode"] = "normal"
                elif start.button_pressed() == 1:
                    control["state"] = switch_state(start, states.GAME_1)
                    control["game_mode"] = "easy"
                elif start.button_pressed() == 2:
                    control["state"] = switch_state(start, states.GAME_3)
                    control["game_mode"] = "hard"
                elif start.button_pressed() == 3:
                    pass
                elif start.button_pressed() == 4:
                    control["state"] = switch_state(start, states.MENU)

        if not no_joystick:
            if str(joy.get_hat(0)) == joy_ctrl["up"] and flag:
                start.update_button("up")
                flag = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and flag:
                start.update_button("down")
                flag = False
            if joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(joy_ctrl["accept"]) and flag2:
                flag2 = False
                if start.button_pressed(True) == 0:
                    control["state"] = switch_state(start, states.GAME_2)
                    control["game_mode"] = "normal"
                elif start.button_pressed(True) == 1:
                    control["state"] = switch_state(start, states.GAME_1)
                    control["game_mode"] = "easy"
                elif start.button_pressed(True) == 2:
                    control["state"] = switch_state(start, states.GAME_3)
                    control["game_mode"] = "hard"
                elif start.button_pressed(True) == 3:
                    pass
                elif start.button_pressed(True) == 4:
                    control["state"] = switch_state(start, states.MENU)
            elif not joy.get_button(joy_ctrl["accept"]):
                flag2 = True

        start.show(window, 140, 160)
        pygame.display.flip()
        clock.tick(48)
