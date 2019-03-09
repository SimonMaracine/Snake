from engine.room import Settings
from engine.room_item import Button
from src.common import WIDTH, HEIGHT, clock, no_joystick, joy, states, switch_state

import pygame
import os
import configparser

def set_controls() -> str:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "None"
            if event.type == pygame.JOYBUTTONDOWN:
                if not no_joystick:
                    for button in joy.get_buttons():
                        if button:
                            print(button)
                            return button
                    for direction in joy.get_hats()[0]:
                        if direction:
                            print(direction)
                            return direction


def get_controls() -> tuple:
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    left = config["Joy_controls"]["left"]
    right = config["Joy_controls"]["right"]
    up = config["Joy_controls"]["up"]
    down = config["Joy_controls"]["down"]
    accept = config["Joy_controls"]["accept"]
    pause = config["Joy_controls"]["pause"]
    return left, right, up, down, accept, pause


def set_controls_state(window):
    flag = True
    flag2 = False
    show_press = False
    button_font = pygame.font.SysFont("calibri", 55, True)
    title_font = pygame.font.SysFont("calibri", 65, True)
    controls_font = pygame.font.SysFont("calibri", 24, True)
    title_text = title_font.render("Controls", True, (240, 240, 240))
    press_text = pygame.font.SysFont("calibri", 30, True).render("Press any button", True, (240, 240, 240))
    joy_ctrl = get_controls()
    left_text = controls_font.render(joy_ctrl[0], True, (240, 240, 240))
    right_text = controls_font.render(joy_ctrl[1], True, (240, 240, 240))
    up_text = controls_font.render(joy_ctrl[2], True, (240, 240, 240))
    down_text = controls_font.render(joy_ctrl[3], True, (240, 240, 240))
    accept_text = controls_font.render(joy_ctrl[4], True, (240, 240, 240))
    pause_text = controls_font.render(joy_ctrl[5], True, (240, 240, 240))
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2 - 190, HEIGHT // 2 - 100, (16, 16, 255), button_font, "left", colors, True).set_offset_pos()
    button2 = Button(WIDTH // 2 - 30, HEIGHT // 2 - 100, (16, 16, 255), button_font, "right", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2 - 190, HEIGHT // 2, (16, 16, 255), button_font, "up", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2 - 30, HEIGHT // 2, (16, 16, 255), button_font, "down", colors, True).set_offset_pos()
    button5 = Button(WIDTH // 2 + 160, HEIGHT // 2 - 100, (16, 16, 255), button_font, "accept", colors, True).set_offset_pos()
    button6 = Button(WIDTH // 2 + 160, HEIGHT // 2, (16, 16, 255), button_font, "pause", colors, True).set_offset_pos()
    button7 = Button(WIDTH // 2, HEIGHT // 2 + 170, (16, 16, 255), button_font, "BACK", colors, True).set_offset_pos().set_selected()
    buttons = (button1, button2, button3, button4, button5, button6, button7)
    controls = Settings(title_text, buttons, None, (16, 16, 216))

    while controls.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ret = switch_state(controls, states["quit"])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    controls.update_button("up")
                elif event.key == pygame.K_DOWN:
                    controls.update_button("down")
                if controls.button_pressed() == 0:  # left
                    show_press = True
                elif controls.button_pressed() == 1:  # right
                    show_press = True
                elif controls.button_pressed() == 2:  # up
                    show_press = True
                elif controls.button_pressed() == 3:  # down
                    show_press = True
                elif controls.button_pressed() == 4:  # accept
                    show_press = True
                elif controls.button_pressed() == 5:  # pause
                    show_press = True
                elif controls.button_pressed() == 6:
                    ret = switch_state(controls, states["options"])

        if not no_joystick:
            if joy.get_hat(0) == (0, 1) and flag:
                controls.update_button("up")
                flag = False
            elif joy.get_hat(0) == (0, -1) and flag:
                controls.update_button("down")
                flag = False
            elif joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(1) and flag2:
                flag2 = False
                if controls.button_pressed(True) == 0:
                    pass
                elif controls.button_pressed(True) == 1:
                    pass
                elif controls.button_pressed(True) == 2:
                    pass
                elif controls.button_pressed(True) == 3:
                    pass
                elif controls.button_pressed(True) == 4:
                    pass
                elif controls.button_pressed(True) == 5:
                    pass
                elif controls.button_pressed(True) == 6:
                    ret = switch_state(controls, states["options"])
            elif not joy.get_button(1):
                flag2 = True

        controls.show(window, WIDTH // 2 - 110, 100)
        if show_press:
            window.blit(press_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))
        window.blit(left_text, (WIDTH // 2 - 215, HEIGHT // 2 - 40))
        window.blit(right_text, (WIDTH // 2 - 55, HEIGHT // 2 - 40))
        window.blit(up_text, (WIDTH // 2 - 215, HEIGHT // 2 + 60))
        window.blit(down_text, (WIDTH // 2 - 55, HEIGHT // 2 + 60))

        window.blit(accept_text, (WIDTH // 2 + 150, HEIGHT // 2 - 40))
        window.blit(pause_text, (WIDTH // 2 + 150, HEIGHT // 2 + 60))
        pygame.display.flip()
        clock.tick(48)

    return ret
