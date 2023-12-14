import numpy as np
from barriers import *
import pygame

# константы
FPS = 30 # Частота обновления кадров

# Описываем цвета RGB-схемы
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
floor = (254, 251, 232)

# цвета игры
d_blue = (100, 131, 249)
l_blue = (201, 232, 235)
d_red = (234, 73, 85)
l_red = (255, 222, 197)
d_green = (78, 164, 120)
l_green = (203, 255, 169)
yellow = (246, 230, 107)
grey = (129, 129, 129)

# наборы мест и их активность
top_y_table = 392
second_row_x = 105
second_row_y = 570
table_small_height = 25
second_row_long = 695
table_rect_width = 43 # Ширина стола
table_height = 80 # Высота стола
# верхние и нижние места
upper_y = 405
lower_y = 460

left_x_table = 160 # Левый край левого стола по ОХ

# расстояние между стульями по обе стороны от одного стола
table_width = 68

# расстояние между стульями в проходе
table_gap = 35

# количество столов
n_tables = 5

x_table_coord = []
# Координаты для столов (чтобы охранник обходил эти столы)
tables_left_coords = [left_x_table + i * (table_width + table_gap) for i in range(5)]

# Координаты для столов нижнего ряда
tables_left_coords_2 = [second_row_x + i * (table_width + table_gap) for i in range(7)]

for i in range(n_tables):
    # левое место у i стола
    x_table_coord.append(left_x_table - 10 + i * (table_width + table_gap))
    # правое место у i стола
    x_table_coord.append(left_x_table - 15 + i * (table_width + table_gap) + table_width)

# y-координаты коридоров
coridor1 = 200
coridor2 = 345
coridor3 = 510

# правила игры
rules_size = 30
line_pos_x = 5
line_pos_y = 5
leng = 16

# генерация студента каждые 2 секунды (в среднем)
prob_stud = 1 / (FPS * 0.5)

# доля честных студентов
prob_not_thief = 0.5

# границы поля
WIDTH = 800
HEIGHT = 600

# границы слева, справа и снизу
RIGHT = 10
LEFT = 10
BOTTOM = 3

# ширина ленты выдачи
TOP = 123

# координата кассы
PAY_DESK = WIDTH - 90

# расстояние между студентами
DS = 5

# координаты охранника в начале игры
x1 = LEFT
y1 = TOP + (HEIGHT - BOTTOM - TOP) / 2

# время оплаты
pay_time = 1 * FPS

# время еды
eat_time = 2 * FPS

# Количество жизней охранника
live = 110
