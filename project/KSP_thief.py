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

go = 'None'
x1 = 0
y1 = 270
money = 0
x = 5
window=pygame.display.set_mode((1200,740)) # Задаем размеры игрового окна

# Координаты охранника
#x1 = 50 Координата охранника по Ох
#y1 = 50 Координата охранника по Оy
#x1_change = 0 Изменение координаты охранника по Ох
#y1_change = 0 Изменение координаты охранника по Оy

class Security():
    def __init__(self, window: pygame.Surface, x1, y1):
        self.window = window
        self.x1 = x1
        self.y1 = y1
        self.live = 3

    def move(self):
        x1 += x1_change
        y1 += y1_change

    def draw(self):
        pygame.draw.rect(window, black, [x1, y1, 50, 50])

class Students():
    def __init__(self, window: pygame.Surface, money):
        self.window = window
        self.money = randint(0,1)
        self.x = 5
        self.y = 80
        # 0 - without money((
        # 1 - with money
    def move(self):
        self.x += 1

    def draw(self):
        pygame.draw.circle(self.window, black, (self.x, self.y), 25)




# Начало координат - левый верхний угол

clock = pygame.time.Clock() # Перменнная для подсчета времени

pygame.display.update() # Обновляем содержимое игрового поля
pygame.display.set_caption("KSP_thief") # Добавляем название игры в левом верхнем углу игрового окна
gameNow = False # Переменная, чтобы по ее значению понимать, идет игра или нет

security = Security(window, x1, y1)
students = Students(window, money)

# Функция pygame.event.get() возвращает все события, происходящие на игровом поле:
while not gameNow:

    for event in pygame.event.get():

        if event.type==pygame.QUIT: # Если нажат крестик, то окно игры закрывается
            gameNow = True

        # Движение охранника
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -10
                y1_change = 0

                go = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                x1_change = 10
                y1_change = 0

                go = 'RIGHT'
            elif event.key == pygame.K_UP:
                x1_change = 0
                y1_change = -10 # Ставим здесь знак "минус", так как движение вверх, но координата по Оу должна уменьшаться

                go = 'UP'
            elif event.key == pygame.K_DOWN:
                x1_change = 0
                y1_change = 10

                go = 'DOWN'
        if event.type == pygame.KEYUP:

                go = 'None'

    window.fill(white)

    security.draw()
    students.move()
    students.draw()
    #students.new_students()
    pygame.display.update()

    if go == 'LEFT' or go == 'RIGHT' or go == 'UP' or go == 'DOWN':
        x1 += x1_change
        y1 += y1_change
    clock.tick(FPS)
pygame.quit()
quit()






