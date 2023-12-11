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
        self.live = live
        self.v = 10
        self.r = security_r
        self.direction = 'r'

        #
        # ВАЖНО! NEW_SECURITY - SECURITY В СЛЕДУЮЩИЙ МОМЕНТ ВРЕМЕНИ, ПО КОТОРОМУ ПРОВЕРЯТСЯ, НЕ СТОЛКНУЛСЯ ЛИ ОН СО СТОЛАМИ/КОЛОННАМИ
        self.cont = pygame.Rect(self.x, self.y, self.r, self.r)

    def move(self, keys, barriers, students):

        if keys[pygame.K_LEFT]:
            self.x -= self.v
            self.direction = 'l'
            if self.x < LEFT:
                self.x = LEFT
            #проверяет столкновение с барьерами слева
            for b in barriers:
                if b.collide(self):
                    self.x = b.x + b.width

        if keys[pygame.K_RIGHT]:
            self.x += self.v
            self.direction = 'r'
            if self.x + self.r > WIDTH - RIGHT:
                self.x = WIDTH - RIGHT - self.r
            #проверяет столкновение с барьерами справа
            for b in barriers:
                if b.collide(self):
                    self.x = b.x - self.r

        if keys[pygame.K_UP]:
            self.y -= self.v  # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться
            self.direction = 'u'
            if self.y < TOP:
                self.y = TOP
            #проверяет столкновение с барьерами сверху
            for b in barriers:
                if b.collide(self):
                    self.y = b.y + b.height

        if keys[pygame.K_DOWN]:
            self.y += self.v
            self.direction = 'd'
            if self.y + self.r > HEIGHT - BOTTOM:
                self.y = HEIGHT - BOTTOM - self.r
            #проверяет столкновение с барьерами снизу
            for b in barriers:
                if b.collide(self):
                    self.y = b.y - self.r

        sec_stud_collide(self, students)

    #region new_security version
    """ new_security version
    def move(self, keys):
        new_security = copy(self)

        if keys[pygame.K_LEFT]:
            new_security.x -= new_security.v
            new_security.direcion = 'l'
            if new_security.x < LEFT:
                new_security.x = LEFT

        elif keys[pygame.K_RIGHT]:
            new_security.x += new_security.v
            new_security.direction = 'r'
            if new_security.x + new_security.r > WIDTH - RIGHT:
                new_security.x = WIDTH - RIGHT - new_security.r

        elif keys[pygame.K_UP]:
            new_security.y -= new_security.v  # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться
            new_security.direction = 'u'
            if new_security.y < TOP:
                new_security.y = TOP

        elif keys[pygame.K_DOWN]:
            new_security.y += new_security.v
            new_security.direction = 'd'
            if new_security.y + new_security.r > HEIGHT - BOTTOM:
                new_security.y = HEIGHT - BOTTOM - new_security.r

        return new_security
    """
    #endregion

    def draw(self):
        if self.direction == 'r':
            angle = 0
        elif self.direction == 'l':
            angle = 180
        elif self.direction == 'd':
            angle = 270
        elif self.direction == 'u':
            angle = 90
        pic = pygame.transform.rotate(security_pic, angle)
        security_pic_rect.topleft = self.x, self.y
        self.window.blit(pic, security_pic_rect)
        pygame.draw.rect(self.window, red, security_pic_rect, 2)


        #pygame.draw.rect(self.window, black, (self.x, self.y, self.r, self.r))

    def draw_lifes(self):
        """
        отрисовывает количество жизней охраны
        """
        x = 150
        y = 550
        for i in range(self.live):
            draw_heart(self.window, x + i * heart_size * 1.5, y)


