from SpriteFiles.ChessPieces.chessPiece import ChessPiece
import pygame
pawnTexture = "Textures/Pieces/Pawn.png"
pawnHitTexture = "Textures/Pieces/PawnHit.png"
pawnDead = "Textures/Pieces/PawnDead.png"
class Pawn(ChessPiece):
    def __init__(self):
        #initializing the supersclass's constructors
        super().__init__()

        #initializing the pawn's attributes
        self.pieceType = "PAWN"
        self.health = 2  
        self.timeHit = 0
        self.enemyNear = 0
        self.enemyNearTimer = 0
        self.hasImmunity = False
        self.immunityStart = 0

        #gives the sprite the texture of the chess piece
        self.image = pygame.image.load(pawnTexture).convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def draw(self, screen, hasItem):
        if self.isDead:
            self.image = pygame.image.load(pawnDead).convert_alpha()
        elif self.isHit and pygame.time.get_ticks() - self.tickWhenHit <= 500:
            self.image = pygame.image.load(pawnHitTexture).convert_alpha()
        else:
            self.isHit = False
            self.image = pygame.image.load(pawnTexture).convert_alpha()
        screen.blit(self.image, self.rect)    