import pygame
heartTextures = {0:"Textures/GameLoopUI/Hearts/0Heart.png", 1:"Textures/GameLoopUI/Hearts/1Heart.png", 2:"Textures/GameLoopUI/Hearts/2Heart.png"}
class Hearts:
    def __init__(self):
        self.image = pygame.image.load(heartTextures[2]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 10

    def draw(self, screen, pawnHealth):
        if pawnHealth == 2:
            self.image = pygame.image.load(heartTextures[2]).convert_alpha()
        elif pawnHealth == 1:
            self.image = pygame.image.load(heartTextures[1]).convert_alpha()
        else:
            self.image = pygame.image.load(heartTextures[0]).convert_alpha()
        screen.blit(self.image, self.rect)    