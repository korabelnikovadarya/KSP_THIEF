# Прописываем нижние две строки, чтобы не было пайгеймовской надписи "Hello from the pygame community"
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import os

print(os.getcwd())

import pygame  # Импортируем библиотеку pygame
from random import randint, random
import numpy as np
import time
# Начало отсчета времени
start = time.time()

#region константы
FPS = 30  # Частота обновления кадров (30 к/с)

# Описываем цвета RGB-схемы
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# наборы мест и их активность
upper_y = 405
lower_y = 460
left_x_table = 145
table_width = 68
table_gap = 35
n_tables = 5

x_table_coord = []

upper_active = np.array([1] * n_tables * 2)
lower_active = np.array([1] * n_tables * 2)

for i in range(n_tables):
    x_table_coord.append(left_x_table + i * (table_width + table_gap))
    x_table_coord.append(left_x_table + i * (table_width + table_gap) + table_width)


# y-координаты коридоров
coridor1 = 200
coridor2 = 345
coridor3 = 510

                       

# генерация студента каждые 2 секунды (в среднем)
prob_stud = 1 / (FPS * 2)

# доля честных студентов
prob_not_thief = 0.5

# границы поля
WIDTH = 800
HEIGHT = 600

# границы слева, справа и снизу

RIGHT = 10
LEFT = 10
BOTTOM = 10

# ширина ленты выдачи
TOP = 123

# координата кассы

PAY_DESK = WIDTH - 75

# расстояние между студентами
DS = 5

# координаты охранника в начале игры
x1 = LEFT
y1 = TOP + (HEIGHT - BOTTOM - TOP) / 2

# время оплаты

pay_time = 1 * FPS

pygame.init()  # Инициализируем библиотеку pygame

window = pygame.display.set_mode((WIDTH, HEIGHT))  # Задаем размеры игрового окна

# Количество жизней охранника
live = 3
#endregion

#region картинки
# Доллар при оплате
dollar = pygame.image.load('dollar.png').convert_alpha()
dollar = pygame.transform.scale(dollar, (40, 50))
dollar_rect = dollar.get_rect()

# project/

# Сердечки-жизни охранника
heart = pygame.image.load('heart.png').convert_alpha()
heart_size = 50
heart = pygame.transform.scale(heart, (heart_size, heart_size))
heart_rect = heart.get_rect()

# Основной фон
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Еда
food1 = pygame.image.load('food1.png').convert_alpha()
food1 = pygame.transform.scale(food1, (40, 50))
food1_rect = food1.get_rect()

food2 = pygame.image.load('food2.png').convert_alpha()
food2 = pygame.transform.scale(food2, (40, 50))
food2_rect = food2.get_rect()

# Студенты

stud_green = pygame.image.load('student_green.png')
stud_green = pygame.transform.scale(stud_green, (50, 50))
stud_green_rect = stud_green.get_rect()

stud_red = pygame.image.load('student_red.png')
stud_red = pygame.transform.scale(stud_red, (50, 50))
stud_red_rect = stud_red.get_rect()

stud_blue = pygame.image.load('student_blue.png')
stud_blue = pygame.transform.scale(stud_blue, (50, 50))
stud_blue_rect = stud_blue.get_rect()

#endregion

def decision(probability):
    # Выдает 1 с данной вероятностью
    return random() < probability

def draw_heart(screen, x, y):
    heart_rect.center = x, y
    screen.blit(heart, heart_rect)

def draw_seats(screen):
    for i in x_table_coord:
        pygame.draw.circle(screen, black, (i, lower_y), 5)


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
        if ((obj.r / 2 + self.r) >= (((self.x - (obj.x + obj.r / 2)) ** 2 + (self.y - (obj.y + obj.r / 2)) ** 2)) ** 0.5) and self.money == 1 and self.kill == 0:
            obj.live -= 1
            self.kill = 1 # Ставим единицу, чтобы больше жизни у охранника не отнимались из-за данного студента
        if ((obj.r / 2 + self.r) >= (((self.x - (obj.x + obj.r / 2)) ** 2 + (self.y - (obj.y + obj.r / 2)) ** 2)) ** 0.5) and self.money == 0:
            self.kill = 1



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


clock = pygame.time.Clock()  # Перменнная для подсчета времени

pygame.display.update()  # Обновляем содержимое игрового поля
pygame.display.set_caption("KSP_thief")  # Добавляем название игры в левом верхнем углу игрового окна
gameNow = True  # Переменная, чтобы по ее значению понимать, идет игра или нет

security = Security(window, x1, y1)
students = []

# Функция pygame.event.get() возвращает все события, происходящие на игровом поле:
while gameNow:
    window.blit(background, (0, 0))
    security.draw_lifes()

    #отладочная печать
    draw_seats(window)

    if security.live < 1:
        gameNow = not (gameNow)

    security.draw()

    for s in students:
        s.draw()
        s.pay()
        s.hittest(security)

    pygame.display.update()
    clock.tick(FPS)

    # генерация студента
    if decision(prob_stud):
        if decision(prob_not_thief):
            students.append(Student(window))
        else:
            students.append(Thief(window))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # Если нажат крестик, то окно игры закрывается
            gameNow = False

    # Движение охранника
    keys = pygame.key.get_pressed()
    security.move(keys)

    for i in range(len(students)):
        if i == 0:
            # самый первый студент
            students[i].move(0)
        else:
            students[i].move(students[i - 1])


pygame.quit()
quit()







