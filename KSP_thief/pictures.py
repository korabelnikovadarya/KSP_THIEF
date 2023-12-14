import pygame
from constants import *

pygame.init()  # Инициализируем библиотеку pygame

window = pygame.display.set_mode((WIDTH, HEIGHT))  # Задаем размеры игрового окна

# картинки
# Доллар при оплате
dollar = pygame.image.load('images/dollar.png').convert_alpha()
dollar = pygame.transform.scale(dollar, (40, 50))
dollar_rect = dollar.get_rect()

# Сердечки-жизни охранника
heart = pygame.image.load('images/heart.png').convert_alpha()
heart_size = 50
heart = pygame.transform.scale(heart, (heart_size, heart_size))
heart_rect = heart.get_rect()

# Основной фон
background = pygame.image.load('images/background.jpg').convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Студенты
stud_green = pygame.image.load('images/student_green.png')
stud_green = pygame.transform.scale(stud_green, (35, 35))
stud_green_rect = stud_green.get_rect()
student_r = stud_green.get_width() / 2

stud_red = pygame.image.load('images/student_red.png')
stud_red = pygame.transform.scale(stud_red, (35, 35))
stud_red_rect = stud_red.get_rect()

stud_blue = pygame.image.load('images/student_blue.png')
stud_blue = pygame.transform.scale(stud_blue, (35, 35))
stud_blue_rect = stud_blue.get_rect()

ksp = pygame.image.load('images/ksp.png')
ksp = pygame.transform.scale(ksp, (400, 400))
ksp_rect = ksp.get_rect()
ksp_rect.center = 420, 200

security_pic = pygame.image.load('images/SECURITY.png')
security_pic = pygame.transform.scale(security_pic, (50, 50))
security_pic_rect = security_pic.get_rect()
security_r = security_pic.get_width()

# колонны
green_column = pygame.image.load('images/Green.png').convert_alpha()
gc_width = green_column.get_width()
gc_height = green_column.get_height()

gc_x, gc_y = (155, 214)

red_column = pygame.image.load('images/Red.png').convert_alpha()
rc_width = red_column.get_width()
rc_height = red_column.get_height()

rc_width = 86
rc_height = 86
rc_x, rc_y = (327, 214)

blue_column = pygame.image.load('images/Blue.png').convert_alpha()
bc_width = blue_column.get_width()
bc_height = blue_column.get_height()

bc_width = 86
bc_height = 86
bc_x, bc_y = (498, 214)
