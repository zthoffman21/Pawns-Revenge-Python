# Importing the libraries
import pygame
from SpriteFiles.items import Items
import math
from UsefulFunctions.movement import Movement
from SpriteFiles.powerBar import PowerBar
from SpriteFiles.ChessPieces.pawn import Pawn
from SpriteFiles.ChessPieces.enemy import Enemy
from UsefulFunctions.boardInfo import BoardInfo

class GameLoop():

    def throwItem(self, projectile, velocity, allProjectiles, pawn):
        allProjectiles.append(projectile)
        projectile.velocity = velocity * 0.05

        mouseCord = pygame.mouse.get_pos()
        diffX = mouseCord[0]-pawn.rect.centerx
        diffY = mouseCord[1]-pawn.rect.centery

        if diffX == 0:
            projectile.launchAngle = -3/2*math.pi
        else:
            projectile.launchAngle = math.atan(diffY/diffX)
        if diffX < 0:
            projectile.launchAngle += math.pi

    def moveProjectiles(self, timePassed, allProjectiles, allChessPiecesArr, allThrowableItemsArr, mapOfPieces, pawn):
            for projectile in allProjectiles:
                thisIttVel = projectile.velocity * timePassed/40

                movementX = thisIttVel * math.cos(projectile.launchAngle)
                movementY = thisIttVel * math.sin(projectile.launchAngle)

                collidesWithPiece = False

                for piece in allChessPiecesArr:
                    if piece is not pawn:
                        if pygame.Rect.colliderect(piece.rect, projectile.rect):
                            collidesWithPiece = True
                            piece.getHit()
                            if piece.health <= 0:
                                self.pieceDeath(piece, allChessPiecesArr, allThrowableItemsArr, mapOfPieces)
                            break                

                if projectile.rect.x + movementX + projectile.image.get_width() >= 705:
                    projectile.rect.x = 705 - projectile.image.get_width()
                    projectile.velocity = 0
                elif projectile.rect.x + movementX <= 25:
                    projectile.rect.x = 25
                    projectile.velocity = 0
                else:
                    projectile.rect.x += movementX

                if projectile.rect.y + movementY + projectile.image.get_height() >= 612:
                    projectile.rect.y = 612 - projectile.image.get_height()
                    projectile.velocity = 0
                elif projectile.rect.y + movementY <= 100:
                    projectile.rect.y = 100
                    projectile.velocity = 0
                else:
                    projectile.rect.y += movementY

                projectile.velocity -= 10*timePassed/100

                if collidesWithPiece:
                    projectile.velocity = 0

                if projectile.velocity <= 0:
                    allProjectiles.remove(projectile)

    def pieceDeath(self, piece, allChessPiecesArr, allThrowableItemsArr, mapOfPieces):
        piece.isDead = True
        cords = (piece.findChessBoardCordX(), piece.findChessBoardCordY())
        if piece in allChessPiecesArr:
            allChessPiecesArr.remove(piece)
        mapOfPieces[cords[1]][cords[0]] = "-"
        piece.health -= 1
        allThrowableItemsArr.append(piece)

    def addEnemy(self, allChessPiecesArr, movement, mapOfPieces, pawn, boardInfo, pieceType):
        allChessPiecesArr.append(Enemy(pieceType))

        cord = movement.findOpenSpot(mapOfPieces, pawn)
        cordPix = boardInfo.convertChessCordsToPixels(cord[0],cord[1])
        allChessPiecesArr[len(allChessPiecesArr)-1].rect.x = cordPix[0]
        allChessPiecesArr[len(allChessPiecesArr)-1].rect.y = cordPix[1]

        mapOfPieces[cord[1]][cord[0]] = "X"

    def pickupItem(self, allThrowableItemsArr, pawn, info):
        allThrowableItemsArr[info[1]].rect.x = pawn.rect.centerx - allThrowableItemsArr[info[1]].image.get_width()/2
        allThrowableItemsArr[info[1]].rect.y = pawn.rect.centery - allThrowableItemsArr[info[1]].image.get_height()/2

    def dicipherWaveCode(self, level, enimiesInLevel, timingOfLevel):
        pieces = {"N":"KNIGHT", "B":"BISHOP", "R":"ROOK", "Q":"QUEEN", "K":"KING"}
        index = 0

        while index < len(level):
            if level[index] in pieces:
                enimiesInLevel.append(pieces[level[index]])
            else:
                if index != 0:
                    enimiesInLevel.append("X")
                time = level[index]
                while (index+1) < len(level) and level[index+1] not in pieces:
                    time += level[index+1]
                    index += 1
                timingOfLevel.append(time)
            index += 1

    def game(self, screen):
        powerBar = PowerBar()
        game = GameLoop()
        boardInfo = BoardInfo()

        # initializing colors
        lightBrown = (166, 126, 61)
        darkBrown = (37, 24, 0)


        #variable initialization
        movement = Movement()
        hasItem = False
        isShooting = False
        canThrow = False
        timeOfDeath = -4000
        startTime = 0
        endTime = 0
        currentTicks = 0
        lastTicks = 0
        ticksPassed = 0
        lastEnemyMove = 0
        timeLastSpawned = 0
        waveLevel = 0
        allWaves = ["3N5BN", "3NNN"]
        mapOfPieces = [["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-","-","-"],]


        #creating storage for all chess pieces. Sprite group allows to print at once, while arr allows for itteration and minipulation
        allChessPiecesArr = []
        allProjectiles = [] 

        #creating storage for all throwable items
        allThrowableItemsArr = []

        #creating all the different item types
        itemTypes = ["A","B","C","D","E","F","G","H","1","2","3","4","5","6","7","8"]

        #creating all throwable items from a-h
        for index in range(8):
            item = Items(itemTypes[index])
            item.rect.x = index*85 + 97
            item.rect.y = 597
            allThrowableItemsArr.append(item)
        #creating all throwable items from 1-8
        for index in range(8,16):
            item = Items(itemTypes[index])
            item.rect.x = 27
            item.rect.y = 550 - 64*(index-8)
            allThrowableItemsArr.append(item)


        #user 
        pawn = Pawn()
        pawn.rect.x = boardInfo.convertChessCordsToPixels(4,4)[0]
        pawn.rect.y = boardInfo.convertChessCordsToPixels(4,4)[1]
        mapOfPieces[4][4] = "X"
        allChessPiecesArr.append(pawn)

        running = True
        while running:

            enimiesInLevel = []
            timingOfLevel = []
            game.dicipherWaveCode(allWaves[waveLevel], enimiesInLevel, timingOfLevel)

            while len(allChessPiecesArr) -1 > 0 or len(enimiesInLevel) > 0:

                if pawn.health <= 0:
                    if(pygame.time.get_ticks() - timeOfDeath) >= 3000:
                        print(pygame.time.get_ticks() - timeOfDeath)
                        running = False
                        break

                if len(timingOfLevel) > 0 and (pygame.time.get_ticks() - timeLastSpawned)/1000 >= int(timingOfLevel[0]):
                    while len(enimiesInLevel) > 0 and enimiesInLevel[0] != "X":
                        self.addEnemy(allChessPiecesArr, movement, mapOfPieces, pawn, boardInfo, enimiesInLevel[0])
                        del enimiesInLevel[0]
                    timeLastSpawned = pygame.time.get_ticks()
                    if len(enimiesInLevel) > 0:
                        del timingOfLevel[0]
                        del enimiesInLevel[0]

                if pawn.health != 2 and pygame.time.get_ticks() - pawn.timeHit >= 10000:
                    print("regen")
                    pawn.health += 1


                #gets the ammount of ticks that pass since last frame
                currentTicks = pygame.time.get_ticks()
                ticksPassed = currentTicks-lastTicks
                lastTicks = currentTicks

                if pawn.enemyNear and currentTicks - pawn.enemyNearTimer >= 500 and not pawn.hasImmunity:
                    pawn.getHit()
                    pawn.timeHit = pygame.time.get_ticks()
                    pawn.hasImmunity = True
                    pawn.immunityStart = pygame.time.get_ticks()
                    if pawn.health == 0:
                        game.pieceDeath(pawn, allChessPiecesArr, allThrowableItemsArr, mapOfPieces)
                        hasItem = False
                        canThrow = False
                        isShooting = False
                        timeOfDeath = pygame.time.get_ticks()

                # initializing default screen
                screen.fill(darkBrown)
                pygame.draw.rect(screen, lightBrown, pygame.Rect(20, 95, 690, 548))
                screen.blit(pygame.image.load("Textures/ChessBoardSVS.png").convert_alpha(), (25,100))

                #drawing all the pieces
                for item in allThrowableItemsArr:
                    if not hasItem or item is not allThrowableItemsArr[info[1]]:
                        item.draw(screen, False)

                for piece in allChessPiecesArr:
                        piece.draw(screen, False)
                if hasItem:
                    allThrowableItemsArr[info[1]].draw(screen, hasItem)

                if isShooting:
                    powerBar.rect.x = pawn.rect.x + pawn.image.get_width() + 5 
                    powerBar.rect.y = pawn.rect.y
                    powerBar.draw(screen, pygame.time.get_ticks() - startTime)

                #update display
                pygame.display.flip()

                if len(allProjectiles) > 0:
                    game.moveProjectiles(ticksPassed, allProjectiles, allChessPiecesArr, allThrowableItemsArr, mapOfPieces, pawn)
                        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False


                    if event.type == pygame.KEYDOWN and pawn.health > 0:
                        #checks for movement input
                        if event.key in [pygame.K_RIGHT, pygame.K_d] and movement.canMoveRight(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'R', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.x += 85
                            pawn.rect.x += 85
                        elif event.key in [pygame.K_LEFT, pygame.K_a] and movement.canMoveLeft(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'L', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.x -= 85
                            pawn.rect.x -= 85
                        elif event.key in [pygame.K_UP, pygame.K_w] and movement.canMoveUp(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'U', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.y -= 64
                            pawn.rect.y -= 64
                        elif event.key in [pygame.K_DOWN, pygame.K_s] and movement.canMoveDown(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'D', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.y += 64
                            pawn.rect.y += 64

                        pawn.enemyNear = movement.checkIfEnemyIsNear((pawn.findChessBoardCordX(),pawn.findChessBoardCordY()), mapOfPieces)
                        if pawn.enemyNear:
                            pawn.enemyNearTimer = pygame.time.get_ticks()

                        #sorts the pieces by ycord so they get displayed from back to front
                        allChessPiecesArr.sort(key=boardInfo.getYCord)


                    if event.type == pygame.MOUSEBUTTONDOWN and pawn.health > 0:
                        #checks if the mouse if clicked and has an item(trying to shoot the item)
                        if canThrow:
                            #if the player has an item and is not building velocity, this starts building it
                            if not isShooting:
                                startTime = pygame.time.get_ticks()
                                isShooting = True
                        #if the player clicks the mouse but does not have an item, it checks if they 
                        #can pickup an item, if so, it picks up that item
                        else:
                            info = boardInfo.getItemPickupInfo(pawn, allThrowableItemsArr)
                            if info[0]:
                                game.pickupItem(allThrowableItemsArr, pawn, info)
                                hasItem = True
                        #if the mouse is not clicked and the player is shooting, it shoots the item
                    elif not pygame.mouse.get_pressed()[0]:
                        if hasItem:
                            canThrow = True

                        if isShooting:
                            endTime = pygame.time.get_ticks()
                            if endTime-startTime >= 800:
                                game.throwItem(allThrowableItemsArr[info[1]], 800, allProjectiles, pawn)
                            else:
                                game.throwItem(allThrowableItemsArr[info[1]], endTime-startTime, allProjectiles, pawn)
                            isShooting = False
                            hasItem = False
                            canThrow = False
                
                if pygame.time.get_ticks() - lastEnemyMove >= 1000 and pawn.health > 0:
                    #game.addEnemy(allChessPiecesArr, allEnimiesArr, movement, mapOfPieces, pawn, boardInfo)

                    lastEnemyMove = pygame.time.get_ticks()
                    allChessPiecesArr.sort(key=lambda x: movement.getDistFromPawn(pawn, x))

                    for enemy in allChessPiecesArr:
                        if enemy is not pawn:
                            movement.moveEnemy(enemy, movement.findEnemyNextMove(pawn, enemy, mapOfPieces), mapOfPieces)

                    allChessPiecesArr.sort(key=boardInfo.getYCord)
                    
                    if not pawn.enemyNear:
                        pawn.enemyNear = movement.checkIfEnemyIsNear((pawn.findChessBoardCordX(), pawn.findChessBoardCordY()), mapOfPieces)
                        if pawn.enemyNear:
                            pawn.enemyNearTimer = pygame.time.get_ticks()

                if pawn.hasImmunity and pygame.time.get_ticks() - pawn.immunityStart >= 2000:
                    pawn.hasImmunity = False
            waveLevel += 1
            print("wave complete")

            #checks if the item the user is holding as the wave ends is an enemy
            if hasItem and isinstance(allThrowableItemsArr[info[1]], Enemy):
                hasItem = False
                canThrow = False
                isShooting = False

            while len(allThrowableItemsArr) > 16:
                del allThrowableItemsArr[16]

