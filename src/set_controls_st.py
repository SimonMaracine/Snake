import os
import configparser
import pygame

from src import states
from src.common import WIDTH, HEIGHT, clock, no_joystick, joy, switch_state, read_all_controls
from engine.room import Settings
from engine.room_item import Button

def get_control(window, press_text) -> str:
    window.blit(press_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "None"
            if not no_joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    for i in range(joy.get_numbuttons()):
                        button = joy.get_button(i)
                        if button:
                            return str(i)
                hat = str(joy.get_hat(0))
                if hat in ("(1, 0)", "(0, 1)", "(-1, 0)", "(0, -1)"):
                    return hat
            else:
                print("No joystick detected.")
                return "None"


def set_control(control, button):
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    config["Joy_controls"][control] = button
    with open(os.path.join("data", "settings.ini"), "w") as settings_file:
        config.write(settings_file)


def set_controls_state(window, control):
    flag = True
    flag2 = False
    joy_ctrl = read_all_controls()
    button_font = pygame.font.SysFont("calibri", 55, True)
    title_font = pygame.font.SysFont("calibri", 65, True)
    controls_font = pygame.font.SysFont("calibri", 24, True)
    title_text = title_font.render("Controls", True, (240, 240, 240))
    press_text = pygame.font.SysFont("calibri", 30, True).render("Press any button", True, (240, 240, 240))
    left_text = controls_font.render(joy_ctrl["left"], True, (240, 240, 240))
    right_text = controls_font.render(joy_ctrl["right"], True, (240, 240, 240))
    up_text = controls_font.render(joy_ctrl["up"], True, (240, 240, 240))
    down_text = controls_font.render(joy_ctrl["down"], True, (240, 240, 240))
    accept_text = controls_font.render(str(joy_ctrl["accept"]), True, (240, 240, 240))
    pause_text = controls_font.render(str(joy_ctrl["pause"]), True, (240, 240, 240))
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
                control["state"] = switch_state(controls, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    controls.update_button("up")
                elif event.key == pygame.K_DOWN:
                    controls.update_button("down")
                if controls.button_pressed() == 0:  # left
                    button = get_control(window, press_text)
                    set_control("left", button)
                    left_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed() == 1:  # right
                    button = get_control(window, press_text)
                    set_control("right", button)
                    right_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed() == 2:  # up
                    button = get_control(window, press_text)
                    set_control("up", button)
                    up_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed() == 3:  # down
                    button = get_control(window, press_text)
                    set_control("down", button)
                    down_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed() == 4:  # accept
                    button = get_control(window, press_text)
                    set_control("accept", button)
                    accept_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed() == 5:  # pause
                    button = get_control(window, press_text)
                    set_control("pause", button)
                    pause_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed() == 6:
                    control["state"] = switch_state(controls, states.OPTIONS)

        if not no_joystick:
            if str(joy.get_hat(0)) == joy_ctrl["up"] and flag:
                controls.update_button("up")
                flag = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and flag:
                controls.update_button("down")
                flag = False
            elif joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(joy_ctrl["accept"]) and flag2:
                flag = False
                flag2 = False
                if controls.button_pressed(True) == 0:
                    button = get_control(window, press_text)
                    set_control("left", button)
                    left_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed(True) == 1:
                    button = get_control(window, press_text)
                    set_control("right", button)
                    right_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed(True) == 2:
                    button = get_control(window, press_text)
                    set_control("up", button)
                    up_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed(True) == 3:
                    button = get_control(window, press_text)
                    set_control("down", button)
                    down_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed(True) == 4:
                    button = get_control(window, press_text)
                    set_control("accept", button)
                    accept_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed(True) == 5:
                    button = get_control(window, press_text)
                    set_control("pause", button)
                    pause_text = controls_font.render(button, True, (240, 240, 240))
                elif controls.button_pressed(True) == 6:
                    control["state"] = switch_state(controls, states.OPTIONS)
            elif not joy.get_button(joy_ctrl["accept"]):
                flag2 = True

        controls.show(window, WIDTH // 2 - 110, 100)
        window.blit(left_text, (WIDTH // 2 - 215, HEIGHT // 2 - 40))
        window.blit(right_text, (WIDTH // 2 - 55, HEIGHT // 2 - 40))
        window.blit(up_text, (WIDTH // 2 - 215, HEIGHT // 2 + 60))
        window.blit(down_text, (WIDTH // 2 - 55, HEIGHT // 2 + 60))

        window.blit(accept_text, (WIDTH // 2 + 150, HEIGHT // 2 - 40))
        window.blit(pause_text, (WIDTH // 2 + 150, HEIGHT // 2 + 60))
        pygame.display.flip()
        clock.tick(48)
