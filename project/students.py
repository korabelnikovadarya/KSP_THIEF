from pictures import *
from constants import *
import pygame
from functions import *


class Student():
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.money = 1
        self.v = 5
        self.r = 20
        self.x = -self.r
        self.y = 78

        #направление движения студента для правильной отрисовки
        self.direction = 'r' # right, left, down, up

        self.state = 0
        # что делает студент
        # 0 - идет вдоль ленты
        # 1 - расплачивается
        # 2 - идет к столу
        # 3 - ест

        self.kill = 0 # Переменная, в которую запоминаем, подходил ли охранник или нет

        self.color = green

        # время оплаты + время отхода от кассы
        self.time_goaway = (2 * self.r + DS) // self.v
        self.pay_time = pay_time + self.time_goaway

    def move(self, obj):
        # учет студента спереди
        if obj and obj.state <= 1 and obj.x - obj.r <= self.x + self.r + DS:
            self.x = obj.x - obj.r - self.r - DS
            return
        if self.state == 0:
            self.x += self.v
            if self.x >= PAY_DESK:
                self.state = 1
            return
        if self.state == 1:
            if self.pay_time <= self.time_goaway:
                self.direction = 'd'
                self.y += self.v
                if self.pay_time == 1:
                    self.state = 2
                    # студент выбирает место 
                    if decision(0.5) and any(upper_active):
                        idx_free, = np.nonzero(upper_active)
                        idx_table = np.random.choice(idx_free)
                        direction = 'r' if idx_table % 2 == 0 else 'l'
                        self.table = (0, x_table_coord[idx_table], direction) 
                        # 0 - верхний стол, координата места по x, направление взгляда
                        upper_active[idx_table] = 0
                    else:
                        idx_free, = np.nonzero(lower_active)
                        idx_table = np.random.choice(idx_free)
                        direction = 'r' if idx_table % 2 == 0 else 'l'
                        self.table = (1, x_table_coord[idx_table], direction) 
                        # 1 - нижний стол, координата места по x, направление взгляда
                        lower_active[idx_table] = 0
                else:
                    self.pay_time -= 1
            else:
                self.pay_time -= 1
        if self.state == 2:
            if self.table[0] == 0:
                if self.y < coridor2:
                    self.direction = 'd'
                    self.y += self.v 
                    if self.y >= coridor2:
                        self.y = coridor2
                elif self.x > self.table[1]:
                    self.direction = 'l'
                    self.x -= self.v
                    if self.x <= self.table[1]:
                        self.x = self.table[1]
                elif self.y < upper_y:
                    self.direction = 'd'
                    self.y += self.v 
                    if self.y >= upper_y:
                        self.y = upper_y
                        self.state = 3
                        self.direction = self.table[2]
            else:
                if self.y < coridor3 and self.x > self.table[1]:
                    self.direction = 'd'
                    self.y += self.v 
                    if self.y >= coridor3:
                        self.y = coridor3
                elif self.x > self.table[1]:
                    self.direction = 'l'
                    self.x -= self.v
                    if self.x <= self.table[1]:
                        self.x = self.table[1]
                elif self.y > lower_y:
                    self.direction = 'u'
                    self.y -= self.v 
                    if self.y <= lower_y:
                        self.y = lower_y
                        self.state = 3
                        self.direction = self.table[2]


    def pay(self):
        if self.state == 1:
            dollar.set_alpha(255 * (self.pay_time - self.time_goaway) // pay_time)
            dollar_rect.center = self.x, self.y - (pay_time - self.pay_time)
            self.window.blit(dollar, dollar_rect)

    def eat(self):
        pass

    def draw(self):
        if self.direction == 'r':
            angle = 0
        elif self.direction == 'l':
            angle = 180
        elif self.direction == 'd':
            angle = 270
        elif self.direction == 'u':
            angle = 90
        
        if self.state == 0:
            pic = pygame.transform.rotate(stud_blue, angle)
            stud_blue_rect.center = self.x, self.y
            self.window.blit(pic, stud_blue_rect)
        else:
            pic = pygame.transform.rotate(stud_green, angle)
            stud_green_rect.center = self.x, self.y
            self.window.blit(pic, stud_green_rect)


    # Проверяем, находится ли охранник рядом со студентом, который не является вором, если да, то количество жизней охранника уменьшается
    def hittest(self, obj):
        if ((obj.r / 2 + self.r) >= (((self.x - (obj.x + obj.r / 2)) ** 2 + (self.y - (obj.y + obj.r / 2)) ** 2)) ** 0.5) and self.kill == 0:
            obj.live -= 1
            self.kill = 1 # Ставим единицу, чтобы больше жизни у охранника не отнимались из-за данного студента
        return False



class Thief(Student):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self.color = red
        self.money = 0
        self.pay_time = self.time_goaway

    def draw(self):
        # Если охранник поймал красного, то этот красный пропадает с игрового поля
        if not self.kill:
            if self.direction == 'r':
                angle = 0
            elif self.direction == 'l':
                angle = 180
            elif self.direction == 'd':
                angle = 270
            elif self.direction == 'u':
                angle = 90
            if self.state == 0:
                pic = pygame.transform.rotate(stud_blue, angle)
                stud_blue_rect.center = self.x, self.y
                self.window.blit(pic, stud_blue_rect)
            else:
                pic = pygame.transform.rotate(stud_red, angle)
                stud_red_rect.center = self.x, self.y
                self.window.blit(pic, stud_red_rect)
    
    def hittest(self, obj):
        if ((obj.r / 2 + self.r) >= (((self.x - (obj.x + obj.r / 2)) ** 2 + (self.y - (obj.y + obj.r / 2)) ** 2)) ** 0.5) and self.kill == 0:
            self.kill = 1
            return True
        return False

