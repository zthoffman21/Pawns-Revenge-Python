# Importing the libraries
import pygame
class ChessPiece(pygame.sprite.Sprite):
    def __init__(self):
        #initializing the supersclass's constructors
        super().__init__()

        self.isHit = False
        self.tickWhenHit = 0
        self.isDead = False
    
    def findChessBoardCordX(self):
        return int((self.rect.x - 30) / 85)

    def findChessBoardCordY(self):
        return int((self.rect.y - 84) / 64)
    
    def getHit(self):
        self.health -= 1
        self.tickWhenHit = pygame.time.get_ticks()
        self.isHit = True
