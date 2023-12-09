from pictures import *
from constants import *
import pygame
from functions import *
from math import sin, cos, pi # для часов

class Student():
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.money = 1
        self.number_table = 0 # будем запоминать индекс стола, чтобы потом этот стол освобождать
        self.v = 5
        #self.v = 0.2
        self.r = 20
        self.x = -self.r
        self.y = 78

        #направление движения студента для правильной отрисовки
        self.direction = 'r' # right, left, down, up

        self.state = 0
        # что делает студент
        # 0 - идет вдоль ленты
        # 1 - расплачивается
        # 2 - отходит от кассы
        # 3 - идет к столу
        # 4 - ест
        # 5 - уходит
        # 6 -

        self.kill = 0 # Переменная, в которую запоминаем, подходил ли охранник или нет

        self.color = green

        # время оплаты + время отхода от кассы

        self.time_goaway = (2 * self.r + DS) // self.v
        self.pay_time = pay_time + self.time_goaway

    def move(self, obj):
        # учет студента спереди
        if obj and obj.state <= 2 and obj.x - obj.r <= self.x + self.r + DS:
            self.x = obj.x - obj.r - self.r - DS
            return
        if self.state == 0:
            self.x += self.v
            if self.x >= PAY_DESK:
                self.state = 1
            return
        if self.state == 1:
            if self.pay_time > 0:
                self.pay_time -= 1
            else:

                # студент выбирает место 
                if decision(0.5) and any(upper_active):
                    # c вероятносью 0.5 выбираем верхний ряд
                    self.state = 2

                    # находим все индексы свободных мест сверху
                    idx_free, = np.nonzero(upper_active)
                    # из свободных выбираем одно
                    idx_table = np.random.choice(idx_free)
                    self.number_table = idx_table # запоминаем индекс занятого стола, чтобы потом этот стол освободить
                    # направление взгляда когда будет сидеть за столом
                    direction = 'r' if idx_table % 2 == 0 else 'l'

                    self.table = (0, x_table_coord[idx_table], direction) 
                    # 0 - верхний стол, координата места по x, направление взгляда

                    # делаем место неактивным
                    upper_active[idx_table] = 0

                elif any(lower_active):
                    # c вероятносью 0.5 выбираем нижний ряд
                    self.state = 2

                    idx_free, = np.nonzero(lower_active)
                    idx_table = np.random.choice(idx_free)
                    direction = 'r' if idx_table % 2 == 0 else 'l'
                    self.table = (1, x_table_coord[idx_table], direction) 
                    # 1 - нижний стол, координата места по x, направление взгляда
                    lower_active[idx_table] = 0
                #else:
                    # если стол не выбран, то чел просто стоит
                 #   pass
        if self.state == 2:
            if self.time_goaway == 1:
                self.state = 3
            else:
                self.direction = 'd'
                self.y += self.v  
                self.time_goaway -= 1
        if self.state == 3:

            if (self.table[1] == self.x and self.y == upper_y) or (self.table[1] == self.x and self.y == lower_y):
                self.pay_time = 60
                self.state = 4
                print(self.pay_time, self.state)


            if self.table[0] == 0:
                # движение к верхнему столу
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
                # движение к нижнему столу
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
# self.state = 4 - кушает (прописано в eat)
        if self.state == 5:
            # студент уходит
            if self.x < - 2 * self.r: # освобождает индекс места, если ушел
                self.state = 6

            if self.table[0] == 0:
                # движение на выход от верхнего стола
                if self.y >= coridor2:
                    self.direction = 'u'
                    self.y -= self.v
                    if self.y <= coridor2:
                        self.y = coridor2 - 1
                elif self.x > -50:
                    self.direction = 'l'
                    self.x -= self.v



            else:
                # движение на выход от нижнего стола
                if self.y < coridor3:
                    self.direction = 'd'
                    self.y += self.v
                    if self.y >= coridor3:
                        self.y = coridor3
                elif self.x > -50:
                    self.direction = 'l'
                    self.x -= self.v

        if self.state == 6:
            # если ушел достаточно далеко, то освобождает место
            if self.table[0] == 0:
                upper_active[self.number_table] = 1
                self.state = 7
            else:
                lower_active[self.number_table] = 1
                self.state = 7
    def pay(self):
        if self.state == 1:
            dollar.set_alpha(255 * self.pay_time // pay_time)
            dollar_rect.center = self.x, self.y - (pay_time - self.pay_time)
            self.window.blit(dollar, dollar_rect)

    def eat(self):
        # часы, когда кушает
        if self.state == 4:
            if self.pay_time > 0:
                self.pay_time -= 1

                pygame.draw.circle(self.window, black, (self.x + 2, self.y), 17)
                pygame.draw.line(self.window, white, [self.x + 2, self.y],
                                 [self.x - 15 * sin(pi + 2 * pi / 60 * (60 - self.pay_time)),
                                  self.y + 15 * cos(pi + 2 * pi / 60 * (60 - self.pay_time))], 3)
            else:
                self.state = 5



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
        self.number_table = 0
        self.pay_time = 0

    def draw(self):
        # Если охранник поймал красного, то этот красный пропадает с игрового поля
        if self.kill == 0:
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
        else:
            if self.kill == 1:
                self.kill = 2
                self.state = 6 # меняем значение, чтобы часы не рисовались, когда игрока уже нет


    def hittest(self, obj):
        if ((obj.r / 2 + self.r) >= (((self.x - (obj.x + obj.r / 2)) ** 2 + (self.y - (obj.y + obj.r / 2)) ** 2)) ** 0.5) and self.kill == 0:
            self.kill = 1
            return True
        if self.x < 1 and self.kill == 0 and self.state > 2:
            print('NO')
            obj.live -= 1
            self.kill = 1 # меняем на 2, чтобы место не освобождалось постоянно, даже когда вора нет, а осободилось только 1 раз


        return False

