import math
class BoardInfo:
    
    def getItemPickupInfo(self, pawn, allThrowableItemsArr):
        for x in range(len(allThrowableItemsArr)):
            if math.dist(pawn.rect.center,allThrowableItemsArr[x].rect.center) <= 55:
                return (1,x)
        return (0,-1)
    
    def getYCord(self, piece):
        if piece.health <= 0:
            return -1
        else:
            return piece.rect.y
            
    def convertChessCordsToPixels(self, cordX, cordY):
        chessBoardX = cordX * 85 + 30
        chessBoardY = cordY * 64 + 84
        return (chessBoardX, chessBoardY)

    def updateMap(self, piece, direction, mapOfPieces):
        chessX = piece.findChessBoardCordX()
        chessY = piece.findChessBoardCordY()
        mapOfPieces[chessY][chessX] = "-"

        if direction == 'R':
            mapOfPieces[chessY][chessX + 1] = "X"
        elif direction == 'L':
            mapOfPieces[chessY][chessX - 1] = "X"
        elif direction == 'U':
            mapOfPieces[chessY - 1][chessX] = "X"
        else:
            mapOfPieces[chessY + 1][chessX] = "X"
