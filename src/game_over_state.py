from engine.room import Room
from engine.room_item import Button
from src.common import WIDTH, HEIGHT, clock, no_joystick, joy, states, switch_state
from src.quit_state import quit_state

import pygame

def game_over_state(window):
    flag = True
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 45, True)
    title_text = pygame.font.SysFont("calibri", 60, True).render("Game Over", True, (240, 240, 240))
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 18, (16, 16, 255), button_font, "RESTART", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 + 37, (16, 16, 255), button_font, "EXIT", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 92, (16, 16, 255), button_font, "QUIT", colors, True).set_offset_pos()
    buttons = (button1, button2, button3)
    game_over = Room(buttons)

    while game_over.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ret = switch_state(game_over, states["quit"])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_over.update_button("up")
                elif event.key == pygame.K_DOWN:
                    game_over.update_button("down")
                if game_over.button_pressed() == 0:
                    game_over.exit()
                elif game_over.button_pressed() == 1:
                    ret = switch_state(game_over, states["menu"])
                elif game_over.button_pressed() == 2:
                    ret = switch_state(game_over, states["quit"])

        if not no_joystick:
            if joy.get_hat(0) == (0, 1) and flag:
                game_over.update_button("up")
                flag = False
            elif joy.get_hat(0) == (0, -1) and flag:
                game_over.update_button("down")
                flag = False
            elif joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(1):
                if game_over.button_pressed(True) == 0:
                    ret = switch_state(game_over, states["game"])
                elif game_over.button_pressed(True) == 1:
                    ret = switch_state(game_over, states["menu"])
                elif game_over.button_pressed(True) == 2:
                    ret = switch_state(game_over, states["quit"])

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((16, 16, 216))
        window.blit(title_text, (WIDTH // 2 - 140, HEIGHT // 2 - 110))
        game_over.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return ret
