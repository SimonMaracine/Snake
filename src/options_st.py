import pygame

from res import button_sound
import states, ask_clear_st
from common import WIDTH, HEIGHT, clock, no_joystick, joy, toggle_fullscreen, set_fullscreen, switch_state, read_all_controls
from engine.room import MainMenu
from engine.room_item import Button


def options_state(window, control):
    flag = True
    flag2 = False
    joy_ctrl = read_all_controls()
    button_font = pygame.font.SysFont("calibri", 55, True)
    title_font = pygame.font.SysFont("calibri", 65, True)
    title_text = title_font.render("Options", True, (240, 240, 240))
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 110, (16, 16, 255), button_font, "CLEAR DATA", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 - 40, (16, 16, 255), button_font, "VOLUME", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 30, (16, 16, 255), button_font, "TOGGLE FULLSCREEN", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2, HEIGHT // 2 + 100, (16, 16, 255), button_font, "SET CONTROLS", colors, True).set_offset_pos()
    button5 = Button(WIDTH // 2, HEIGHT // 2 + 170, (16, 16, 255), button_font, "BACK", colors, True).set_offset_pos()
    buttons = (button1, button2, button3, button4, button5)
    options = MainMenu(title_text, buttons, button_sound, (16, 16, 216))

    while options.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(options, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    options.update_button("up")
                elif event.key == pygame.K_DOWN:
                    options.update_button("down")
                if options.button_pressed() == 0:
                    switch_state(options, ask_clear_st.ask_clear_state, window, control)
                elif options.button_pressed() == 1:
                    pass
                elif options.button_pressed() == 2:
                    window = toggle_fullscreen(control)
                    set_fullscreen(control)
                elif options.button_pressed() == 3:
                    control["state"] = switch_state(options, states.SET_CONTROLS)
                elif options.button_pressed() == 4:
                    control["state"] = switch_state(options, states.MENU)

        if not no_joystick:
            if str(joy.get_hat(0)) == joy_ctrl["up"] and flag:
                options.update_button("up")
                flag = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and flag:
                options.update_button("down")
                flag = False
            elif joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(joy_ctrl["accept"]) and flag2:
                flag2 = False
                if options.button_pressed(True) == 0:
                    switch_state(options, ask_clear_st.ask_clear_state, window, control)
                elif options.button_pressed(True) == 1:
                    pass
                elif options.button_pressed(True) == 2:
                    window = toggle_fullscreen(control)
                    set_fullscreen(control)
                elif options.button_pressed(True) == 3:
                    control["state"] = switch_state(options, states.SET_CONTROLS)
                elif options.button_pressed(True) == 4:
                    control["state"] = switch_state(options, states.MENU)
            elif not joy.get_button(joy_ctrl["accept"]):
                flag2 = True

        options.show(window, WIDTH // 2 - 110, 100)
        pygame.display.flip()
        clock.tick(48)
