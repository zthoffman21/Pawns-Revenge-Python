# Importing the libraries
import pygame
buttonTextures = {"PLAY":"Textures/MainMenu/PlayButton.png", "BACK":"Textures/MainMenu/BackButton.png", "CONTROLS":"Textures/MainMenu/ControlsButton.png"}
buttonClickedTextures = {"PLAY":"Textures/MainMenu/PlayButtonClicked.png", "BACK":"Textures/MainMenu/BackButtonClicked.png", "CONTROLS":"Textures/MainMenu/ControlsButtonClicked.png"}
class MenuButtons(pygame.sprite.Sprite):
    def __init__(self, type):
        #initializing the supersclass's constructors
        super().__init__()

        #initializing it characteristics
        self.itemType = type
        self.image = pygame.image.load(buttonTextures[self.itemType]).convert_alpha()
        self.isClicked = False
        self.timeClicked = -1000
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def draw(self, screen):
        if self.isClicked:
            self.image = pygame.image.load(buttonClickedTextures[self.itemType]).convert_alpha()
        else:
            self.image = pygame.image.load(buttonTextures[self.itemType]).convert_alpha()
        screen.blit(self.image, self.rect)    

    def checkIfButtonClicked(self, mousePos, buttons):
        mouse = pygame.Rect(mousePos[0], mousePos[1], 1, 1)
        for x in range(len(buttons)):
            if buttons[x].rect.contains(mouse):
                return x
        return -1