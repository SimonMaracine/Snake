import pygame
from random import randint
import vectors
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
        self.dir = vectors.Vector(self.vel, 0, 0)
        self.body = [vectors.Vector(self.x, self.y, 0), vectors.Vector(self.x + GRID, self.y, 0), vectors.Vector(self.x + GRID * 2, self.y, 0)]
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.directions = [self.left, self.right, self.up, self.down]

    def show(self):
        for i in range(len(self.body)):
            pygame.draw.rect(window, (255, 255, 255), (self.body[i].x + 1, self.body[i].y + 1, self.width, self.width))
        pygame.draw.rect(window, (160, 160, 255), (self.body[i].x + 1, self.body[i].y + 1, self.width, self.width))

    def move(self):
        temp_body = deepcopy(self.body)
        head = temp_body[-1]
        for i in range(len(self.body) - 1):
            self.body[i] = self.body[i + 1]
        self.body.pop()
        head.x += self.dir.vector[0]
        head.y += self.dir.vector[1]
        self.body.append(head)

    def eat(self, food):
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

    def collide(self):
        x = self.body[-1].x
        y = self.body[-1].y
        for segment in self.body[0:len(self.body) - 1]:
            if segment.x + self.width > x + self.width / 2 > segment.x:
                if segment.y + self.width > y + self.width / 2 > segment.y:
                    return True
            else:
                return False

    # def direction(self, direct):
    #     for i in range(len(self.directions)):
    #         if self.directions[i] is direct:
    #             self.directions[i] = True
    #         else:
    #             self.directions[i] = False


class Food(object):
    rand_location = (randint(0, 41) * GRID, randint(0, 31) * GRID)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = GRID - 4
        self.color = (240, 100, 100)

    def show(self):
        pygame.draw.rect(window, self.color, (self.x + 2, self.y + 2, self.width, self.width))


def show_fps():
    fps_text = fps_font.render("FPS: " + str(round(clock.get_fps())), False, (255, 255, 255))
    window.blit(fps_text, (6, HEIGHT - 25))


def game_over_state():
    global running
    run = True
    q = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False
                q = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                run = False
    return q

def game_state():
    global running
    run = True

    snake = Snake()
    food = Food(*Food.rand_location)
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 60)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not snake.left:
                snake.dir = vectors.Vector(snake.vel, 0, 0)
                # snake.direction(snake.right)
                snake.left = False
                snake.right = True
                snake.up = False
                snake.down = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not snake.right:
                snake.dir = vectors.Vector(-snake.vel, 0, 0)
                # snake.direction(snake.left)
                snake.left = True
                snake.right = False
                snake.up = False
                snake.down = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and not snake.up:
                snake.dir = vectors.Vector(0, snake.vel, 0)
                # snake.direction(snake.down)
                snake.left = False
                snake.right = False
                snake.up = False
                snake.down = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not snake.down:
                snake.dir = vectors.Vector(0, -snake.vel, 0)
                # snake.direction(snake.up)
                snake.left = False
                snake.right = False
                snake.up = True
                snake.down = False
            if event.type == MOVE:
                snake.move()

        window.fill((16, 16, 16))
        if snake.eat(food):
            snake.grow()
            food = Food(randint(0, 41) * GRID, randint(0, 31) * GRID)
        if snake.collide():
            run = False
            if game_over_state() == 1:
                running = False
        snake.show()
        food.show()
        show_fps()
        pygame.display.flip()
        clock.tick(48)


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

fps_font = pygame.font.SysFont("calibri", 16, True)

current_state = game_state

while running:
    current_state()

pygame.quit()
