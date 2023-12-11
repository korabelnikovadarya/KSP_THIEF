from random import random
from pictures import *
import pygame

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
