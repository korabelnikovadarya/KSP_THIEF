from pictures import *
from constants import *
import pygame
from functions import *
class Button():
    def __init__(self, text, window: pygame.Surface, x, y, d_color, l_color):
        self.window = window
        self.x = x
        self.y = y
        self.d_color = d_color
        self.l_color = l_color
        self.text = text
        self.text_color = black
        self.text_size = 40
        self.active = 0
        self.width = 200
        self.height = 100
        self.growth = 1
        self.dy = 5

    def draw(self):
        pygame.draw.ellipse(self.window,
                            self.d_color,
                            (self.x - self.width * self.growth / 2,
                             self.y + self.dy - self.height * self.growth / 2,
                             self.width * self.growth,
                             self.height * self.growth))

        pygame.draw.ellipse(self.window,
                            self.l_color,
                            (self.x - self.width * self.growth / 2,
                             self.y - self.height * self.growth / 2,
                             self.width * self.growth,
                             self.height * self.growth))

        font = pygame.font.SysFont(None, int(self.text_size * self.growth))
        img = font.render(self.text, True, self.text_color)
        self.window.blit(img, (self.x - img.get_width() / 2, self.y - img.get_height() / 2))

    def activate(self, event):
        mouse_color = self.window.get_at(event.pos)
        font = pygame.font.SysFont(None, int(self.text_size * self.growth))
        img = font.render(self.text, True, self.text_color)
        text_area = img.get_rect(topleft=(self.x - img.get_width() / 2, self.y - img.get_height() / 2))
        if mouse_color == self.l_color or text_area.collidepoint(event.pos):
            self.active = 1
            self.growth = 1.2
        else:
            self.active = 0
            self.growth = 1

    def push(self):
        """
        если мышка находится на кнопке, то она активна, если в этот момент MOUSEBUTTONDOWN, то кнопка нажата
        """
        if self.active:
            return True
        else:
            return False

    def not_active(self):
        self.active = 0
        self.growth = 1
