import pygame
class RoundNumber:
    def __init__(self):
        pass

    def draw(self, screen, roundNum):
        lightBrown = (166, 126, 61)
        font = pygame.font.Font("Textures/GameLoopUI/RoundFont.ttf", 50)
        roundImage = font.render(str(roundNum), True, lightBrown)
        screen.blit(roundImage, (710 - roundImage.get_width(), 100-roundImage.get_height()))