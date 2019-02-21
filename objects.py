from pygame import draw
from vectors import Vector
from copy import deepcopy


def import_obj():
    from Snake import GRID, WIDTH, HEIGHT, window

    class Snakes(object):
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
                draw.rect(window, (255, 255, 255), (self.body[i].x + 1, self.body[i].y + 1, self.width, self.width))
            draw.rect(window, (160, 160, 255), (self.body[-1].x + 1, self.body[-1].y + 1, self.width, self.width))

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
            draw.rect(window, self.color, (self.x + 3, self.y + 3, self.width, self.width))


    return Snakes, Food
