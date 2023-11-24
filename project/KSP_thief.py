# Прописываем нижние две строки, чтобы не было пайгеймовской надписи "Hello from the pygame community"
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame # Импортируем библиотеку pygame
from random import randint
FPS = 30 # Частота обновления кадров (30 к/с)

pygame.init() # Инициализируем библиотеку pygame
# Описываем цвета RGB-схемы
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

go = 'None'
x1 = 0
y1 = 270
#money = 0
x = 5
window=pygame.display.set_mode((800,600)) # Задаем размеры игрового окна

# Координаты охранника
#x1 = 50 Координата охранника по Ох
#y1 = 50 Координата охранника по Оy
#x1_change = 0 Изменение координаты охранника по Ох
#y1_change = 0 Изменение координаты охранника по Оy

class Security():
    def __init__(self, window: pygame.Surface, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.live = 3
        self.v = 10

    def move(self, key):
        if key == pygame.K_LEFT:
            self.x -= self.v

        elif key == pygame.K_RIGHT:
            self.x += self.v

        elif key == pygame.K_UP:
            self.y -= self.v # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться

        elif key == pygame.K_DOWN:
            self.y += self.v

        else:
            print(0)

    def draw(self):
        pygame.draw.rect(window, black, [x1, y1, 50, 50])

class Student():
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.money = 1
        self.x = 5
        self.y = 80
        self.v = 10
        self.color = green

    def move(self):
        self.x += self.v

    def draw(self):
        pygame.draw.circle(self.window, black, (self.x, self.y), 25)

class Thief(Student):
    def __init__(self, window: pygame.Surface, money):
        super().__init__(window, money)
        self.color = red
    





# Начало координат - левый верхний угол

clock = pygame.time.Clock() # Перменнная для подсчета времени

pygame.display.update() # Обновляем содержимое игрового поля
pygame.display.set_caption("KSP_thief") # Добавляем название игры в левом верхнем углу игрового окна
gameNow = True # Переменная, чтобы по ее значению понимать, идет игра или нет

security = Security(window, x1, y1)
students = Student(window)

# Функция pygame.event.get() возвращает все события, происходящие на игровом поле:
while gameNow:

    for event in pygame.event.get():

        if event.type==pygame.QUIT: # Если нажат крестик, то окно игры закрывается
            gameNow = False

        # Движение охранника
        if event.type == pygame.KEYDOWN:
            security.move(event.key)
            print(event.key)

    window.fill(white)

    security.draw()
    students.move()
    students.draw()
    #students.new_students()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()






