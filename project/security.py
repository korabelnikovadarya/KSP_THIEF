from pictures import *
from constants import *
import pygame
from functions import *
from copy import copy
from typing import Tuple

class Security():
    def __init__(self, window: pygame.Surface, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.live = 3
        self.v = 10
        self.r = 35

        #
        # ВАЖНО! NEW_SECURITY - SECURITY В СЛЕДУЮЩИЙ МОМЕНТ ВРЕМЕНИ, ПО КОТОРОМУ ПРОВЕРЯТСЯ, НЕ СТОЛКНУЛСЯ ЛИ ОН СО СТОЛАМИ/КОЛОННАМИ
        self.cont = pygame.Rect(self.x, self.y, self.r, self.r)

    def move(self, keys):
        #
        new_security = copy(self)

        if keys[pygame.K_LEFT]:
            new_security.x -= new_security.v
            if new_security.x < LEFT:
                new_security.x = LEFT

        elif keys[pygame.K_RIGHT]:
            new_security.x += new_security.v
            if new_security.x + new_security.r > WIDTH - RIGHT:
                new_security.x = WIDTH - RIGHT - new_security.r

        elif keys[pygame.K_UP]:
            new_security.y -= new_security.v  # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться
            if new_security.y < TOP:
                new_security.y = TOP

        elif keys[pygame.K_DOWN]:
            new_security.y += new_security.v
            if new_security.y + new_security.r > HEIGHT - BOTTOM:
                new_security.y = HEIGHT - BOTTOM - new_security.r

        return new_security

    def draw(self):
        pygame.draw.rect(window, black, [self.x, self.y, self.r, self.r])

    def draw_lifes(self):
        """
        отрисовывает количество жизней охраны
        """
        x = 600
        y = 550
        for i in range(self.live):
            draw_heart(self.window, x + i * heart_size * 1.5, y)


