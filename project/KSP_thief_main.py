# Прописываем нижние две строки, чтобы не было пайгеймовской надписи "Hello from the pygame community"
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import os

print(os.getcwd())

import pygame  
# Импортируем библиотеку pygame

import time

from constants import *
from pictures import *
from students import *
from functions import *
from security import *
from buttons import *


# Начало отсчета времени
start = time.time()

pygame.init()  
# Инициализируем библиотеку pygame

window = pygame.display.set_mode((WIDTH, HEIGHT))  
# Задаем размеры игрового окна


clock = pygame.time.Clock()  
# Перменнная для подсчета времени

pygame.display.update()  
# Обновляем содержимое игрового поля

pygame.display.set_caption("KSP_thief")  
# Добавляем название игры в левом верхнем углу игрового окна

gameNow = 1
# Переменная, чтобы по ее значению понимать, какая часть игры на экране
# 1 - start -  начальный экран
# 2 - game - игра идет
# 3 - rules - правила
# 4 - lose - экран проигрыша
# 0 - завершение игры

security = Security(window, x1, y1)
students = []
SCORE = 0
RECORD = -1
new_record = False # поставил ли игрок новый рекорд в раунде

play_button = Button('Играть', window, 400, 450, d_green, l_green)
rules_button = Button('Правила', window, 150, 450, d_blue, l_blue)
exit_button = Button('Выход', window, 650, 450, d_red, l_red)
back_button = Button('К началу', window, 400, 500, d_blue, l_blue)

# Функция pygame.event.get() возвращает все события, происходящие на игровом поле:
while gameNow:
    if gameNow == 2:

        #region отрисовка экрана
        window.blit(background, (0, 0))
        security.draw_lifes()

        #отладочная печать
        draw_seats(window)

        security.draw()

        for s in students:
            s.draw()
            s.pay()
            if s.hittest(security):
                SCORE += 1


        pygame.display.update()
        clock.tick(FPS)
        #endregion 

        # генерация студента
        if decision(prob_stud):
            if decision(prob_not_thief):
                students.append(Student(window))
            else:
                students.append(Thief(window))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                # Если нажат крестик, то окно игры закрывается
                gameNow = 0

        # Движение охранника
        keys = pygame.key.get_pressed()
        security.move(keys)

        for i in range(len(students)):
            if i == 0:
                # самый первый студент
                students[i].move(0)
            else:
                students[i].move(students[i - 1])
        
        if security.live < 1:
            gameNow = 4
            background.set_alpha(100)
            if SCORE > RECORD:
                RECORD = SCORE
                new_record = True
            else:
                new_record = False
            play_button.x, play_button.y = (200, 150)
            rules_button.x, rules_button.y = (200, 300) 
            exit_button.x, exit_button.y = (200, 450)

        
    elif gameNow == 4:
        window.fill(white)
        background.set_alpha(100)
        window.blit(background, (0, 0))

        play_button.draw()
        rules_button.draw()
        exit_button.draw()

        draw_score(window, SCORE, RECORD, new_record, 600, 300, 300, 400)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameNow = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.push():
                    gameNow = 2
                    background.set_alpha(255)
                    SCORE = 0
                    security = Security(window, x1, y1)
                    students = []
                    play_button.not_active()
                if exit_button.push():
                    gameNow = 0
                if rules_button.push():
                    gameNow = 3
                    rules_button.not_active()
            elif event.type == pygame.MOUSEMOTION:
                play_button.activate(event)
                rules_button.activate(event)
                exit_button.activate(event)
    elif gameNow == 1:
        window.fill(white)
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
                    play_button.not_active()
                if exit_button.push():
                    gameNow = 0
                if rules_button.push():
                    gameNow = 3
                    rules_button.not_active()
            elif event.type == pygame.MOUSEMOTION:
                play_button.activate(event)
                rules_button.activate(event)
                exit_button.activate(event)
    elif gameNow == 3:

        window.fill(white)
        background.set_alpha(100)
        window.blit(background, (0, 0))
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







