# Importing the libraries
import pygame
from GameLoop.gameLoop import GameLoop
from MainMenu.mainMenu import MainMenu

# Initializing Pygame
pygame.init()


# Initializing surface
size = 730, 880
width, height = size
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pawn's Revenge")
pygame_icon = pygame.image.load("Textures/Pieces/Pawn.png")
pygame.display.set_icon(pygame_icon)
game = GameLoop()
mainMenu = MainMenu()

mainMenu.mainMenu(screen)
game.game(screen)
print("end")