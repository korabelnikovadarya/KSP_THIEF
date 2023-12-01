# Прописываем нижние две строки, чтобы не было пайгеймовской надписи "Hello from the pygame community"
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame  # Импортируем библиотеку pygame
from random import randint, random
import time
# Начало отсчета времени
start = time.time()
FPS = 30  # Частота обновления кадров (30 к/с)

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
# картинки
# Доллар при оплате
dollar = pygame.image.load('dollar.png').convert_alpha()
dollar = pygame.transform.scale(dollar, (40, 50))
dollar_rect = dollar.get_rect()
# Сердечки-жизни охранника
heart = pygame.image.load('heart.png').convert_alpha()
heart = pygame.transform.scale(heart, (50, 50))
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


def decision(probability):
    # Выдает 1 с данной вероятностью
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
        #print(self.x, self.y)



class Student():
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.money = 1
        self.v = 5
        self.r = 20
        self.x = -self.r
        self.y = 78
        self.state = 0
        self.kill = 0 # Переменная, в которую запоминаем, подходил ли охранник или нет
        self.track = 0  # Задаем для студента "случайную" траекторию движения к столу
        # что делает студент
        # 0 - идет вдоль ленты
        # 1 - расплачивается
        # 2 - идет к столу
        self.color = green
        # время оплаты + время отхода от кассы
        self.time_goaway = (2 * self.r + DS) // self.v
        self.pay_time = pay_time + self.time_goaway
        self.yesno = 0
    def move(self, obj):
        # учет студента спереди
        if obj and obj.state == 0 and obj.x - obj.r <= self.x + self.r + DS:
            self.x = obj.x - obj.r - self.r - DS
            return
        if self.state == 0:
            self.x += self.v
            if self.x >= PAY_DESK:
                self.state = 1
            return
        if self.state == 1:
            if self.pay_time <= self.time_goaway:
                self.y += self.v
                if self.pay_time == 1:
                    self.state = 2
                else:
                    self.pay_time -= 1
            else:
                self.pay_time -= 1


    def pay(self):
        if self.state == 1:
            dollar.set_alpha(255 * (self.pay_time - self.time_goaway) // pay_time)
            dollar_rect.center = self.x, self.y - (pay_time - self.pay_time)
            self.window.blit(dollar, dollar_rect)


    def draw(self):
        # Если охранник поймал красного, то этот красный пропадает с игрового поля
        if not(self.kill == 1 and self.money == 0):
         pygame.draw.circle(self.window, self.color, (self.x, self.y), self.r)

         # Только один раз для данного студента выбираем траекторию движения
         if self.yesno == 0:
             self.track = randint(0, 1)
             #print(self.track)
             self.yesno = 1

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
# Класс с описанием траекторий движения студентов до столов
class Trajectory():
    def __init__(self, window: pygame.Surface):
        self.v = 5
        self.window = window

    def move0(self, obj):

        if obj.state == 2:
            obj.x += self.v *(720 - 720) / ((720 - 720)**2 + (345 - 80)**2)**0.5
            obj.y += self.v * (345 - 80) / ((720 - 720)** 2 + (345 - 80)** 2)** 0.5
            if obj.y > 345:
                obj.state = 3

        if obj.state == 3:
            obj.x += self.v * (120 - 700) / ((120 - 700) ** 2 + (345 - 345) ** 2) ** 0.5
            obj.y += self.v * (345 - 345) / ((120 - 700) ** 2 + (345 - 345) ** 2) ** 0.5
            if obj.x < 120:
                obj.state = 4

        if obj.state == 4:
            obj.x += self.v * (125 - 120) / ((125 - 120) ** 2 + (405 - 345) ** 2) ** 0.5
            obj.y += self.v * (405 - 345) / ((125 - 120) ** 2 + (405 - 345) ** 2) ** 0.5
            if obj.y > 405:
                obj.state = 5

            #obj.x += self.v * (120- 700) / ((120- 700) ** 2 + (345 - 345) ** 2) ** 0.5
            #obj.y += self.v * (345 - 345) / ((120- 700) ** 2 + (345 - 345) ** 2) ** 0.5


        '''
        print(obj.x, obj.y)
        if obj.state == 2:
            if obj.y < 515 and obj.x > 150:
                obj.y += self.v
            if obj.y >= 515 and obj.x >= 150:
                obj.x -= self.v
            if obj.x < 150 and obj.y > 415:
                obj.y = self.v
            if obj.x < 150 and obj.y <= 415:
                # Здесь может быть анимация еды:
                obj.x -= self.v
        '''


    def move1(self, obj):
        pass
        '''
        if obj.state == 2:
            if obj.y < 515 and obj.x > 150:
                obj.y += self.v
            if obj.y >= 515 and obj.x >= 150:
                obj.x -= self.v
            if obj.x < 150 and obj.y > 460:
                obj.y -= self.v

            if obj.x < 150 and obj.y <= 460:
                # Здесь может быть анимация еды:
                obj.x -= self.v
        '''

    def move2(self, obj):
        pass


# Начало координат - левый верхний угол

clock = pygame.time.Clock()  # Перменнная для подсчета времени

pygame.display.update()  # Обновляем содержимое игрового поля
pygame.display.set_caption("KSP_thief")  # Добавляем название игры в левом верхнем углу игрового окна
gameNow = True  # Переменная, чтобы по ее значению понимать, идет игра или нет

security = Security(window, x1, y1)
trajectory = Trajectory(window)
students = []

# Функция pygame.event.get() возвращает все события, происходящие на игровом поле:
while gameNow:
    # отслеживаем положение мыши на экране

    window.fill(white)
    window.blit(background, (0, 0))
    live = security.live

    if live == 1:
        window.blit(heart, (50, HEIGHT - 70), heart_rect)
    if live == 2:
        window.blit(heart, (50, HEIGHT - 70), heart_rect)
        window.blit(heart, (150, HEIGHT - 70), heart_rect)
    if live == 3:
        window.blit(heart, (50, HEIGHT - 70), heart_rect)
        window.blit(heart, (150, HEIGHT - 70), heart_rect)
        window.blit(heart, (250, HEIGHT - 70), heart_rect)
    if live < 1:
        gameNow = not (gameNow)

    security.draw()

    for s in students:
        s.draw()
        s.pay()
        s.hittest(security)
        if s.track == 0:
            trajectory.move0(s)
        elif s.track == 1:
            trajectory.move1(s)

    pygame.display.update()
    clock.tick(FPS)

    # генерация студента
    if decision(prob_stud):
        if decision(prob_not_thief):
            students.append(Student(window))
        else:
            students.append(Thief(window))

    for event in pygame.event.get():
        # Отслеживаем координаты мыши
        if event.type == pygame.MOUSEMOTION:
            xm, ym = event.pos
            print(xm, ym)

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







