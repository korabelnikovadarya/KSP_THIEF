import pygame

class Barrier:  # КОЛОННЫ, СТОЛЫ
    def __init__(self, window, x, y, width, height, surface=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.surface = surface

    def draw(self):
        if self.surface is not None:
            self.window.blit(self.surface, (self.x, self.y))

    def collide(self, security) -> bool:
        security_rect = pygame.Rect(security.x, security.y, security.r, security.r)
        barrier_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return pygame.Rect.colliderect(barrier_rect, security_rect)
