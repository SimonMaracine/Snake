from engine.room import Room
from engine.room_item import Button
import pygame
from random import randint
from vectors import Vector


def pause_state() -> int:
    import Snake

    once = True
    quit = 0
    background = pygame.Surface((Snake.WIDTH // 2, Snake.HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 40, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(Snake.WIDTH // 2 - 60, Snake.HEIGHT // 2 - 100, (16, 16, 220), button_font, "RESUME", colors, True)
    button2 = Button(Snake.WIDTH // 2 - 70, Snake.HEIGHT // 2 - 50, (16, 16, 220), button_font, "RESTART", colors, True)
    button3 = Button(Snake.WIDTH // 2 - 45, Snake.HEIGHT // 2, (16, 16, 220), button_font, "EXIT", colors, True)
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

        if not Snake.no_joystick:
            if Snake.joy.get_button(1):
                if pause.button_pressed(True) == 0:
                    pause.exit()
                elif pause.button_pressed(True) == 1:
                    pause.exit()
                    quit = 1
                elif pause.button_pressed(True) == 2:
                    pause.exit()
                    Snake.running = False
                    quit = 1
            if Snake.joy.get_hat(0) == (0, 1) and once:
                pause.update_button("up")
                once = False
            elif Snake.joy.get_hat(0) == (0, -1) and once:
                pause.update_button("down")
                once = False
            if Snake.joy.get_hat(0) == (0, 0):
                once = True

        Snake.window.blit(background, (Snake.WIDTH // 4, Snake.HEIGHT // 4))
        background.fill((0, 0, 255))
        pause.show(Snake.window, 0, 0)
        pygame.display.flip()
        Snake.clock.tick(48)

    return quit


def game_over_state() -> int:
    import Snake

    quit = 0
    background = pygame.Surface((Snake.WIDTH // 2, Snake.HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 40, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(Snake.WIDTH // 2 - 70, Snake.HEIGHT // 2 - 80, (16, 16, 220), button_font, "RESTART", colors, True)
    button2 = Button(Snake.WIDTH // 2 - 45, Snake.HEIGHT // 2 - 30, (16, 16, 220), button_font, "EXIT", colors, True)
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

        if not Snake.no_joystick:
            if Snake.joy.get_button(1):
                if game_over.button_pressed(True) == 0:
                    game_over.exit()
                elif game_over.button_pressed(True) == 1:
                    game_over.exit()
                    Snake.running = False
                    quit = 1
            if Snake.joy.get_hat(0) == (0, 1):
                game_over.update_button("up")
            elif Snake.joy.get_hat(0) == (0, -1):
                game_over.update_button("down")

        Snake.window.blit(background, (Snake.WIDTH // 4, Snake.HEIGHT // 4))
        background.fill((0, 0, 255))
        game_over.show(Snake.window, 0, 0)
        pygame.display.flip()
        Snake.clock.tick(48)

    return quit


def game_state():
    import Snake
    import objects
    global score

    once = False
    score = 0
    snake = objects.Snakes()
    food = objects.Food(randint(0, 39) * Snake.GRID, randint(0, 29) * Snake.GRID)
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

        if not Snake.no_joystick:
            if Snake.joy.get_button(9):
                if pause_state() == 1:
                    game.exit()
            elif Snake.joy.get_button(8) and once:
                game.exit()
                once = False
            elif Snake.joy.get_button(3):
                snake.grow()
            if not Snake.joy.get_button(8):
                once = True
            if Snake.joy.get_hat(0) == (-1, 0) and not snake.dirs["right"]:
                snake.dir = Vector(-snake.vel, 0, 0)
                snake.change_direction("left")
            elif Snake.joy.get_hat(0) == (1, 0) and not snake.dirs["left"]:
                snake.dir = Vector(snake.vel, 0, 0)
                snake.change_direction("right")
            elif Snake.joy.get_hat(0) == (0, 1) and not snake.dirs["down"]:
                snake.dir = Vector(0, -snake.vel, 0)
                snake.change_direction("up")
            elif Snake.joy.get_hat(0) == (0, -1) and not snake.dirs["up"]:
                snake.dir = Vector(0, snake.vel, 0)
                snake.change_direction("down")

        Snake.window.fill((16, 16, 16))
        if snake.eat(food):
            snake.grow()
            score += 1
            food = objects.Food(randint(0, 39) * Snake.GRID, randint(0, 29) * Snake.GRID)
        snake.show()
        food.show()
        Snake.show_score(score)
        Snake.show_fps()
        pygame.display.flip()
        Snake.clock.tick(48)
