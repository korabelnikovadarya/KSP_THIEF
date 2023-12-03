from random import random
from pictures import *
import pygame

def decision(probability):
    # Выдает 1 с данной вероятностью
    return random() < probability

def draw_heart(screen, x, y):
    heart_rect.center = x, y
    screen.blit(heart, heart_rect)

def draw_seats(screen):
    for i in x_table_coord:
        pygame.draw.circle(screen, black, (i, lower_y), 5)

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
        img = font.render(str(score), True, black)
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

