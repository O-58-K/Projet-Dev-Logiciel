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
        self.direct = True

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = '169.254.230.36', 80

        self.JoueurX1, self.JoueurY1 = 20, 250
        self.JoueurX2, self.JoueurY2 = 860, 250
        self.Joueur_size = [20, 80]
        self.vitesseY1, self.vitesseY2 = 0, 0

        self.Joueur1 = Joueur(self.JoueurX1, self.JoueurY1, self.Joueur_size)
        self.Joueur2 = Joueur(self.JoueurX2, self.JoueurY2, self.Joueur_size)

        self.rect = pygame.Rect(0, 0, 900, 500)
        self.score1, self.score2 = 0, 0

        self.ballX, self.ballY = None, None
        self.Joueur1Pos = 250
        self.recv_data = False        
        self.ball_direction = [-1, 1]
        self.ball = Ball(450, 250, [20, 20], random.choice(self.ball_direction))
        self.ball_shot = False
        self.ballVx, self.ballVy = 1, 1
      
    def principal(self):
        
        self.client.connect((self.ip, self.port))
        self.threadC(self.receive_data)
                
        while self.direct:

            clock.tick(400)
        
            for event in pygame.event.get():
                
                if event.type == pygame.quit:
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.vitesseY2 = -1

                    if event.key == pygame.K_s:
                        self.vitesseY2 = 1

                    if event.key == pygame.K_SPACE:
                        self.ball_shot = True
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        self.vitesseY2 = 0

                    if event.key == pygame.K_s:
                        self.vitesseY2 = 0

            if self.recv_data:

                self.ball.rect.x = self.ballX
                self.ball.rect.y = self.ballY
                self.Joueur1.rect.y = self.Joueur1Pos

                                                                   
            self.Joueur1.mouvement(self.vitesseY1)
            self.Joueur2.mouvement(self.vitesseY2)
            positionYJoueur2 = f" { self.Joueur2.rect.y }"

            self.client.send(positionYJoueur2.encode('utf-8'))

            self.Joueur1.rect.clamp_ip(self.rect) # Permet au joueur de se déplacer uniquement dans l'espace prévu
            self.Joueur2.rect.clamp_ip(self.rect) # Permet au joueur de se déplacer uniquement dans l'espace prévu

            self.recv_data = True
            self.ecran.fill((50, 50, 50))

            self.information('good', f"Ping Pong", [330, 50, 20, 20], (255, 255, 255))
            self.information('good', f" { self.score1 } ", [180, 50, 20, 20], (255, 255, 255))
            self.information('good', f" { self.score2 } ", [670, 50, 20, 20], (255, 255, 255))

            self.ball.affichage(self.ecran)
            self.Joueur1.affichage(self.ecran)
            self.Joueur2.affichage(self.ecran)

            pygame.display.flip()

    
    def receive_data(self):
        while True:
            data_receive = self.client.recv(128).decode('utf-8')
            data_receive = data_receive.split(', ')
            self.Joueur1Pos =  int(data_receive[0])   
            self.ballX = int(data_receive[1])
            self.ballY = int(data_receive[2])
            self.score1 = int(data_receive[3])
            self.score2 = int(data_receive[4])
            print(data_receive)        

    def information(self, font, message, messager, color):

        if font == 'good':
            font = pygame.font.Font('/Users/Okan/Desktop/DevPython/04B_19__.TTF', 50)

        message = font.render(message, True, color)
        self.ecran.blit(message, messager)        

    def ball_redirection(self, vitesse, angle):

        vitesse = - (vitesse * math.cos(angle))  
        return vitesse 
            
    def threadC(self, cible):
        thread = threading.Thread(target=cible)
        thread.daemon = True
        thread.start()

if __name__ == '__main__':
    
    pygame.init()
    Jeu().principal()
    pygame.quit()