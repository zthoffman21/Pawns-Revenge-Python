# Importing the libraries
import pygame
from gameLoop import GameLoop

# Initializing Pygame
pygame.init()


# Initializing surface
size = 730, 880
width, height = size
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pawn's Revenge")
game = GameLoop()

game.game(screen)