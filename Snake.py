import pygame
from random import randint
import vectors
from copy import deepcopy

GRID = 20
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
        self.body = [vectors.Vector(0, 0, 0)]

    def show(self):
        for i in range(len(self.body)):
            pygame.draw.rect(window, (240, 240, 240), (self.body[i].x + 1, self.body[i].y + 1, self.width, self.width))

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


def main():
    global running
    run = True

    snake = Snake()
    food = Food(*Food.rand_location)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                snake.dir = vectors.Vector(snake.vel, 0, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                snake.dir = vectors.Vector(-snake.vel, 0, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                snake.dir = vectors.Vector(0, snake.vel, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                snake.dir = vectors.Vector(0, -snake.vel, 0)

        window.fill((0, 0, 0))
        if snake.eat(food):
            snake.grow()
            food = Food(randint(0, 41) * GRID, randint(0, 31) * GRID)
        snake.move()
        snake.show()
        food.show()
        show_fps()
        pygame.display.flip()
        clock.tick(16)


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

fps_font = pygame.font.SysFont("calibri", 16, True)

while running:
    main()

pygame.quit()
