# Importing the libraries
import pygame
itemTextures = {"A":"Textures/A.png", "B":"Textures/B.png", "C":"Textures/C.png", "D":"Textures/D.png", "E":"Textures/E.png", "F":"Textures/F.png", "G":"Textures/G.png",
                "H":"Textures/H.png", "1":"Textures/1.png", "2":"Textures/2.png", "3":"Textures/3.png", "4":"Textures/4.png", "5":"Textures/5.png", "6":"Textures/6.png", 
                "7":"Textures/7.png", "8":"Textures/8.png"}

class Items(pygame.sprite.Sprite):
    def __init__(self, type):
        #initializing the supersclass's constructors
        super().__init__()

        #initializing it characteristics
        self.itemType = type
        self.velocity = 0
        self.launchAngle = 0
        self.image = pygame.image.load(itemTextures[self.itemType]).convert_alpha()
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def draw(self, screen, hasItem):
        screen.blit(self.image, self.rect)    