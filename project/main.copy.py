# Прописываем нижние две строки, чтобы не было пайгеймовской надписи "Hello from the pygame community"
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame  # Импортируем библиотеку pygame
from random import randint, random


FPS = 30  # Частота обновления кадров (30 к/с)

pygame.init()  # Инициализируем библиотеку pygame

# Описываем цвета RGB-схемы
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

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
TOP = 100

# координаты охранника в начале игры
x1 = LEFT
y1 = TOP + (HEIGHT - BOTTOM - TOP) / 2

window = pygame.display.set_mode((WIDTH, HEIGHT))  # Задаем размеры игрового окна


# Координаты охранника
# x1 = 50 Координата охранника по Ох
# y1 = 50 Координата охранника по Оy
# x1_change = 0 Изменение координаты охранника по Ох
# y1_change = 0 Изменение координаты охранника по Оy

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
            self.y -= self.v  # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться
            if self.y < TOP:
                self.y = TOP

        elif keys[pygame.K_DOWN]:
            self.y += self.v
            if self.y + self.r > HEIGHT - BOTTOM:
                self.y = HEIGHT - BOTTOM - self.r

    def draw(self):
        pygame.draw.rect(window, black, [self.x, self.y, self.r, self.r])


class Student():
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.money = 1
        self.x = 5
        self.y = 80
        self.v = 10
        self.vy = 0
        self.r = 10
        self.state = 0
        # что делает студент
        # 0 - идет вдоль ленты
        # 1 - расплачивается
        # 2 - идет к столу
        self.color = green

    def move(self):
        if self.state == 0:
            self.x += self.v
        else:
            self.v = randint(-1,6)
            self.vy = randint(1, 5)
            self.y += self.vy
            self.x -= self.v

        if self.x > 500:
            self.state = 1
            self.vy = randint(1,5)

    def draw(self):
        pygame.draw.circle(self.window, self.color, (self.x, self.y), self.r)




class Thief(Student):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self.color = red
        self.money = 0


# Начало координат - левый верхний угол

clock = pygame.time.Clock()  # Перменнная для подсчета времени

pygame.display.update()  # Обновляем содержимое игрового поля
pygame.display.set_caption("KSP_thief")  # Добавляем название игры в левом верхнем углу игрового окна
gameNow = True  # Переменная, чтобы по ее значению понимать, идет игра или нет

security = Security(window, x1, y1)

students = []

# Функция pygame.event.get() возвращает все события, происходящие на игровом поле:
while gameNow:

    window.fill(white)

    security.draw()
    for s in students:
        s.move()
        s.draw()

    # генерация студента
    if decision(prob_stud):
        if decision(prob_not_thief):
            students.append(Student(window))

        else:
            students.append(Thief(window))

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # Если нажат крестик, то окно игры закрывается
            gameNow = False

    # Движение охранника
    keys = pygame.key.get_pressed()
    security.move(keys)

pygame.quit()
quit()
