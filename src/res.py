import os
import pygame

pygame.mixer.init(22050, -16, 2, 256)

button_sound = pygame.mixer.Sound(os.path.join("sounds", "button.wav"))
eat_sound = pygame.mixer.Sound(os.path.join("sounds", "eat.wav"))
hit_sound = pygame.mixer.Sound(os.path.join("sounds", "hit.wav"))
