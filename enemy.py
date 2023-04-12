from SpriteFiles.ChessPieces.chessPiece import ChessPiece
import pygame
import random
pieces = ["KNIGHT", "BISHOP", "ROOK", "QUEEN", "KING"]
pieceHealth = {"KNIGHT":2, "BISHOP":2, "ROOK":3, "QUEEN":4, "KING":5}
pieceWeight = ["KNIGHT" for x in range(30)] + ["BISHOP" for x in range(30)] + ["ROOK" for x in range(20)] + ["QUEEN" for x in range(10)] + ["KING" for x in range(10)]
pieceTextures = {"KNIGHT":"Textures/Knight.png", "BISHOP":"Textures/Bishop.png", "ROOK":"Textures/Rook.png", "QUEEN":"Textures/Queen.png", "KING":"Textures/King.png"}
pieceHitTextures = {"KNIGHT":"Textures/KnightHit.png", "BISHOP":"Textures/BishopHit.png", "ROOK":"Textures/RookHit.png", "QUEEN":"Textures/QueenHit.png", "KING":"Textures/KingHit.png"}
pieceDeadTextures = {"KNIGHT":"Textures/KnightDead.png", "BISHOP":"Textures/BishopDead.png", "ROOK":"Textures/RookDead.png", "QUEEN":"Textures/QueenDead.png", "KING":"Textures/KingDead.png"}
class Enemy(ChessPiece):
    def __init__(self):
        #initializing the supersclass's constructors
        super().__init__()

        #initializing attributes of the piece
        self.pieceType = self.createPieceType()
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
    
    def createPieceType(self):
        randPiece = random.randint(0,len(pieceWeight)-1)       
        return pieceWeight[randPiece]
    
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
