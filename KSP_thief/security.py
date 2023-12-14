from pictures import *
from constants import *
import pygame
from functions import *
class Security():
    """
    Класс охранника отвечает за движение охранника.
    У охранника есть ограниченное количество жизней.
    В переменную score ведется подсчет количества очков -
    количества пойманный воров.
    Если у охранника закончатся жизни, игра прервется.
    """
    def __init__(self, window: pygame.Surface, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.live = live
        self.v = 10
        self.r = security_r
        self.direction = 'r'
        self.cont = pygame.Rect(self.x, self.y, self.r, self.r)

    def move(self, keys, barriers, students):
        if keys[pygame.K_LEFT]:
            self.x -= self.v
            self.direction = 'l'
            if self.x < LEFT:
                self.x = LEFT
            # проверяет столкновение с барьерами слева
            for b in barriers:
                if b.collide(self):
                    self.x = b.x + b.width

        elif keys[pygame.K_RIGHT]:
            self.x += self.v
            self.direction = 'r'
            if self.x + self.r > WIDTH - RIGHT:
                self.x = WIDTH - RIGHT - self.r
            # проверяет столкновение с барьерами справа
            for b in barriers:
                if b.collide(self):
                    self.x = b.x - self.r

        elif keys[pygame.K_UP]:
            self.y -= self.v
            self.direction = 'u'
            if self.y < TOP:
                self.y = TOP
            # проверяет столкновение с барьерами сверху
            for b in barriers:
                if b.collide(self):
                    self.y = b.y + b.height

        elif keys[pygame.K_DOWN]:
            self.y += self.v
            self.direction = 'd'
            if self.y + self.r > HEIGHT - BOTTOM:
                self.y = HEIGHT - BOTTOM - self.r
            # проверяет столкновение с барьерами снизу
            for b in barriers:
                if b.collide(self):
                    self.y = b.y - self.r

        sec_stud_collide(self, students)

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

    def draw_lifes(self):
        """
        отрисовывает количество жизней охраны
        """
        x = 150
        y = 550
        for i in range(self.live):
            draw_heart(self.window, x + i * heart_size * 1.5, y)
