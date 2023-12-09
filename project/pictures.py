import pygame
from constants import *

pygame.init()  # Инициализируем библиотеку pygame

window = pygame.display.set_mode((WIDTH, HEIGHT))  # Задаем размеры игрового окна

#картинки

# Доллар при оплате
# dollar = pygame.image.load('project/dollar.png').convert_alpha()
dollar = pygame.image.load('project/dollar.png').convert_alpha()
dollar = pygame.transform.scale(dollar, (40, 50))
dollar_rect = dollar.get_rect()

# Сердечки-жизни охранника
heart = pygame.image.load('project/heart.png').convert_alpha()
heart_size = 50
heart = pygame.transform.scale(heart, (heart_size, heart_size))
heart_rect = heart.get_rect()

# Основной фон
background = pygame.image.load('project/background.jpg').convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Еда
food1 = pygame.image.load('project/food1.png').convert_alpha()
food1 = pygame.transform.scale(food1, (40, 50))
food1_rect = food1.get_rect()

food2 = pygame.image.load('project/food2.png').convert_alpha()
food2 = pygame.transform.scale(food2, (40, 50))
food2_rect = food2.get_rect()

# Студенты

stud_green = pygame.image.load('project/student_green.png')
stud_green = pygame.transform.scale(stud_green, (50, 50))
stud_green_rect = stud_green.get_rect()

stud_red = pygame.image.load('project/student_red.png')
stud_red = pygame.transform.scale(stud_red, (50, 50))
stud_red_rect = stud_red.get_rect()

stud_blue = pygame.image.load('project/student_blue.png')
stud_blue = pygame.transform.scale(stud_blue, (50, 50))
stud_blue_rect = stud_blue.get_rect()

ksp = pygame.image.load('project/ksp.png')
ksp = pygame.transform.scale(ksp, (400, 400))
ksp_rect = ksp.get_rect()
ksp_rect.center = 420, 200
