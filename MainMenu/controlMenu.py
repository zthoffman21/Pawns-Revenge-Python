import pygame
from MainMenu.menuButtons import MenuButtons
class ControlsMenu:
    def controlsMenu(self, screen):
        backButton = MenuButtons("BACK")
        backButton.rect.x = 365 - backButton.image.get_width()/2
        backButton.rect.y = 700

        screen.blit(pygame.image.load("Textures/MainMenu/ControlsMenu.png").convert(), (0,0))
        pygame.display.flip()

        running = True
        while running:

            if backButton.isClicked and (pygame.time.get_ticks() - backButton.timeClicked) >= 100:
                running = False

            backButton.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.checkIfButtonClicked(pygame.mouse.get_pos(), backButton):
                        backButton.isClicked = True
                        backButton.timeClicked = pygame.time.get_ticks()

    def checkIfButtonClicked(self, mousePos, backButton):
        mouse = pygame.Rect(mousePos[0], mousePos[1], 1, 1)
        if backButton.rect.contains(mouse):
            return 1
        return 0