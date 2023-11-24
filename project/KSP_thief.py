# Прописываем нижние две строки, чтобы не было пайгеймовской надписи "Hello from the pygame community"
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame # Импортируем библиотеку pygame
from random import randint
from random import random

FPS = 30 # Частота обновления кадров (30 к/с)


# Описываем цвета RGB-схемы
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# генерация студента каждые 2 секунды (в среднем)
prob_stud = 1/ (FPS*2)

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
TOP = 120

# координата кассы

PAY_DESK = WIDTH - 50

# расстояние между студентами
DS = 5

#координаты охранника в начале игры
x1 = LEFT
y1 = TOP + (HEIGHT - BOTTOM - TOP) /2

# время оплаты

pay_time = 1 * FPS


pygame.init() # Инициализируем библиотеку pygame


window=pygame.display.set_mode((WIDTH,HEIGHT)) # Задаем размеры игрового окна

#картинки
dollar = pygame.image.load('dollar.png').convert_alpha()
dollar = pygame.transform.scale(dollar, (40, 50))
dollar_rect = dollar.get_rect()


def decision(probability):
    """
    выдает 1 с данной вероятностью
    """
    return random() < probability



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
            self.y -= self.v # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться
            if self.y < TOP:
                self.y = TOP

        elif keys[pygame.K_DOWN]:
            self.y += self.v
            if self.y + self.r > HEIGHT - BOTTOM:
                self.y = HEIGHT - BOTTOM - self.r

    def draw(self):
        pygame.draw.rect(window, black, [self.x, self.y,self.r, self.r])

class Student():
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.money = 1
        self.v = 5
        self.r = 10
        self.x = -self.r
        self.y = 100
        self.state = 0
        # что делает студент
        # 0 - идет вдоль ленты
        # 1 - расплачивается
        # 2 - идет к столу
        self.color = green
        # время оплаты + время отхода от кассы
        self.pay_time = pay_time + 2 * self.r // self.v

    def move(self, obj):
        #учет студента спереди
        if obj and obj.state != 2 and obj.x - obj.r <= self.x + self.r + DS:
                self.x = obj.x - obj.r - self.r - DS
                return 
        if self.state == 0:
            self.x += self.v
            if self.x >= PAY_DESK:
                self.state = 1
            return
        if self.state == 1:
            if self.pay_time <= 2 * self.r // self.v:
                self.y += self.v
                if self.pay_time == 1:
                    self.state = 2
                else:
                    self.pay_time -= 1
            else:
                self.pay_time -= 1

    def pay(self):
        if self.state == 1:
            dollar.set_alpha(255 * (self.pay_time - 2 * self.r // self.v) // pay_time)
            dollar_rect.center = self.x, self.y - (pay_time - self.pay_time)
            self.window.blit(dollar, dollar_rect)
        
    def draw(self):
        pygame.draw.circle(self.window, self.color, (self.x, self.y), self.r)

class Thief(Student):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self.color = red
        self.money = 0
        self.pay_time = 2 * self.r // self.v
    





# Начало координат - левый верхний угол

clock = pygame.time.Clock() # Перменнная для подсчета времени

pygame.display.update() # Обновляем содержимое игрового поля
pygame.display.set_caption("KSP_thief") # Добавляем название игры в левом верхнем углу игрового окна
gameNow = True # Переменная, чтобы по ее значению понимать, идет игра или нет

security = Security(window, x1, y1)

students = []



# Функция pygame.event.get() возвращает все события, происходящие на игровом поле:
while gameNow:

    window.fill(white)
    security.draw()

    for s in students:
        s.draw()
        s.pay()
    
    pygame.display.update()
    clock.tick(FPS)
    
    #генерация студента
    if decision(prob_stud):
        if decision(prob_not_thief):
            students.append(Student(window))
        else:
            students.append(Thief(window))


    for event in pygame.event.get():

        if event.type==pygame.QUIT: # Если нажат крестик, то окно игры закрывается
            gameNow = False
        
    # Движение охранника
    keys = pygame.key.get_pressed()
    security.move(keys)

    for i in range(len(students)):
        if i == 0:
            #самый первый студент
            students[i].move(0)
        else:
            students[i].move(students[i - 1])
    
pygame.quit()
quit()






