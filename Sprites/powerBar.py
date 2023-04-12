import pygame
powerBarTexture = "Textures/PowerBar/1.png"
class PowerBar(pygame.sprite.Sprite):
    def __init__(self):
        #initializing the supersclass's constructors
        super().__init__()
        #initializing some basic attributes
        self.image = pygame.image.load(powerBarTexture).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def getTexture(self, power):
        powerTexture = 0
        #if the power is greater than 800 the bar is full so it is texture 16
        if power >= 800:
            powerTexture = 16
        else:
            powerTexture = int(power/50)
        return powerBarTexture[:18] + str(powerTexture) + powerBarTexture[19:]
    
    def draw(self, screen, power):
        #sets the image to whatever level power the bar is and draws it to the screen
        self.image = pygame.image.load(self.getTexture(power)).convert_alpha()
        screen.blit(self.image, self.rect)    