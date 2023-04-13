import pygame
from mainMenu.menuButtons import MenuButtons
from mainMenu.controlMenu import ControlsMenu
class MainMenu:
    def checkIfButtonClicked(self, mousePos, buttons):
        mouse = pygame.Rect(mousePos[0], mousePos[1], 1, 1)
        for x in range(len(buttons)):
            if buttons[x].rect.contains(mouse):
                return x
        return -1

    def mainMenu(self, screen):
        controlsMenu = ControlsMenu()

        playButton = MenuButtons("PLAY")
        playButton.rect.x = 365 - int(playButton.image.get_width()/2)
        playButton.rect.y = 595

        controlsButton = MenuButtons("CONTROLS")
        controlsButton.rect.x = 365 - int(playButton.image.get_width()/2)
        controlsButton.rect.y = 715

        buttons = [playButton, controlsButton]

        running = True
        while running:
            if playButton.isClicked and pygame.time.get_ticks() - playButton.timeClicked >= 100:
                running = False

            if controlsButton.isClicked and pygame.time.get_ticks() - controlsButton.timeClicked >= 100:
                controlsButton.isClicked = False
                controlsMenu.controlsMenu(screen)

            screen.blit(pygame.image.load("Textures/MainMenu/MainMenu.png").convert(), (0,0))
            playButton.draw(screen)
            controlsButton.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttonClicked = self.checkIfButtonClicked(pygame.mouse.get_pos(), buttons)
                    if buttonClicked != -1:
                        buttons[buttonClicked].isClicked = True
                        buttons[buttonClicked].timeClicked = pygame.time.get_ticks()