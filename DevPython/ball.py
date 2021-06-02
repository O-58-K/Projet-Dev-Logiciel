import pygame 
import random


class Ball:

    def affichage(self, surface):
        pygame.draw.rect(surface, (230,230,230), self.rect)
    
    def __init__(self, x, y, size, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.vitesse_Yrandom = random.randint(1, 1)
        
        
    def mouvement(self, vitesseX, vitesseY):
        self.vitesseX = 2
        self.vitesseY = 3
        self.rect.x = (self.rect.x + self.direction * vitesseX)
        self.rect.y += self.vitesse_Yrandom * vitesseY