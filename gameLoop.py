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

    def moveProjectiles(self, timePassed, allProjectiles, allEnimiesArr, allThrowableItemsArr, mapOfPieces):
            for projectile in allProjectiles:
                thisIttVel = projectile.velocity * timePassed/40

                movementX = thisIttVel * math.cos(projectile.launchAngle)
                movementY = thisIttVel * math.sin(projectile.launchAngle)

                collidesWithPiece = False

                for piece in allEnimiesArr:
                    if pygame.Rect.colliderect(piece.rect, projectile.rect):
                        collidesWithPiece = True
                        piece.getHit()
                        if piece.health <= 0:
                            self.pieceDeath(piece, allEnimiesArr, allThrowableItemsArr, mapOfPieces)
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

    def pieceDeath(self, piece, allEnimiesArr, allThrowableItemsArr, mapOfPieces):
        piece.isDead = True
        cords = (piece.findChessBoardCordX(), piece.findChessBoardCordY())
        if piece in allEnimiesArr:
            allEnimiesArr.remove(piece)
        mapOfPieces[cords[1]][cords[0]] = "-"
        piece.health -= 1
        allThrowableItemsArr.append(piece)

    def addEnemy(self, allChessPiecesArr, allEnimiesArr, movement, mapOfPieces):
        allChessPiecesArr.append(Enemy())
        allEnimiesArr.append(allChessPiecesArr[len(allChessPiecesArr)-1])

        cord = movement.findOpenSpot(mapOfPieces)
        cordPix = self.convertChessCordsToPixels(cord[0],cord[1])
        allChessPiecesArr[len(allChessPiecesArr)-1].rect.x = cordPix[0]
        allChessPiecesArr[len(allChessPiecesArr)-1].rect.y = cordPix[1]

        mapOfPieces[cord[1]][cord[0]] = "X"

    def pickupItem(self, allThrowableItemsArr, pawn, info):
        allThrowableItemsArr[info[1]].rect.x = pawn.rect.centerx - allThrowableItemsArr[info[1]].image.get_width()/2
        allThrowableItemsArr[info[1]].rect.y = pawn.rect.centery - allThrowableItemsArr[info[1]].image.get_height()/2


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
        startTime = 0
        endTime = 0
        currentTicks = 0
        lastTicks = 0
        ticksPassed = 0
        lastEnemyMove = 0
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
        allEnimiesArr = []
        allProjectiles = [] 

        #creating storage for all throwable items
        allThrowableItems = pygame.sprite.Group()
        allThrowableItemsArr = []

        #creating all the different item types
        itemTypes = ["A","B","C","D","E","F","G","H","1","2","3","4","5","6","7","8"]

        #creating all throwable items from a-h
        for index in range(8):
            item = Items(itemTypes[index])
            item.rect.x = index*85 + 97
            item.rect.y = 597
            allThrowableItems.add(item)
            allThrowableItemsArr.append(item)
        #creating all throwable items from 1-8
        for index in range(8,16):
            item = Items(itemTypes[index])
            item.rect.x = 27
            item.rect.y = 550 - 64*(index-8)
            allThrowableItems.add(item)
            allThrowableItemsArr.append(item)


        #temp pawn to test 
        pawn = Pawn()
        pawn.rect.x = boardInfo.convertChessCordsToPixels(4,4)[0]
        pawn.rect.y = boardInfo.convertChessCordsToPixels(4,4)[1]
        mapOfPieces[4][4] = "X"
        allChessPiecesArr.append(pawn)

        #temp piece
        dummy = Enemy()
        dummy.rect.x = boardInfo.convertChessCordsToPixels(0,0)[0]
        dummy.rect.y = boardInfo.convertChessCordsToPixels(0,0)[1]
        mapOfPieces[0][0] = "X"
        allChessPiecesArr.append(dummy)
        allEnimiesArr.append(dummy)

        #temp piece2
        dummy2 = Enemy()
        dummy2.rect.x = boardInfo.convertChessCordsToPixels(7,7)[0]
        dummy2.rect.y = boardInfo.convertChessCordsToPixels(7,7)[1]
        mapOfPieces[7][7] = "X"
        allChessPiecesArr.append(dummy2)
        allEnimiesArr.append(dummy2)

        running = True
        while running:
            #gets the ammount of ticks that pass since last frame
            currentTicks = pygame.time.get_ticks()
            ticksPassed = currentTicks-lastTicks
            lastTicks = currentTicks

            if pawn.enemyNear and currentTicks - pawn.enemyNearTimer >= 500 and not pawn.hasImmunity:
                pawn.getHit()
                pawn.hasImmunity = True
                pawn.immunityStart = pygame.time.get_ticks()
                if pawn.health <= 0:
                    game.pieceDeath(pawn, allEnimiesArr, allThrowableItemsArr, mapOfPieces)

            # initializing default screen
            screen.fill(darkBrown)
            pygame.draw.rect(screen, lightBrown, pygame.Rect(20, 95, 690, 548))
            screen.blit(pygame.image.load("Textures/ChessBoardSVS.png").convert_alpha(), (25,100))

            #drawing all the pieces
            allThrowableItems.draw(screen)
            for piece in allChessPiecesArr:
                if not hasItem or piece is not allThrowableItemsArr[info[1]]:
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
                game.moveProjectiles(ticksPassed, allProjectiles, allEnimiesArr, allThrowableItemsArr, mapOfPieces)
                    
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
                #game.addEnemy(allChessPiecesArr, allEnimiesArr, movement, mapOfPieces)

                lastEnemyMove = pygame.time.get_ticks()
                allEnimiesArr.sort(key=lambda x: movement.getDistFromPawn(pawn, x))

                for enemy in allEnimiesArr:
                    movement.moveEnemy(enemy, movement.findEnemyNextMove(pawn, enemy, mapOfPieces), mapOfPieces)

                allChessPiecesArr.sort(key=boardInfo.getYCord)
                
                if not pawn.enemyNear:
                    pawn.enemyNear = movement.checkIfEnemyIsNear((pawn.findChessBoardCordX(), pawn.findChessBoardCordY()), mapOfPieces)
                    if pawn.enemyNear:
                        pawn.enemyNearTimer = pygame.time.get_ticks()

            if pawn.hasImmunity and pygame.time.get_ticks() - pawn.immunityStart >= 2000:
                pawn.hasImmunity = False