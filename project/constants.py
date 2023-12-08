import numpy as np

#константы
FPS = 30  # Частота обновления кадров (30 к/с)

# Описываем цвета RGB-схемы
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

#цвета игры
d_blue = (100, 131, 249)
l_blue = (201, 232, 235)
d_red = (234, 73, 85)
l_red = (255, 222, 197)
d_green = (78, 164, 120)
l_green = (203, 255, 169)
yellow = (246, 230, 107)
grey = (129, 129, 129)



""" наборы мест и их активность """

#верхние и нижние места
upper_y = 405
lower_y = 460

left_x_table = 145

#расстояние между стульями по обе стороны от одного стола
table_width = 68

#расстояние между стульями в проходе
table_gap = 35

#количество столов
n_tables = 5

#координаты мест
x_table_coord = []

#активность верзних и нижних мест
# 1 - место свободно
# 0 - место занято
upper_active = np.array([1] * n_tables * 2)
lower_active = np.array([1] * n_tables * 2)

for i in range(n_tables):
    # левое место у i стола
    x_table_coord.append(left_x_table + i * (table_width + table_gap))
    # правое место у i стола
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

# Количество жизней охранника
live = 3