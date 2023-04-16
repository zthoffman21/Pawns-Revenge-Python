# Importing the libraries
import pygame
from SpriteFiles.items import Items
import math
from UsefulFunctions.movement import Movement
from SpriteFiles.powerBar import PowerBar
from SpriteFiles.ChessPieces.pawn import Pawn
from SpriteFiles.ChessPieces.enemy import Enemy
from UsefulFunctions.boardInfo import BoardInfo
from gameLoop.hearts import Hearts
from gameLoop.roundNumber import RoundNumber
import random

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

    def drawEverything(self, screen, pawn, hearts, roundNumber, waveLevel, allThrowableItemsArr, hasItem, info, allChessPiecesArr, isShooting, powerBar, shootingStartTime, boardInfo):     
        #sorts the pieces by ycord so they get displayed from back to front
        allChessPiecesArr.sort(key=boardInfo.getYCord)

        # initializing colors
        lightBrown = (166, 126, 61)
        darkBrown = (37, 24, 0)

        #draw background and board to screen
        screen.fill(darkBrown)
        pygame.draw.rect(screen, lightBrown, pygame.Rect(20, 95, 690, 548))
        screen.blit(pygame.image.load("Textures/ChessBoardSVS.png").convert_alpha(), (25,100))

        #draw gameloop ui to screen
        hearts.draw(screen, pawn.health)
        roundNumber.draw(screen, waveLevel+1)

        #drawing throwable items to screen except the one the player is holding
        for item in allThrowableItemsArr:
            if not hasItem or item is not allThrowableItemsArr[info[1]]:
                item.draw(screen, False)
        #drawing all pieces to screen (enemies and user)
        for piece in allChessPiecesArr:
                piece.draw(screen, False)
        #if the player has an item, draws it onto the screen 
        if hasItem:
            allThrowableItemsArr[info[1]].draw(screen, hasItem)
        #if the player is shooting, draws the powerbar onto the screen
        if isShooting:
            powerBar.rect.x = pawn.rect.x + pawn.image.get_width() + 5 
            powerBar.rect.y = pawn.rect.y
            powerBar.draw(screen, pygame.time.get_ticks() - shootingStartTime)

        #update display
        pygame.display.flip()

    def createWaveCode(self, waveNum):
        enemies = ["N" for x in range(30)] + ["B" for x in range(30)] + ["R" for x in range(25)] + ["Q" for x in range(10)] + ["K" for x in range(5)]
        wave = []

        for x in range(int(1/75 * ((waveNum-10)**3 - waveNum**2) + 17.5)):
            wave.append(enemies[random.randint(0,99)])

        index = 0
        l = len(wave)
        while index < l:
            enemiesAtOnce = random.randint(1,4)
            while index + enemiesAtOnce >= len(wave):
                enemiesAtOnce = random.randint(1,4)
            time = enemiesAtOnce**2 + 5
            wave.insert(index+enemiesAtOnce, str(time))
            index += enemiesAtOnce + 1
        wave.insert(0, "5")
        return "".join(wave)

    def game(self, screen):
        powerBar = PowerBar()
        game = GameLoop()
        boardInfo = BoardInfo()
        hearts = Hearts()
        roundNumber = RoundNumber()

        #variable initialization
        movement = Movement()
        hasItem = False
        isShooting = False
        canThrow = False
        timeOfDeath = -4000
        shootingStartTime = 0
        shootingEndTime = 0
        currentTicks = 0
        lastTicks = 0
        lastEnemyMove = 0
        timeLastSpawned = 0
        waveLevel = 0
        info = []
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

            #creates the wave code and timing of the wave for this wave
            enimiesInLevel = []
            timingOfLevel = []
            waveCode = self.createWaveCode(waveLevel)
            game.dicipherWaveCode(waveCode, enimiesInLevel, timingOfLevel)
            print(waveCode)

            #ends the wave when either more enemies are to come, or there are still enemies in the wave that have not been killed
            while len(allChessPiecesArr) -1 > 0 or len(enimiesInLevel) > 0:

                #ends the game loop if 3 seconds have past since the pawn has died
                if pawn.health <= 0:
                    if(pygame.time.get_ticks() - timeOfDeath) >= 3000:
                        running = False
                        break

                #checks if it is time to spawn more enemies based on the time code of the wave
                if len(timingOfLevel) > 0 and (pygame.time.get_ticks() - timeLastSpawned)/1000 >= int(timingOfLevel[0]):
                    #spawns new enemies until it sees an "X" in the wave code
                    while len(enimiesInLevel) > 0 and enimiesInLevel[0] != "X":
                        self.addEnemy(allChessPiecesArr, movement, mapOfPieces, pawn, boardInfo, enimiesInLevel[0])
                        del enimiesInLevel[0]
                    #prepares for next spawning
                    timeLastSpawned = pygame.time.get_ticks()
                    if len(enimiesInLevel) > 0:
                        del timingOfLevel[0]
                        del enimiesInLevel[0]

                #checks if the pawn can regen health
                if pawn.health != 2 and pygame.time.get_ticks() - pawn.timeHit >= 10000:
                    pawn.health += 1

                #checks if the pawn has lost immunity
                if pawn.hasImmunity and pygame.time.get_ticks() - pawn.immunityStart >= 2000:
                    pawn.hasImmunity = False

                #checks if the pawn has been next to an enemy for a half second. If so, the pawn takes damage
                if pawn.enemyNear and pygame.time.get_ticks() - pawn.enemyNearTimer >= 500 and not pawn.hasImmunity:
                    pawn.getHit()
                    pawn.timeHit = pygame.time.get_ticks()

                    #starts the pawn's immunity
                    pawn.hasImmunity = True
                    pawn.immunityStart = pygame.time.get_ticks()

                    #checks if this hit has caused the pawn to die
                    if pawn.health == 0:
                        game.pieceDeath(pawn, allChessPiecesArr, allThrowableItemsArr, mapOfPieces)
                        hasItem = False
                        canThrow = False
                        isShooting = False
                        timeOfDeath = pygame.time.get_ticks()

                #draw everything to the screen
                self.drawEverything(screen, pawn, hearts, roundNumber, waveLevel, allThrowableItemsArr, hasItem, info, allChessPiecesArr, isShooting, powerBar, shootingStartTime, boardInfo)

                #moves all projectiles based on the amount of ticks that has passes since last frame
                currentTicks = pygame.time.get_ticks()
                if len(allProjectiles) > 0:
                    game.moveProjectiles(currentTicks-lastTicks, allProjectiles, allChessPiecesArr, allThrowableItemsArr, mapOfPieces, pawn)
                lastTicks = currentTicks
                        
                #checks for events from the player
                for event in pygame.event.get():

                    #checks if the player hits the "x" button
                    if event.type == pygame.QUIT:
                        running = False

                    #checks if the player wants to move the pawn while their health is greater than 0. Also, it moves the item if the player is holding one and updates the map of pieces
                    if event.type == pygame.KEYDOWN and pawn.health > 0:

                        #move right
                        if event.key in [pygame.K_RIGHT, pygame.K_d] and movement.canMoveRight(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'R', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.x += 85
                            pawn.rect.x += 85
                        #move left
                        elif event.key in [pygame.K_LEFT, pygame.K_a] and movement.canMoveLeft(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'L', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.x -= 85
                            pawn.rect.x -= 85
                        #move up
                        elif event.key in [pygame.K_UP, pygame.K_w] and movement.canMoveUp(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'U', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.y -= 64
                            pawn.rect.y -= 64
                        #move down
                        elif event.key in [pygame.K_DOWN, pygame.K_s] and movement.canMoveDown(pawn, mapOfPieces):
                            boardInfo.updateMap(pawn,'D', mapOfPieces)
                            if hasItem:
                                allThrowableItemsArr[info[1]].rect.y += 64
                            pawn.rect.y += 64

                        #checks if there is an enemy near after the player has moved. If so, starts the timer until the player takes damage
                        pawn.enemyNear = movement.checkIfEnemyIsNear((pawn.findChessBoardCordX(),pawn.findChessBoardCordY()), mapOfPieces)
                        if pawn.enemyNear:
                            pawn.enemyNearTimer = pygame.time.get_ticks()



                    if event.type == pygame.MOUSEBUTTONDOWN and pawn.health > 0:

                        #checks if the mouse if clicked and has an item(trying to shoot the item)
                        if canThrow:
                            #if the player has an item and is not building velocity, this starts building it
                            if not isShooting:
                                shootingStartTime = pygame.time.get_ticks()
                                isShooting = True

                        #if the player clicks the mouse but does not have an item, it checks if they 
                        #can pickup an item, if so, it picks up that item
                        else:
                            info = boardInfo.getItemPickupInfo(pawn, allThrowableItemsArr)
                            if info[0]:
                                game.pickupItem(allThrowableItemsArr, pawn, info)
                                hasItem = True


                    elif not pygame.mouse.get_pressed()[0]:
                        
                        #if the player has an item and is not pressing the mouse, the player can now throw
                        if hasItem:
                            canThrow = True

                        #if the player is shooting and not is not pressing the mouse, it throws the item the player was holding
                        if isShooting:
                            shootingEndTime = pygame.time.get_ticks()
                            if shootingEndTime-shootingStartTime >= 800:
                                game.throwItem(allThrowableItemsArr[info[1]], 800, allProjectiles, pawn)
                            else:
                                game.throwItem(allThrowableItemsArr[info[1]], shootingEndTime-shootingStartTime, allProjectiles, pawn)
                            isShooting = False
                            hasItem = False
                            canThrow = False
                
                #checks if the it is time for the enemies to move again
                if pygame.time.get_ticks() - lastEnemyMove >= 1000 and pawn.health > 0:
                    lastEnemyMove = pygame.time.get_ticks()

                    #sorts the enemies from closest to user to the furthest so the front enemies do not block the back ones from moving
                    allChessPiecesArr.sort(key=lambda x: movement.getDistFromPawn(pawn, x))

                    #moving all enemies
                    for enemy in allChessPiecesArr:
                        if enemy is not pawn:
                            movement.moveEnemy(enemy, movement.findEnemyNextMove(pawn, enemy, mapOfPieces), mapOfPieces)
                    
                    #checks if an enemies has moved into attacking distance
                    if not pawn.enemyNear:
                        pawn.enemyNear = movement.checkIfEnemyIsNear((pawn.findChessBoardCordX(), pawn.findChessBoardCordY()), mapOfPieces)
                        if pawn.enemyNear:
                            pawn.enemyNearTimer = pygame.time.get_ticks()


            waveLevel += 1
            print("wave complete")

            #checks if the item the user is holding as the wave ends is an enemy
            if hasItem and isinstance(allThrowableItemsArr[info[1]], Enemy):
                hasItem = False
                canThrow = False
                isShooting = False

            #deletes all of this rounds corpses
            while len(allThrowableItemsArr) > 16:
                del allThrowableItemsArr[16]