import pygame
import math
import random
class Movement:
    def findEnemyNextMove(self, pawn, enemy, mapOfPieces):
        
        currX = enemy.findChessBoardCordX()
        currY = enemy.findChessBoardCordY()
        pawnCord = (pawn.findChessBoardCordX(), pawn.findChessBoardCordY())

        currDistance = math.dist((currX, currY), pawnCord)
        distanceMoveLeft = math.dist((currX-1, currY), pawnCord)
        distanceMoveRight = math.dist((currX+1, currY), pawnCord)
        distanceMoveUp = math.dist((currX, currY-1), pawnCord)
        distanceMoveDown = math.dist((currX,currY+1), pawnCord)

        allPossMovesResults = [distanceMoveLeft-currDistance, distanceMoveRight-currDistance, distanceMoveUp-currDistance, distanceMoveDown-currDistance, currDistance-currDistance]
        resultKey = ['L','R','U','D','N']
        while(len(resultKey) > 1):
            bestMove = min(allPossMovesResults)
            ans = resultKey[allPossMovesResults.index(bestMove)]
            if ans == 'L' and self.canMoveLeft(enemy, mapOfPieces):
                return ans
            elif ans == 'R' and self.canMoveRight(enemy, mapOfPieces):
                return ans
            elif ans == 'U' and self.canMoveUp(enemy, mapOfPieces):
                return ans
            elif ans == 'D' and self.canMoveDown(enemy, mapOfPieces):
                return ans
            elif ans == 'N':
                return ans
            else:
                resultKey.remove(ans)
                allPossMovesResults.remove(bestMove)

    def moveEnemy(self, enemy, direction, mapOfPieces):
        currX = enemy.findChessBoardCordX()
        currY = enemy.findChessBoardCordY()
        if direction == 'L':
            enemy.rect.x -= 85
            mapOfPieces[currY][currX-1] = "X"
            mapOfPieces[currY][currX] = "-"
        if direction == 'R':
            enemy.rect.x += 85
            mapOfPieces[currY][currX+1] = "X"
            mapOfPieces[currY][currX] = "-"
        if direction == 'U':
            enemy.rect.y -= 64
            mapOfPieces[currY-1][currX] = "X"
            mapOfPieces[currY][currX] = "-"
        if direction == 'D':
            enemy.rect.y += 64
            mapOfPieces[currY+1][currX] = "X"
            mapOfPieces[currY][currX] = "-"

    def getDistFromPawn(self, enemy, pawn):
        return math.dist((enemy.findChessBoardCordX(), enemy.findChessBoardCordY()), (pawn.findChessBoardCordX(), pawn.findChessBoardCordY()))

    def canMoveRight(self, pieceWantingToMove, mapOfPieces):
        if pieceWantingToMove.findChessBoardCordX() == 7 or mapOfPieces[pieceWantingToMove.findChessBoardCordY()][pieceWantingToMove.findChessBoardCordX() + 1] == "X":
            return False
        return True

    def canMoveLeft(self, pieceWantingToMove, mapOfPieces):
        if pieceWantingToMove.findChessBoardCordX() == 0 or mapOfPieces[pieceWantingToMove.findChessBoardCordY()][pieceWantingToMove.findChessBoardCordX() - 1] == "X":
            return False
        return True

    def canMoveUp(self, pieceWantingToMove, mapOfPieces):
        if pieceWantingToMove.findChessBoardCordY() == 0 or mapOfPieces[pieceWantingToMove.findChessBoardCordY() - 1][pieceWantingToMove.findChessBoardCordX()] == "X":
            return False
        return True

    def canMoveDown(self, pieceWantingToMove, mapOfPieces):
        if pieceWantingToMove.findChessBoardCordY() == 7 or mapOfPieces[pieceWantingToMove.findChessBoardCordY() + 1][pieceWantingToMove.findChessBoardCordX()] == "X":
            return False
        return True
    
    def checkIfEnemyIsNear(self, currPos, mapOfPieces):
        currX = currPos[0]
        currY = currPos[1]
        around = [mapOfPieces[currY][currX+1], mapOfPieces[currY][currX-1], mapOfPieces[currY+1][currX], mapOfPieces[currY-1][currX]]
        if "X" in around:
            return True
        return False
    
    def findOpenSpot(self, mapOfPieces, pawn):
        randX = random.randint(0,7)
        randY = random.randint(0,7)
        pawnPoss = (pawn.findChessBoardCordX(), pawn.findChessBoardCordY())

        while(mapOfPieces[randY][randX] == "X" or math.dist((randX, randY), (pawnPoss[0], pawnPoss[1])) < 3):
            randX = random.randint(0,7)
            randY = random.randint(0,7)
        return (randX, randY)