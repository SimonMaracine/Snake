class Room(object):
    def __init__(self, button_list=None, sound=None):
        self.run = True
        self.button_list = button_list
        self.sound = sound

    def show(self, surface, x, y):
        for button in self.button_list:
            button.show(surface)
            button.pressed()

    def update_button(self, direction):
        current_button = 0
        for i in range(len(self.button_list)):
            if self.button_list[i].selected:
                current_button = i
        if direction == "up":
            if self.button_list[current_button] != self.button_list[0]:
                self.button_list[current_button].set_selected()
                self.button_list[current_button - 1].set_selected()
        elif direction == "down":
            if self.button_list[current_button] != self.button_list[-1]:
                self.button_list[current_button].set_selected()
                self.button_list[current_button + 1].set_selected()

    def button_pressed(self, button=None) -> int:
        for i in range(len(self.button_list)):
            if self.button_list[i].pressed(button):
                if self.sound is not None:
                    self.sound.play()
                return i
        return 16

    def exit(self):
        self.run = False


class MainMenu(Room):
    def __init__(self, title, button_list, sound, bg_color):
        super().__init__(button_list, sound)
        self.title = title
        self.bg_color = bg_color

    def show(self, surface, x, y):
        surface.fill(self.bg_color)
        surface.blit(self.title, (x, y))
        for button in self.button_list:
            button.show(surface)
            button.pressed()


# class Settings(MainMenu):
#     def __init__(self, title, button_list, sound, bg_color, slider_list):
#         super().__init__(title, button_list, sound, bg_color)
#         self.slider_list = slider_list
#
#     def show(self, surface, x, y):
#         surface.fill(self.bg_color)
#         surface.blit(self.title, (x, y))
#         for button in self.button_list:
#             button.show(surface)
#             button.pressed()
#         for slider in self.slider_list:
#             slider.show(surface)
#             slider.pressed()
#             slider.change_volume()
