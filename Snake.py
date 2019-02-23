from engine.room import Room, MainMenu
from engine.room_item import Button
import pygame
import os
import datetime
import pickle
import configparser
from random import randint
from vectors import Vector
from copy import deepcopy

GRID = 20
WIDTH = 40 * GRID
HEIGHT = 30 * GRID
running = True

class Snake(object):
    def __init__(self, x=WIDTH/2, y=HEIGHT/2):
        self.x = x
        self.y = y
        self.width = GRID - 2
        self.vel = GRID
        self.dir = Vector(self.vel, 0, 0)
        self.body = [Vector(self.x, self.y, 0),
                     Vector(self.x + GRID, self.y, 0),
                     Vector(self.x + GRID * 2, self.y, 0)]
        self.dirs = {"left": False, "right": True, "up": False, "down": False}

    def show(self):
        for i in range(len(self.body) - 1):
            pygame.draw.rect(window, (255, 255, 255), (self.body[i].x + 1, self.body[i].y + 1, self.width, self.width))
        pygame.draw.rect(window, (160, 160, 255), (self.body[-1].x + 1, self.body[-1].y + 1, self.width, self.width))

    def move(self):
        temp_body = deepcopy(self.body)
        head = temp_body[-1]
        for i in range(len(self.body) - 1):
            self.body[i] = self.body[i + 1]
        self.body.pop()
        head.x += self.dir.vector[0]
        head.y += self.dir.vector[1]
        self.body.append(head)

        if head.x > WIDTH:
            head.x = 0
        elif head.x < 0:
            head.x = WIDTH
        elif head.y > HEIGHT:
            head.y = 0
        elif head.y < 0:
            head.y = HEIGHT

    def eat(self, food) -> bool:
        x = self.body[-1].x
        y = self.body[-1].y
        if food.x + food.width > x + self.width / 2 > food.x:
            if food.y + food.width > y + self.width / 2 > food.y:
                return True
        else:
            return False

    def grow(self):
        head = self.body[-1]
        self.body.append(head)

    def collide(self) -> bool:
        x = self.body[-1].x
        y = self.body[-1].y
        for part in self.body[0:len(self.body) - 2]:
            if part.x + self.width > x + self.width / 2 > part.x:
                if part.y + self.width > y + self.width / 2 > part.y:
                    return True
        return False

    def change_direction(self, direct):
        for direction in self.dirs:
            if direction == direct:
                self.dirs[direction] = True
            else:
                self.dirs[direction] = False


class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = GRID - 5
        self.color = (240, 100, 100)

    def show(self):
        pygame.draw.rect(window, self.color, (self.x + 3, self.y + 3, self.width, self.width))


def show_fps():
    fps_text = fps_font.render("FPS: " + str(round(clock.get_fps())), False, (255, 255, 255))
    window.blit(fps_text, (6, HEIGHT - 25))


def save_best_score(score):
    with open(os.path.join("data", "data.dat"), "rb") as data_file:
        prev_best_score = int(pickle.load(data_file)[0])
        if score > prev_best_score:
            data_to_write = [score, datetime.datetime.now()]
            with open(os.path.join("data", "data.dat"), "wb") as data_file2:
                pickle.dump(data_to_write, data_file2)


def load_best_score() -> tuple:
    with open(os.path.join("data", "data.dat"), "rb") as data_file:
        dt = pickle.load(data_file)
        try:
            date_time = "{:04d}/{:02d}/{:02d}-{:02d}:{:02d}".format(dt[1].year, dt[1].month, dt[1].day, dt[1].hour, dt[1].minute)
        except AttributeError:
            date_time = dt[1]
        return int(dt[0]), date_time


def clear_data():
    with open(os.path.join("data", "data.dat"), "wb") as data_file:
        data_to_write = [0, "n/a"]
        pickle.dump(data_to_write, data_file)


def check_data_file():
    try:
        open(os.path.join("data", "data.dat"), "rb")
    except FileNotFoundError:
        clear_data()
        print("Data file not found; created a new one.")


def init_joystick() -> pygame.joystick.Joystick:
    global no_joystick

    if pygame.joystick.get_count() > 0:
        print("Joystick found.")
        no_joystick = False
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        print("Joystick not found.")
        no_joystick = True
        joystick = None
    return joystick


def get_fullscreen() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    return config["settings"].getboolean("fullscreen")


def set_fullscreen():
    config = configparser.ConfigParser()
    config.read(os.path.join("data", "settings.ini"))
    config["settings"]["fullscreen"] = str(not fullscreen)
    with open(os.path.join("data", "settings.ini"), "w") as settings_file:
        config.write(settings_file)


def toggle_fullscreen() -> pygame.Surface:
    global fullscreen

    if not fullscreen:
        fullscreen = True
        return pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        fullscreen = False
        return pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)


def pause_state() -> int:
    global running, current_state

    flag = True
    quit = 0
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 50, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 110, (16, 16, 255), button_font, "RESUME", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 - 50, (16, 16, 255), button_font, "RESTART", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 10, (16, 16, 255), button_font, "EXIT", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2, HEIGHT // 2 + 70, (16, 16, 255), button_font, "QUIT", colors, True).set_offset_pos()
    buttons = (button1, button2, button3, button4)
    pause = Room(buttons)

    while pause.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause.exit()
                running = False
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
                    quit = 1
                    current_state = menu_state
                elif pause.button_pressed() == 3:
                    pause.exit()
                    running = False
                    quit = 1

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
                    quit = 1
                elif pause.button_pressed(True) == 2:
                    pause.exit()
                    quit = 1
                    current_state = menu_state
                elif pause.button_pressed(True) == 3:
                    pause.exit()
                    running = False
                    quit = 1

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((16, 16, 216))
        pause.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return quit


def game_over_state() -> int:
    global running, current_state

    flag = True
    quit = 0
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
                game_over.exit()
                running = False
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
                    current_state = menu_state
                elif game_over.button_pressed() == 2:
                    game_over.exit()
                    running = False
                    quit = 1

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
                    game_over.exit()
                elif game_over.button_pressed(True) == 1:
                    game_over.exit()
                    current_state = menu_state
                elif game_over.button_pressed(True) == 2:
                    game_over.exit()
                    running = False
                    quit = 1

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((16, 16, 216))
        window.blit(title_text, (WIDTH // 2 - 140, HEIGHT // 2 - 110))
        game_over.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return quit


def options_state():
    global running, current_state, window

    flag = True
    flag2 = False
    button_font = pygame.font.SysFont("calibri", 55, True)
    title_font = pygame.font.SysFont("calibri", 65, True)
    title_text = title_font.render("Options", True, (240, 240, 240))
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 40, (16, 16, 255), button_font, "CLEAR DATA", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 + 30, (16, 16, 255), button_font, "VOLUME", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 100, (16, 16, 255), button_font, "TOGGLE FULLSCREEN", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2, HEIGHT // 2 + 170, (16, 16, 255), button_font, "BACK", colors, True).set_offset_pos()
    buttons = (button1, button2, button3, button4)
    options = MainMenu(title_text, buttons, None, (16, 16, 216))

    while options.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                options.exit()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    options.update_button("up")
                elif event.key == pygame.K_DOWN:
                    options.update_button("down")
                if options.button_pressed() == 0:
                    clear_data()
                elif options.button_pressed() == 1:
                    pass
                elif options.button_pressed() == 2:
                    window = toggle_fullscreen()
                    set_fullscreen()
                elif options.button_pressed() == 3:
                    options.exit()
                    current_state = menu_state

        if not no_joystick:
            if joy.get_hat(0) == (0, 1) and flag:
                options.update_button("up")
                flag = False
            elif joy.get_hat(0) == (0, -1) and flag:
                options.update_button("down")
                flag = False
            elif joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(1) and flag2:
                flag2 = False
                if options.button_pressed(True) == 0:
                    clear_data()
                elif options.button_pressed(True) == 1:
                    pass
                elif options.button_pressed(True) == 2:
                    window = toggle_fullscreen()
                    set_fullscreen()
                elif options.button_pressed(True) == 3:
                    options.exit()
                    current_state = menu_state
            elif not joy.get_button(1):
                flag2 = True

        options.show(window, WIDTH // 2 - 110, 100)
        pygame.display.flip()
        clock.tick(48)


def menu_state():
    global running, current_state

    flag = True
    flag2 = False
    button_font = pygame.font.SysFont("calibri", 55, True)
    best_score = load_best_score()
    best_font = pygame.font.SysFont("calibri", 30, True)
    score_text = best_font.render("Best Score: " + str(best_score[0]), True, (216, 216, 216))
    date_text = pygame.font.SysFont('calibri', 30, True).render(best_score[1], True, (216, 216, 216))
    title_text = pygame.font.SysFont("calibri", 85, True).render("Snakesss...", True, (240, 240, 240))
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2, HEIGHT // 2 - 100, (16, 16, 255), button_font, "PLAY", colors, True).set_offset_pos().set_selected()
    button2 = Button(WIDTH // 2, HEIGHT // 2 - 30, (16, 16, 255), button_font, "OPTIONS", colors, True).set_offset_pos()
    button3 = Button(WIDTH // 2, HEIGHT // 2 + 40, (16, 16, 255), button_font, "INSTRUCTIONS", colors, True).set_offset_pos()
    button4 = Button(WIDTH // 2, HEIGHT // 2 + 110, (16, 16, 255), button_font, "HIGH SCORES", colors, True).set_offset_pos()
    button5 = Button(WIDTH // 2, HEIGHT // 2 + 180, (16, 16, 255), button_font, "QUIT", colors, True).set_offset_pos()
    buttons = (button1, button2, button3, button4, button5)
    menu = MainMenu(title_text, buttons, None, (16, 16, 216))

    while menu.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.exit()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.update_button("up")
                elif event.key == pygame.K_DOWN:
                    menu.update_button("down")
                elif event.key == pygame.K_s:
                    print(load_best_score())
                if menu.button_pressed() == 0:
                    menu.exit()
                    current_state = game_state
                elif menu.button_pressed() == 1:
                    menu.exit()
                    current_state = options_state
                elif menu.button_pressed() == 2:
                    pass
                elif menu.button_pressed() == 3:
                    pass
                elif menu.button_pressed() == 4:
                    menu.exit()
                    running = False

        if not no_joystick:
            if joy.get_hat(0) == (0, 1) and flag:
                menu.update_button("up")
                flag = False
            elif joy.get_hat(0) == (0, -1) and flag:
                menu.update_button("down")
                flag = False
            if joy.get_hat(0) == (0, 0):
                flag = True
            if joy.get_button(1) and flag2:
                flag2 = False
                if menu.button_pressed(True) == 0:
                    menu.exit()
                    current_state = game_state
                elif menu.button_pressed(True) == 1:
                    menu.exit()
                    current_state = options_state
                elif menu.button_pressed(True) == 2:
                    pass
                elif menu.button_pressed(True) == 3:
                    pass
                elif menu.button_pressed(True) == 4:
                    menu.exit()
                    running = False
            elif not joy.get_button(1):
                flag2 = True

        menu.show(window, 55, 40)
        window.blit(score_text, (50, HEIGHT // 2 - 155))
        window.blit(date_text, (50, HEIGHT // 2 - 123))
        pygame.display.flip()
        clock.tick(48)


def game_state():
    global running

    score_font = pygame.font.SysFont("calibri", 35, True)
    score = 0
    snake = Snake()
    food = Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 48)

    game = Room()

    while game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
                running = False
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
                elif event.key == pygame.K_b:
                    snake.grow()
            elif event.type == MOVE:
                snake.move()
                if snake.collide():
                    game.exit()
                    if game_over_state() == 1:
                        running = False

        if not no_joystick:
            if joy.get_button(9):
                if pause_state() == 1:
                    game.exit()
            elif joy.get_button(3):
                snake.grow()
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
            food = Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
        snake.show()
        food.show()
        window.blit(score_font.render("SCORE: " + str(score), True, (255, 255, 255)), (WIDTH // 2 - 72, 38))
        show_fps()
        pygame.display.flip()
        clock.tick(48)

    save_best_score(score)


fullscreen = get_fullscreen()
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
window = toggle_fullscreen()
pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load("gfx\\snake.png").convert_alpha())
clock = pygame.time.Clock()
fps_font = pygame.font.SysFont("calibri", 16, True)

check_data_file()
joy = init_joystick()
current_state = menu_state

while running:
    current_state()

pygame.quit()
