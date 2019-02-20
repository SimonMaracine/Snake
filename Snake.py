from engine.room import Room, MainMenu
from engine.room_item import Button
import pygame
from random import randint
from vectors import Vector
from copy import deepcopy

GRID = 20  # todo make fullscreen option
WIDTH = 42 * GRID
HEIGHT = 32 * GRID
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


def show_score():
    score_text = score_font.render("SCORE: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (WIDTH / 2 - 64, 40))


def game_over_state() -> int:
    global running

    quit = 0
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    button_font = pygame.font.SysFont("calibri", 40, True)
    colors = ((0, 0, 0), (255, 255, 255))
    button1 = Button(WIDTH // 2 - 160, HEIGHT // 2, (16, 16, 220), button_font, "RESTART", colors, True)
    button2 = Button(WIDTH // 2 + 40, HEIGHT // 2, (16, 16, 220), button_font, "EXIT", colors, True)
    button1.set_selected()
    buttons = (button1, button2)
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
                elif event.key == pygame.K_r:
                    game_over.exit()
                if game_over.button_pressed() == 0:
                    game_over.exit()
                elif game_over.button_pressed() == 1:
                    game_over.exit()
                    running = False
                    quit = 1

        if not no_joystick:
            if joystick.get_button(1):
                if game_over.button_pressed(True) == 0:
                    game_over.exit()
                elif game_over.button_pressed(True) == 1:
                    game_over.exit()
                    running = False
                    quit = 1

        window.blit(background, (WIDTH // 4, HEIGHT // 4))
        background.fill((0, 0, 255))
        game_over.show(window, 0, 0)
        pygame.display.flip()
        clock.tick(48)

    return quit


def game_state():
    global running, score

    score = 0
    snake = Snake()
    food = Food(randint(0, 41) * GRID, randint(0, 31) * GRID)
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
                elif event.key == pygame.K_r:
                    game.exit()
                elif event.key == pygame.K_ESCAPE:
                    game.exit()
                    if game_over_state() == 1:
                        running = False
                elif event.key == pygame.K_b:
                    snake.grow()
            elif event.type == MOVE:
                snake.move()
                if snake.collide():
                    game.exit()
                    if game_over_state() == 1:
                        running = False

        if not no_joystick:
            if joystick.get_hat(0) == (-1, 0) and not snake.dirs["right"]:
                snake.dir = Vector(-snake.vel, 0, 0)
                snake.change_direction("left")
            elif joystick.get_hat(0) == (1, 0) and not snake.dirs["left"]:
                snake.dir = Vector(snake.vel, 0, 0)
                snake.change_direction("right")
            elif joystick.get_hat(0) == (0, 1) and not snake.dirs["down"]:
                snake.dir = Vector(0, -snake.vel, 0)
                snake.change_direction("up")
            elif joystick.get_hat(0) == (0, -1) and not snake.dirs["up"]:
                snake.dir = Vector(0, snake.vel, 0)
                snake.change_direction("down")

        window.fill((16, 16, 16))
        if snake.eat(food):
            snake.grow()
            score += 1
            food = Food(randint(0, 41) * GRID, randint(0, 31) * GRID)
        snake.show()
        food.show()
        show_score()
        show_fps()
        pygame.display.flip()
        clock.tick(48)


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

fps_font = pygame.font.SysFont("calibri", 16, True)
score_font = pygame.font.SysFont("calibri", 30, True)

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    no_joystick = False
else:
    joystick = None
    no_joystick = True

current_state = game_state

while running:
    current_state()

pygame.quit()
