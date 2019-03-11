import pygame

from src import states
from src.common import WIDTH, HEIGHT, clock, no_joystick, joy, clear_data, switch_state
from engine.room import Room
from engine.room_item import Button

def ask_clear_state(window, control) -> int:
    flag = True
    dark = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 96))
    window.blit(dark, (0, 0))
    background = pygame.Surface((WIDTH // 2 - 150, HEIGHT // 2 - 150))
    button_font = pygame.font.SysFont("calibri", 41, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 40, (16, 16, 255), button_font, "COMMIT", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 + 10, (16, 16, 255), button_font, "CANCEL", colors, True).set_offset_pos()
    buttons = (button1, button2)
    ask_clear = Room(buttons)
    q = 0

    while ask_clear.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(ask_clear, states.QUIT)
                q = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ask_clear.update_button("up")
                elif event.key == pygame.K_DOWN:
                    ask_clear.update_button("down")
                if ask_clear.button_pressed() == 0:
                    clear_data()
                    ask_clear.exit()
                elif ask_clear.button_pressed() == 1:
                    ask_clear.exit()

        if not no_joystick:
            if joy.get_hat(0) == (0, 1) and flag:
                ask_clear.update_button("up")
                flag = False
            elif joy.get_hat(0) == (0, -1) and flag:
                ask_clear.update_button("down")
                flag = False
            if joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(1):
                if ask_clear.button_pressed(True) == 0:
                    clear_data()
                    ask_clear.exit()
                elif ask_clear.button_pressed(True) == 1:
                    ask_clear.exit()

        window.blit(background, (WIDTH // 4 + 75, HEIGHT // 4 + 75))
        background.fill((16, 16, 216))
        ask_clear.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return q
