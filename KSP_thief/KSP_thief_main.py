from os import environ, chdir
import os
import pygame
import time
from constants import *
from pictures import *
from students import *
from functions import *
from security import *
from buttons import *
from barriers import *

# Не выводим надпись "Hello from the pygame community"
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Начало отсчета времени
start = time.time()

# Инициализируем библиотеку pygame
pygame.init()

# Задаем размеры игрового окна
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Перменнная для подсчета времени
clock = pygame.time.Clock()

# Обновляем содержимое игрового поля
pygame.display.update()

# Добавляем название игры в левом верхнем углу игрового окна
pygame.display.set_caption("KSP_thief")

gameNow = 1
# Переменная, чтобы по ее значению понимать, какая часть игры на экране
# 1 - start -  начальный экран
# 2 - game - игра идет
# 3 - rules - правила
# 4 - lose - экран проигрыша
# 0 - завершение игры

# кнопки
play_button = Button('Играть', window, 400, 450, d_green, l_green)
rules_button = Button('Правила', window, 150, 450, d_blue, l_blue)
exit_button = Button('Выход', window, 650, 450, d_red, l_red)
back_button = Button('К началу', window, 400, 500, d_blue, l_blue)

# барьеры
barriers = [
    Barrier(window, gc_x, gc_y, gc_width, gc_height, green_column),
    Barrier(window, rc_x, rc_y, rc_width, rc_height, red_column),
    Barrier(window, bc_x, bc_y, bc_width, bc_height, blue_column),
    Barrier(window, 744, 219, 56, 152)]  # колонны и серая стойка около кассы

# координата по ОХ левого края стола, ширина стола, высота стола
for x in tables_left_coords:
    barriers.append(Barrier(window, x, top_y_table, 0.8 * table_rect_width, table_height))
for x in tables_left_coords_2:
    barriers.append(Barrier(window, x, 540, 0.8 * table_rect_width, table_small_height))

# активность верхних и нижних мест
# 1 - место свободно
# 0 - место занято
upper_active = np.array([1] * n_tables * 2)
lower_active = np.array([1] * n_tables * 2)

security = Security(window, x1, y1)
students = []
score = 0
record = -1
new_record = False # поставил ли игрок новый рекорд в раунде

while gameNow:
    if gameNow == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                # Если нажат крестик, то окно игры закрывается
                gameNow = 0

        # region отрисовка экрана
        window.blit(background, (0, 0))
        security.draw()

        for s in students:
            s.draw()
            s.pay()
            s.eat(upper_active, lower_active)

            if s.hittest(security):
                score += 1
                # Если охранник поймал красного, то этот красный пропадает с игрового поля
                if s.state == 3 or s.state == 4:
                    if s.table[0] == 0:
                        upper_active[s.table[3]] = 1
                    if s.table[0] == 1:
                        lower_active[s.table[3]] = 1
                students.remove(s)
        
        draw_game_score(score, 50, 550)
        security.draw_lifes()
        pygame.display.update()
        clock.tick(FPS)
        # endregion

        # генерация студента
        if decision(prob_stud):
            if decision(prob_not_thief):
                students.append(Student(window))
            else:
                students.append(Thief(window))

        for s in students:
            # движение студентов
            s.move(security, students, upper_active, lower_active)
            # удаление неактивных студентов с поля
            if s.state == 6:
                if s.money == 0:
                    security.live -= 1
                students.remove(s)
        
        # Движение охранника
        keys = pygame.key.get_pressed()
        security.move(keys, barriers, students)
        
        if security.live < 1:
            gameNow = 4
            upper_active = np.array([1] * n_tables * 2)
            lower_active = np.array([1] * n_tables * 2)

            background.set_alpha(100)
            if score > record:
                record = score
                new_record = True
            else:
                new_record = False
            play_button.x, play_button.y = (200, 150)
            rules_button.x, rules_button.y = (200, 300) 
            exit_button.x, exit_button.y = (200, 450)
            score = 0

    elif gameNow == 4:
        window.fill(floor)
        background.set_alpha(100)
        window.blit(background, (0, 0))

        # рисую кнопки
        play_button.draw()
        rules_button.draw()
        exit_button.draw()

        # рисую счет
        draw_score(window, score, record, new_record, 600, 300, 300, 400)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameNow = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # проверка, нажаты ли кнопки
                if play_button.push():
                    gameNow = 2
                    background.set_alpha(255)
                    score = 0
                    security = Security(window, x1, y1)
                    students = []
                    upper_active = np.array([1] * n_tables * 2)
                    lower_active = np.array([1] * n_tables * 2)
                    play_button.not_active()
                if exit_button.push():
                    gameNow = 0
                if rules_button.push():
                    gameNow = 3
                    rules_button.not_active()
            elif event.type == pygame.MOUSEMOTION:
                # проверяю активацию кнопок
                play_button.activate(event)
                rules_button.activate(event)
                exit_button.activate(event)
    elif gameNow == 1:
        window.fill(floor)
        window.blit(background, (0, 0))
        window.blit(ksp, ksp_rect)
        play_button.draw()
        rules_button.draw()
        exit_button.draw()
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameNow = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.push():
                    gameNow = 2
                    background.set_alpha(255)
                    security = Security(window, x1, y1)
                    students = []
                    upper_active = np.array([1] * n_tables * 2)
                    lower_active = np.array([1] * n_tables * 2)
                    play_button.not_active()
                if exit_button.push():
                    gameNow = 0
                if rules_button.push():
                    gameNow = 3
                    background.set_alpha(100)
                    rules_button.not_active()
            elif event.type == pygame.MOUSEMOTION:
                play_button.activate(event)
                rules_button.activate(event)
                exit_button.activate(event)
    elif gameNow == 3:

        window.fill(floor)
        window.blit(background, (0, 0))
        rules(window)
        back_button.draw()
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameNow = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.push():
                    gameNow = 1
                    play_button.x, play_button.y = (400, 450)
                    rules_button.x, rules_button.y = (150, 450) 
                    exit_button.x, exit_button.y = (650, 450)
                    back_button.not_active()
                if exit_button.push():
                    gameNow = 0
            elif event.type == pygame.MOUSEMOTION:
                back_button.activate(event)
pygame.quit()
quit()







