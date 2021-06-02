import pygame

class Joueur:

    def affichage(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.velocity = 2
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        
    def mouvement(self, vitesse):
        self.rect.y += vitesse
        
        
    def move(self, dirn):
        if dirn == 0:
            self.x += self.velocity

        elif dirn == 1:
            self.x -= self.velocity

        elif dirn == 2:
            self.y -= self.velocity

        else:
            self.y += self.velocity