from math import cos
import socket
import threading
import pygame
import sys
import random
import math
from joueur import Joueur 
from ball import Ball

clock=pygame.time.Clock()

class Jeu:
    
    def __init__(self):
        
        self.ecran = pygame.display.set_mode((900, 500))
        pygame.display.set_caption('jeu pong')
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = '169.254.230.36', 80
        self.client, self.adresse = None, None
        self.server.bind((self.ip, self.port))
        self.server.listen(1)

        self.positionY = 250
        self.direct = True

        self.JoueurX1, self.JoueurY1 = 20, 250
        self.JoueurX2, self.JoueurY2 = 860, 250

        self.Joueur_size = [20, 80]
        self.vitesseY1, self.vitesseY2 = 0, 0
        self.Joueur1 = Joueur(self.JoueurX1, self.JoueurY1, self.Joueur_size)
        self.Joueur2 = Joueur(self.JoueurX2, self.JoueurY2, self.Joueur_size)

        self.rect = pygame.Rect(0, 0, 900, 500)
        self.score1, self.score2 = 0, 0
        self.ball_direction = [-1, 1]
        self.ball = Ball(450, 250, [20, 20], random.choice(self.ball_direction))
        self.ball_shot = False
        self.ballVx, self.ballVy = 1, 1
      
    def principal(self):
        
        self.threadC(self.connexion)
        
        while self.direct:

            clock.tick(400)
            
            for event in pygame.event.get():

                if event.type == pygame.quit:
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.vitesseY1 = -1

                    if event.key == pygame.K_DOWN:
                        self.vitesseY1 = 1
                        
                    if event.key == pygame.K_z:
                        self.vitesseY2 = -1

                    if event.key == pygame.K_s:
                        self.vitesseY2 = 1
                        
                    if event.key == pygame.K_SPACE:
                        self.ball_shot = True 
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.vitesseY1 = 0

                    if event.key == pygame.K_DOWN:
                        self.vitesseY1 = 0
                        
                    if event.key == pygame.K_z:
                        self.vitesseY2 = 0

                    if event.key == pygame.K_s:
                        self.vitesseY2 = 0
                    
                        
                        
            self.Joueur1.mouvement(self.vitesseY1)
            self.Joueur2.rect.y = int(float(self.positionY))

            self.Joueur2.mouvement(self.vitesseY2)
            self.Joueur1.rect.clamp_ip(self.rect) # Permet au joueur de se déplacer uniquement dans l'espace prévu
            self.Joueur2.rect.clamp_ip(self.rect) # Permet au joueur de se déplacer uniquement dans l'espace prévu
            
            if self.ball_shot:
                self.ball.mouvement(self.ballVx, self.ballVy) 

            if self.Joueur2.rect.colliderect(self.ball.rect) or self.Joueur1.rect.colliderect(self.ball.rect):
                self.ballVx = self.ball_redirection(self.ballVx, 0)
                self.ballVy = self.ball_redirection(self.ballVy, 60)

            if self.ball.rect.top <= 0 or self.ball.rect.bottom >= 500:
                self.ballVy = self.ball_redirection(self.ballVx, 0)

            if self.ball.rect.right >= 901:
                self.ball.rect.x, self.ball.rect.y = 450, 250
                self.score1 += 1
                self.ball_shot = False
            
            if self.ball.rect.left <= 0:
                self.ball.rect.x, self.ball.rect.y = 450, 250
                self.score2 += 1
                self.ball_shot = False 

            self.ball.rect.clamp_ip(self.rect)  

            send_data = f" {self.Joueur1.rect.y}, {self.ball.rect.x}, {self.ball.rect.y}, {self.score1}, {self.score2} "

            if self.client is not None:
                self.client.send(send_data.encode('utf-8'))
            
            self.ecran.fill((50, 50, 50))

            self.information('good', f"Ping Pong", [330, 50, 20, 20], (255, 255, 255))
            self.information('good', f" { self.score1 } ", [180, 50, 20, 20], (255, 255, 255))
            self.information('good', f" { self.score2 } ", [670, 50, 20, 20], (255, 255, 255))

            if self.ball_shot is False:
                 self.information('good', f"Appuyez sur espace", [210, 120, 20, 20], (255, 255, 255))

            self.ball.affichage(self.ecran)
            self.Joueur1.affichage(self.ecran)
            self.Joueur2.affichage(self.ecran)

            pygame.display.flip()

    def threadC(self, cible):
        thread = threading.Thread(target=cible)
        thread.daemon = True
        thread.start()

    def ball_redirection(self, vitesse, angle):

        vitesse = - (vitesse * math.cos(angle))  
        return vitesse

    def receive(self):
        while True:
            self.positionY = self.client.recv(128).decode('utf-8')        

    def information(self, font, message, messager, color):

        if font == 'good':
            font = pygame.font.Font('/Users/Okan/Desktop/DevPython/04B_19__.TTF', 50)

        message = font.render(message, True, color)
        self.ecran.blit(message, messager)
        
    def connexion(self):
        self.client, self.adresse = self.server.accept()
        self.receive()

if __name__ == '__main__':
    
    pygame.init()
    Jeu().principal()
    pygame.quit()