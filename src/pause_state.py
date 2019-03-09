from engine.room import Room
from engine.room_item import Button
from src.common import WIDTH, HEIGHT, clock, no_joystick, joy, states, switch_state

import pygame

def pause_state(window) -> int:
    flag = True
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 50, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 110, (16, 16, 255), button_font, "RESUME", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 - 50, (16, 16, 255), button_font, "RESTART", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 10, (16, 16, 255), button_font, "EXIT", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2, HEIGHT // 2 + 70, (16, 16, 255), button_font, "QUIT", colors, True).set_offset_pos()
    buttons = (button1, button2, button3, button4)
    pause = Room(buttons)
    ret = 0

    while pause.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ret = switch_state(pause, states["quit"])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pause.update_button("up")
                elif event.key == pygame.K_DOWN:
                    pause.update_button("down")
                if pause.button_pressed() == 0:
                    pause.exit()
                elif pause.button_pressed() == 1:
                    ret = switch_state(pause, states["game"])
                elif pause.button_pressed() == 2:
                    ret = switch_state(pause, states["menu"])
                elif pause.button_pressed() == 3:
                    ret = switch_state(pause, states["quit"])

        if not no_joystick:
            if joy.get_hat(0) == (0, 1) and flag:
                pause.update_button("up")
                flag = False
            elif joy.get_hat(0) == (0, -1) and flag:
                pause.update_button("down")
                flag = False
            if joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(1):
                if pause.button_pressed(True) == 0:
                    pause.exit()
                elif pause.button_pressed(True) == 1:
                    pause.exit()
                elif pause.button_pressed(True) == 2:
                    ret = switch_state(pause, states["menu"])
                elif pause.button_pressed(True) == 3:
                    ret = switch_state(pause, states["quit"])

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((16, 16, 216))
        pause.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return ret
