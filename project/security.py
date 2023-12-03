from pictures import *
from constants import *
import pygame
from functions import *


class Security():
    def __init__(self, window: pygame.Surface, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.live = 3
        self.v = 10
        self.r = 50

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.v
            if self.x < LEFT:
                self.x = LEFT

        elif keys[pygame.K_RIGHT]:
            self.x += self.v
            if self.x + self.r > WIDTH - RIGHT:
                self.x = WIDTH - RIGHT - self.r

        elif keys[pygame.K_UP]:
            self.y -= self.v  # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться
            if self.y < TOP:
                self.y = TOP

        elif keys[pygame.K_DOWN]:
            self.y += self.v
            if self.y + self.r > HEIGHT - BOTTOM:
                self.y = HEIGHT - BOTTOM - self.r

    def draw(self):
        pygame.draw.rect(window, black, [self.x, self.y, self.r, self.r])

    def draw_lifes(self):
        """
        отрисовывает количество жизней охраны
        """
        x = 40
        y = 550
        for i in range(self.live):
            draw_heart(self.window, x + i * heart_size * 1.5, y)
