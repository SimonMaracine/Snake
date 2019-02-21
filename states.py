from engine.room import Room
from engine.room_item import Button
from objects import import_obj
import pygame
from vectors import Vector
from random import randint


def show_score():
    from Snake import WIDTH, window, score_font

    score_text = score_font.render("SCORE: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (WIDTH / 2 - 64, 40))


def pause_state() -> int:
    from Snake import WIDTH, HEIGHT, window, clock, joy, no_joystick
    import Snake

    once = True
    quit = 0
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 40, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2 - 60, HEIGHT // 2 - 100, (16, 16, 220), button_font, "RESUME", colors, True)
    button2 = Button(WIDTH // 2 - 70, HEIGHT // 2 - 50, (16, 16, 220), button_font, "RESTART", colors, True)
    button3 = Button(WIDTH // 2 - 45, HEIGHT // 2, (16, 16, 220), button_font, "EXIT", colors, True)
    button1.set_selected()
    buttons = (button1, button2, button3)
    pause = Room(buttons)

    while pause.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause.exit()
                Snake.running = False
                quit = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pause.update_button("up")
                elif event.key == pygame.K_DOWN:
                    pause.update_button("down")
                if pause.button_pressed() == 0:
                    pause.exit()
                elif pause.button_pressed() == 1:
                    pause.exit()
                    quit = 1
                elif pause.button_pressed() == 2:
                    pause.exit()
                    Snake.running = False
                    quit = 1

        if not no_joystick:
            if joy.get_button(1):
                if pause.button_pressed(True) == 0:
                    pause.exit()
                elif pause.button_pressed(True) == 1:
                    pause.exit()
                    quit = 1
                elif pause.button_pressed(True) == 2:
                    pause.exit()
                    Snake.running = False
                    quit = 1
            if joy.get_hat(0) == (0, 1) and once:
                pause.update_button("up")
                once = False
            elif joy.get_hat(0) == (0, -1) and once:
                pause.update_button("down")
                once = False
            if joy.get_hat(0) == (0, 0):
                once = True

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((0, 0, 255))
        pause.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return quit


def game_over_state() -> int:
    from Snake import WIDTH, HEIGHT, window, clock, joy, no_joystick
    import Snake

    quit = 0
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 40, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2 - 70, HEIGHT // 2 - 80, (16, 16, 220), button_font, "RESTART", colors, True)
    button2 = Button(WIDTH // 2 - 45, HEIGHT // 2 - 30, (16, 16, 220), button_font, "EXIT", colors, True)
    button1.set_selected()
    buttons = (button1, button2)
    game_over = Room(buttons)

    while game_over.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over.exit()
                Snake.running = False
                quit = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_over.update_button("up")
                elif event.key == pygame.K_DOWN:
                    game_over.update_button("down")
                if game_over.button_pressed() == 0:
                    game_over.exit()
                elif game_over.button_pressed() == 1:
                    game_over.exit()
                    Snake.running = False
                    quit = 1

        if not no_joystick:
            if joy.get_button(1):
                if game_over.button_pressed(True) == 0:
                    game_over.exit()
                elif game_over.button_pressed(True) == 1:
                    game_over.exit()
                    Snake.running = False
                    quit = 1
            if joy.get_hat(0) == (0, 1):
                game_over.update_button("up")
            elif joy.get_hat(0) == (0, -1):
                game_over.update_button("down")

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((0, 0, 255))
        game_over.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return quit


def game_state():
    from Snake import GRID, window, clock, joy, no_joystick, show_fps
    import Snake

    global score

    once = False
    score = 0
    snake = import_obj()[0]()
    food = import_obj()[1](randint(0, 41) * GRID, randint(0, 31) * GRID)
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 48)

    game = Room()

    while game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
                Snake.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not snake.dirs["left"]:
                    snake.dir = Vector(snake.vel, 0, 0)
                    snake.change_direction("right")
                elif event.key == pygame.K_LEFT and not snake.dirs["right"]:
                    snake.dir = Vector(-snake.vel, 0, 0)
                    snake.change_direction("left")
                elif event.key == pygame.K_DOWN and not snake.dirs["up"]:
                    snake.dir = Vector(0, snake.vel, 0)
                    snake.change_direction("down")
                elif event.key == pygame.K_UP and not snake.dirs["down"]:
                    snake.dir = Vector(0, -snake.vel, 0)
                    snake.change_direction("up")
                elif event.key == pygame.K_ESCAPE:
                    if pause_state() == 1:
                        game.exit()
                elif event.key == pygame.K_r:
                    game.exit()
                elif event.key == pygame.K_b:
                    snake.grow()
            elif event.type == MOVE:
                snake.move()
                if snake.collide():
                    game.exit()
                    if game_over_state() == 1:
                        Snake.running = False

        if not no_joystick:
            if joy.get_button(9):
                if pause_state() == 1:
                    game.exit()
            elif joy.get_button(8) and once:
                game.exit()
                once = False
            elif joy.get_button(3):
                snake.grow()
            if not joy.get_button(8):
                once = True
            if joy.get_hat(0) == (-1, 0) and not snake.dirs["right"]:
                snake.dir = Vector(-snake.vel, 0, 0)
                snake.change_direction("left")
            elif joy.get_hat(0) == (1, 0) and not snake.dirs["left"]:
                snake.dir = Vector(snake.vel, 0, 0)
                snake.change_direction("right")
            elif joy.get_hat(0) == (0, 1) and not snake.dirs["down"]:
                snake.dir = Vector(0, -snake.vel, 0)
                snake.change_direction("up")
            elif joy.get_hat(0) == (0, -1) and not snake.dirs["up"]:
                snake.dir = Vector(0, snake.vel, 0)
                snake.change_direction("down")

        window.fill((16, 16, 16))
        if snake.eat(food):
            snake.grow()
            score += 1
            food = import_obj()[1](randint(0, 41) * GRID, randint(0, 31) * GRID)
        snake.show()
        food.show()
        show_score()
        show_fps()
        pygame.display.flip()
        clock.tick(48)
