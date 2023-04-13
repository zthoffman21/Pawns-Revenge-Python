from SpriteFiles.ChessPieces.chessPiece import ChessPiece
import pygame
import random
pieces = ["KNIGHT", "BISHOP", "ROOK", "QUEEN", "KING"]
pieceHealth = {"KNIGHT":2, "BISHOP":2, "ROOK":3, "QUEEN":4, "KING":5}
pieceTextures = {"KNIGHT":"Textures/Pieces/Knight.png", "BISHOP":"Textures/Pieces/Bishop.png", "ROOK":"Textures/Pieces/Rook.png", "QUEEN":"Textures/Pieces/Queen.png", "KING":"Textures/Pieces/King.png"}
pieceHitTextures = {"KNIGHT":"Textures/Pieces/KnightHit.png", "BISHOP":"Textures/Pieces/BishopHit.png", "ROOK":"Textures/Pieces/RookHit.png", "QUEEN":"Textures/Pieces/QueenHit.png", "KING":"Textures/Pieces/KingHit.png"}
pieceDeadTextures = {"KNIGHT":"Textures/Pieces/KnightDead.png", "BISHOP":"Textures/Pieces/BishopDead.png", "ROOK":"Textures/Pieces/RookDead.png", "QUEEN":"Textures/Pieces/QueenDead.png", "KING":"Textures/Pieces/KingDead.png"}
class Enemy(ChessPiece):
    def __init__(self, enemyType):
        #initializing the supersclass's constructors
        super().__init__()

        #initializing attributes of the piece
        self.pieceType = enemyType
        self.health = pieceHealth[self.pieceType]
        self.tickWhenHit = 0
        self.isDead = False
        self.velocity = 0
        self.launchAngle = 0

        #gives the sprite the texture of the chess piece
        self.image = pygame.image.load(pieceTextures[self.pieceType]).convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def getImage(self, isHit):
        if isHit:
            return pygame.image.load(pieceHitTextures[self.pieceType]).convert_alpha()
        return pygame.image.load(pieceTextures[self.pieceType]).convert_alpha()
    
    def draw(self, screen, hasItem):
        if self.isDead:
            self.image = pygame.image.load(pieceDeadTextures[self.pieceType]).convert_alpha()
            if hasItem: 
                self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.75), int(self.image.get_size()[1]*0.75)))
        elif self.isHit and pygame.time.get_ticks() - self.tickWhenHit <= 500:
            self.image = pygame.image.load(pieceHitTextures[self.pieceType]).convert_alpha()
        else:
            self.isHit = False
            self.image = pygame.image.load(pieceTextures[self.pieceType]).convert_alpha()
        screen.blit(self.image, self.rect)    
