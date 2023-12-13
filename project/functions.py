from random import random
from pictures import *
import pygame
from math import sin, cos, pi # для часов

def decision(probability):
    # Выдает 1 с данной вероятностью
    return random() < probability

def draw_game_score(score, x, y):
    height = 40
    width = 50
    d_coord = 5

    pygame.draw.rect(window, grey, (x - width / 2 - d_coord, y - height / 2 + d_coord, width, height))
    pygame.draw.rect(window, yellow, (x - width / 2, y - height / 2, width, height))
    pygame.draw.rect(window, black, (x - width / 2, y - height / 2, width, height), 5)
    font = pygame.font.SysFont(None, 35)

    img = font.render(str(score), True, black)
    window.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))

def draw_heart(screen, x, y):
    heart_rect.center = x, y
    screen.blit(heart, heart_rect)

def draw_seats(screen): # Черные точки-ориентиры для столов
    pass
    #for i in x_table_coord:
        #pygame.draw.circle(screen, black, (i, lower_y), 5)

def draw_score(window, score, record, new_record, x, y, width, height):
    d_coord = 15
    pygame.draw.rect(window, grey, (x - width / 2 - d_coord, y - height / 2 + d_coord, width, height))
    pygame.draw.rect(window, yellow, (x - width / 2, y - height / 2, width, height))
    pygame.draw.rect(window, black, (x - width / 2, y - height / 2, width, height), 5)

    if new_record:
        font = pygame.font.SysFont(None, int(height / 9))
        img = font.render('Новый рекорд!', True, black)
        window.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2 - height / 3))

        font = pygame.font.SysFont(None, int(height / 3))
        img = font.render(str(record), True, black)
        window.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))
    else:
        font = pygame.font.SysFont(None, int(height / 5))
        img = font.render('Ваш счет:', True, black)
        window.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2 - height / 3))

        font = pygame.font.SysFont(None, int(height / 3))
        img = font.render(str(score), True, black)
        window.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))

        font = pygame.font.SysFont(None, int(height / 9))
        img = font.render('Ваш рекорд: ' + str(record), True, black)
        window.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2 + height / 3))

<<<<<<< HEAD
def rules(window):
    # if gameNow==3:
        line_pos_y = 5
        line_pos_x = 5
        i = 0
        font = pygame.font.SysFont(None, rules_size)
        with open("Instructions.txt", encoding="utf8") as f:
            for line in f.readlines():
                for i in range(leng):
                    line_pos_y = line_pos_y + 25
                    new_line = line.rstrip().split('//')
                    instruct= font.render(new_line[i], True, black)
                    window.blit(instruct, (line_pos_x, line_pos_y))
=======
def stud_sec_collide(student, security) -> bool:
    # студент воткнулся в охранника
    student_rect = pygame.Rect(student.x - student.r, student.y - student.r, 2 * student.r, 2 * student.r)
    security_rect = pygame.Rect(security.x, security.y, security.r, security.r)
    if pygame.Rect.colliderect(student_rect, security_rect):
        student.touch = 1

        if (student.direction == 'd' and
            security.y < student.y + student.r):
            student.y = security.y - student.r 

        if (student.direction == 'u' and
            security.y + security.r > student.y - student.r):
            student.y = security.y + security.r + student.r 

        if (student.direction == 'l' and
            security.x + security.r > student.x - student.r):
            student.x = security.x + security.r + student.r

        if (student.direction == 'r' and
            security.x < student.x + student.r):
            student.x = security.x - student.r 

        return True
        
    student.touch = 0
    return False

def stud_stud_collide(s1, students) -> bool:
    # студент втыкается в студента
    s1_rect = pygame.Rect(s1.x - s1.r, s1.y - s1.r, 2 * s1.r, 2 * s1.r)
    for s2 in students:
        if s2 != s1:
            s2_rect = pygame.Rect(s2.x - s2.r, s2.y - s2.r, 2 * s2.r, 2 * s2.r)
            if pygame.Rect.colliderect(s1_rect, s2_rect):
                if (s1.direction == 'd' and
                    s2.y - s2.r < s1.y + s1.r):
                    s1.y = s2.y - s2.r - s1.r
                    return True
                if (s1.direction == 'u' and
                    s2.y + s2.r > s1.y - s1.r):
                    s1.y = s2.y + s2.r + s1.r
                    return True
                if (s1.direction == 'r' and
                    s2.x - s2.r < s1.x + s1.r):
                    s1.x = s2.x - s2.r - s1.r
                    return True
                if (s1.direction == 'l' and
                    s2.x + s2.r > s1.x - s1.r):
                    s1.x = s2.x + s2.r + s1.r
                    return True
    return False

def sec_stud_collide(security, students):
    #охранник воткнулся в студента
    security_rect = pygame.Rect(security.x, security.y, security.r, security.r)
    for student in students:
        student_rect = pygame.Rect(student.x - student.r, student.y - student.r, 2 * student.r, 2 * student.r)
        if pygame.Rect.colliderect(student_rect, security_rect):
            student.touch = 1
            if (security.direction == 'd' and
                student.y - student.r < security.y + security.r):
                security.y = student.y - student.r - security.r

            if (security.direction == 'u' and
                student.y + student.r > security.y):
                security.y = student.y + student.r

            if (security.direction == 'l' and
                student.x + student.r > security.x):
                security.x = student.x + student.r

            if (security.direction == 'r' and
                student.x - student.r < security.x + security.r):
                security.x = student.x - student.r - security.r

            return True
        
    return False

def draw_clock(window, x, y, time):
    r = 14
    width = 3
    length = 12

    pygame.draw.circle(window, black, (x, y), r)

    angle = 2 * pi * (eat_time - time) / eat_time

    top_left_x = x - width / 2 * cos(angle)
    top_left_y = y - width / 2 * sin(angle)

    top_right_x = x - width / 2 * cos(angle) + length * sin(angle)
    top_right_y = y - width / 2 * sin(angle) - length * cos(angle)

    bottom_left_x = x + width / 2 * cos(angle)
    bottom_left_y = y + width / 2 * sin(angle)

    bottom_right_x = x + width / 2 * cos(angle) + length * sin(angle)
    bottom_right_y = y + width / 2 * sin(angle) - length * cos(angle)

    pygame.draw.polygon(window, white, [
        (top_left_x, top_left_y),
        (top_right_x, top_right_y),
        (bottom_right_x, bottom_right_y),
        (bottom_left_x, bottom_left_y)
    ])
>>>>>>> refs/remotes/origin/main
