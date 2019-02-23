from pygame import draw, key, constants

class Button(object):
    def __init__(self, x, y, color, font, actual_text, colors, antial=False):
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.actual_text = actual_text
        self.antial = antial
        self.colors = colors
        self.highlight = False
        self.width = font.size(actual_text)[0] + 10
        self.height = font.size(actual_text)[1]
        self.selected = False

    def show(self, surface):
        draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.actual_text, self.antial, self.colors[0 if not self.highlight else 1])
        surface.blit(text, (self.x + 5, self.y + 2))

    def pressed(self, button=False) -> bool:
        if self.selected:
            self.highlight = True
            if key.get_pressed()[constants.K_RETURN] or button:
                return True
            else:
                return False
        else:
            self.highlight = False
            return False

    def set_selected(self):
        self.selected = not self.selected
        return self

    def set_offset_pos(self):
        self.x -= self.width / 2
        return self


# class VolumeSlider(object):
#     def __init__(self, x, y, color, colors, width, height):
#         self.x = x
#         self.y = y
#         self.color = color
#         self.colors = colors
#         self.highlight = False
#         self.width = width
#         self.height = height
#         self.bar_length = self.width - 12
#         self.volume = 1.0
#
#     def show(self, surface):
#         draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
#         draw.rect(surface, self.colors[0 if not self.highlight else 1], (self.x + 6, self.y + 8, self.bar_length, self.height - 18))
#
#     def pressed(self):
#         mouse_pos = mouse.get_pos()
#         if self.x + self.width > mouse_pos[0] > self.x:
#             if self.y + self.height > mouse_pos[1] > self.y:
#                 self.highlight = True
#                 if mouse.get_pressed()[0]:
#                     return True
#             else:
#                 self.highlight = False
#         else:
#             self.highlight = False
#             return False
#
#     def change_volume(self):
#         if self.pressed():
#             mouse_pos = mouse.get_pos()[0]
#             if mouse_pos <= self.x + self.width - 12:
#                 self.bar_length = mouse_pos - self.x
#                 if self.bar_length <= 2:
#                     self.volume = 0.0
#                 elif self.bar_length >= self.width - 14:
#                     self.volume = 1.0
#                 else:
#                     self.volume = (self.bar_length * 1.0) / (self.width - 12)
#
#     def reset_volume(self):
#         self.bar_length = self.width - 12
#         self.volume = 1.0
#
#     def set_volume(self, path):
#         with open(path, "r+") as data:
#             data.seek(4)
#             data.write(str(round(self.volume, 2)))
#
#     def get_volume(self, path):
#         with open(path, "r") as data:
#             self.volume = float(data.read()[4:7])
#         self.bar_length = int(self.volume * (self.width - 12))
