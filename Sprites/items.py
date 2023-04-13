# Importing the libraries
import pygame
itemTextures = {"A":"Textures/Items/A.png", "B":"Textures/Items/B.png", "C":"Textures/Items/C.png", "D":"Textures/Items/D.png", "E":"Textures/Items/E.png", 
                "F":"Textures/Items/F.png", "G":"Textures/Items/G.png", "H":"Textures/Items/H.png", "1":"Textures/Items/1.png", "2":"Textures/Items/2.png", 
                "3":"Textures/Items/3.png", "4":"Textures/Items/4.png", "5":"Textures/Items/5.png", "6":"Textures/Items/6.png", "7":"Textures/Items/7.png", 
                "8":"Textures/Items/8.png"}

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