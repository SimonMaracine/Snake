import pygame

from src.res import button_sound
from src import states
from src.common import WIDTH, HEIGHT, clock, no_joystick, joy, switch_state, read_all_controls
from engine.room import Room
from engine.room_item import Button

def game_over_state(window, control):
    flag = True
    joy_ctrl = read_all_controls()
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 45, True)
    title_text = pygame.font.SysFont("calibri", 60, True).render("Game Over", True, (240, 240, 240))
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 20, (16, 16, 255), button_font, "RESTART", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 + 35, (16, 16, 255), button_font, "EXIT", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 90, (16, 16, 255), button_font, "QUIT", colors, True).set_offset_pos()
    buttons = (button1, button2, button3)
    game_over = Room(buttons, button_sound)
    if control["game_mode"] == "easy":
        game_mode = states.GAME_2
    elif control["game_mode"] == "hard":
        game_mode = states.GAME_3
    else:
        game_mode = states.GAME_1

    while game_over.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(game_over, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_over.update_button("up")
                elif event.key == pygame.K_DOWN:
                    game_over.update_button("down")
                if game_over.button_pressed() == 0:
                    control["state"] = switch_state(game_over, game_mode)
                elif game_over.button_pressed() == 1:
                    control["state"] = switch_state(game_over, states.MENU)
                elif game_over.button_pressed() == 2:
                    control["state"] = switch_state(game_over, states.QUIT)

        if not no_joystick:
            if str(joy.get_hat(0)) == joy_ctrl["up"] and flag:
                game_over.update_button("up")
                flag = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and flag:
                game_over.update_button("down")
                flag = False
            elif joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(joy_ctrl["accept"]):
                if game_over.button_pressed(True) == 0:
                    control["state"] = switch_state(game_over, game_mode)
                elif game_over.button_pressed(True) == 1:
                    control["state"] = switch_state(game_over, states.MENU)
                elif game_over.button_pressed(True) == 2:
                    control["state"] = switch_state(game_over, states.QUIT)

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((16, 16, 216))
        window.blit(title_text, (WIDTH // 2 - 140, HEIGHT // 2 - 110))
        game_over.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)
