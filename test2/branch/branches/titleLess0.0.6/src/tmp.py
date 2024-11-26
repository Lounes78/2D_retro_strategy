#!/usr/bin/env python

import os, sys

try:
    import random
except ImportError:
    print "Error: random module not found. Verify your python instalation."
    sys.exit(1)

try:
    import pygame
except ImportError:
    print "Error: pygame module not installed. Install pygame module."
    sys.exit(1)

try:
    from pygame.locals import *
except ImportError:
    print "Error: pygame.locals not found. Verify your pygame instalation."
    sys.exit(1)

if os.path.isdir(sys.path[0]):
    os.chdir(sys.path[0])
sys.path.append("src")

from mediaManager import *
from windowManager import *
from dungeonManager import *
from spriteManager import *

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
media = loadMedia()
windowManager = windowManager(pantalla)
background = media.loadImage(os.path.join('data', 'images', 'background', 'introBG.png'))
logo = []
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessOne.png')))
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessTwo.png')))
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessThree.png')))
characterInto = []
characterInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoOne.png')))
characterInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackotwo.png')))
characterInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoThree.png')))
font = pygame.font.SysFont("Courier New", 15)
font = font.render("Press Enter to continue or Esc to Exit.", 1, (255, 255, 255))
dummyCounter = 0
spriteCounter = 0
sound = media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_no_survivors_.mid'))
sound.music.play(-1)
centeredLogoX = windowManager.centerItemX(logo[spriteCounter])
centeredLogoY = windowManager.centerItemY(logo[spriteCounter])
centeredCharacterX = windowManager.centerItemX(characterInto[spriteCounter]) + logo[spriteCounter].get_width() / 2 - 10
centeredCharacterY = windowManager.centerItemY(characterInto[spriteCounter]) + logo[spriteCounter].get_height() / 2 - 30
centerFontX = windowManager.centerItemX(font)
centerFontY = windowManager.centerItemY(font) + windowManager.centerItemX(logo[spriteCounter]) / 4
while 1:
    pygame.event.pump()
    keyInput = pygame.key.get_pressed()
    pantalla.blit(background, (0, 0))
    dummyCounter += 1
    flag = False
    if dummyCounter >= 1 and dummyCounter < 300 and not spriteCounter == 0:
        spriteCounter = 0
        flag = True
    elif dummyCounter >= 300 and dummyCounter < 600 and not spriteCounter == 1:
        spriteCounter = 1
        flag = True
    elif dummyCounter >= 600 and dummyCounter < 900 and not spriteCounter == 2:
        spriteCounter = 2
        flag = True
    elif dummyCounter >= 900 and dummyCounter < 1200 and not spriteCounter == 1:
        spriteCounter = 1
        flag = True
    elif dummyCounter == 1200:
        dummyCounter = 0
    if flag:
        pantalla.blit(logo[spriteCounter], (centeredLogoX, centeredLogoY))
        pantalla.blit(characterInto[spriteCounter], (centeredCharacterX, centeredCharacterY))
        pantalla.blit(font, (centerFontX, centerFontY))
        pygame.display.update()
    if keyInput[K_RETURN]:
        break
    elif keyInput[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit()
pygame.time.delay(500)
sound.music.stop()
sound = media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_the_long_journey_home.mid'))
sound.music.play(-1)
tildeFile = media.loadReadFile(os.path.join('data', 'maps', 'tiles.txt'))
nwTiles = media.loadReadFile(os.path.join('data', 'maps', 'nwTiles.txt'))
bigTiles = media.loadReadFile(os.path.join('data', 'maps', 'bigTiles.txt'))
dungeonFile = media.loadReadFile(os.path.join('data', 'maps', 'newDungeon.txt'))
firstDungeon = dungeonManager(media, windowManager, pantalla)
firstDungeon.recordNonWalkableTiles(nwTiles)
firstDungeon.recordBigTiles(bigTiles)
firstDungeon.recordTiles(tildeFile)
firstDungeon.recordDungeon(dungeonFile)
pantalla.blit(background, (0, 0))
dracko = spriteManager(firstDungeon, media)
pygame.display.update()
while 1:
    pygame.event.pump()
    keyInput = pygame.key.get_pressed()
    if keyInput[K_UP]:
        dracko.update(1)
    elif keyInput[K_DOWN]:
        dracko.update(2)
    elif keyInput[K_LEFT]:
        dracko.update(3)
    elif keyInput[K_RIGHT]:
        dracko.update(4)
    if keyInput[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit()
    pantalla.blit(background, (0, 0))
    firstDungeon.fillDungeon(0, 150, dracko)
    pygame.display.update()
    pygame.time.delay(250)
sound.music.stop()
pygame.time.delay(1000)



    def _isTileTransparent(self):
        """Checks if sprite is next"""

        self.isNextFlag = False
        self.trash = int(self.elevation[self._col][self._row])
        if self._sprite:
            while 1:
                if self._sprite.mapPosition == [self._col - self.trash + 1, self._row - self.trash]:
                    if self.basePatch >= int(self.elevation[self._sprite.mapPosition[0]][self._sprite.mapPosition[1]]):
                        self.isNextFlag = True
                if self._sprite.mapPosition == [self._col - self.trash, self._row - self.trash]:
                    if self.basePatch >= int(self.elevation[self._sprite.mapPosition[0]][self._sprite.mapPosition[1]]):
                        self.isNextFlag = True
                if self._sprite.mapPosition == [self._col - self.trash - 1, self._row - self.trash]:
                    if self.basePatch >= int(self.elevation[self._sprite.mapPosition[0]][self._sprite.mapPosition[1]]):
                        self.isNextFlag = True
                if self._sprite.mapPosition == [self._col - self.trash, self._row - self.trash + 1]:
                    if self.basePatch >= int(self.elevation[self._sprite.mapPosition[0]][self._sprite.mapPosition[1]]):
                        self.isNextFlag = True
                self.trash -= 1
                if self.trash == 0:
                    break
        return self.isNextFlag

    def fillDungeon(self, sprite = None):
        """Fills the dungeon maps."""

        self._sprite = sprite
        self._stepX = 0
        self._stepY = 150
        self._rewinderStepX = 0
        self._rewinderStepY = 150
        self._decreaseY = 0
        self.lastValueOfY = 150
        self._tmp = 0
        if self._sprite:
            self._moveMapX = self._sprite.mapPosition[1] - 17
            self._moveMapY = self._sprite.mapPosition[0] - 19
            if self._sprite.mapPosition[1] >= 18 and self._sprite.mapScrollX == 1 and (self._moveMapX < len(self.dungeon[0]) - 19 or self._uglyPatch) and self._sprite.mapPosition[1] > self._rowTmp + 17:
                self._rowTmp = self._moveMapX
            elif self._sprite.mapPosition[1] - 1 > self._rowTmp:
                self._rowTmp = self._rowTmp
            elif not self._rowTmp == 0:
                self._rowTmp -= 1
            if self._sprite.mapPosition[0] >= 20 and self._sprite.mapScrollY == 1 and (self._moveMapY < len(self.dungeon) - 21 or self._uglyPatch) and self._sprite.mapPosition[0] > self._colTmp + 19:
                self._colTmp = self._moveMapY
            elif self._sprite.mapPosition[0] - 1 > self._colTmp:
                self._colTmp = self._colTmp
            elif not self._colTmp == 0:
                self._colTmp -= 1
            if self._uglyPatch:
                self._uglyPatch = False
        if self._tmpAnimateSprite == 4:
            self._tmpAnimateSprite = 0
        self._row = self._rowTmp
        self._col = self._colTmp
        self._patch = 30
        self._centeredItemX = self._windowManager.centerItemX(self._dict[self.dungeon[self._col][self._row]]) + 20
        while 1:
            flag = False
            self.basePatch = 1
            if self.dungeon[self._col][self._row] in self.bigTiles:
                if int(self.elevation[self._col][self._row]) > 1:
                    flag = True
                    for self.basePatch in range(1, int(self.elevation[self._col][self._row])):
                        self._transpTile = self._dict["B"].convert()
                        self._transpTile.set_alpha(255 * .5)
                        self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - self.basePatch * 20))
                if flag:
                    self._transpTile = self._dict[self.dungeon[self._col][self._row]].convert()
                    self._transpTile.set_alpha(255 * 1)
                    self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - 80 - int(self.elevation[self._col][self._row]) * 20))                    
                else:
                    self._screen.blit(self._dict[self.dungeon[self._col][self._row]], (self._centeredItemX + self._stepX, self._stepY - 80 - int(self.elevation[self._col][self._row]) * 20))
            elif not self.dungeon[self._col][self._row] is ' ':
                if int(self.elevation[self._col][self._row]) > 1:
                    flag = True
                    for self.basePatch in range(1, int(self.elevation[self._col][self._row])):
                        if self._isTileTransparent():
                            self._transpTile = self._dict["B"].convert()
                            self._transpTile.set_alpha(255 * .5)
                            self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - self.basePatch * 20))
                        else:
                            self._transpTile = self._dict["B"].convert()
                            self._transpTile.set_alpha(255 * 1)
                            self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - self.basePatch * 20))
                if flag:
                    if self._isTileTransparent():
                        self._transpTile = self._dict[self.dungeon[self._col][self._row]].convert()
                        self._transpTile.set_alpha(255 * .5)
                        self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                    else:
                        self._transpTile = self._dict[self.dungeon[self._col][self._row]].convert()
                        self._transpTile.set_alpha(255 * 1)
                        self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                else:
                    self._screen.blit(self._dict[self.dungeon[self._col][self._row]], (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
            if self._sprite:
                if self._sprite.mapPosition == [self._col, self._row]:
                    #self._screen.blit(self._sprite.sprite[self._tmpAnimateSprite], (self._centeredItemX + self._stepX, self._stepY - 20 - (int(self.elevation[self._col][self._row]) * 20)))
                    self._tmpAnimateSprite += 1
            self._stepX += 19
            self._stepY += 10
            self._row += 1
            if self._centeredItemX + self._stepX >= 800 - self._patch or self._row is len(self.dungeon[self._col]):
                self._patch += 19
                self._row = self._rowTmp
                self._col += 1
                self.lastValueOfY = self._stepY
                self._rewinderStepX -= 19
                self._stepX = self._rewinderStepX
                self._rewinderStepY += 10
                self._stepY = self._rewinderStepY
                if self._centeredItemX + self._stepX <= 0 or self._col is len(self.dungeon):
                    break

    def primerNivel(self, stepX = 0, stepY = 150, sprite = None):
        """Fills the dungeon maps."""

        self._stepX = stepX
        self._stepY = stepY
        self._rewinderStepX = 0
        self._rewinderStepY = 150
        self.lastValueOfY = 150
        self._row = self._rowTmp
        self._col = self._colTmp
        self._patch = 30
        self._centeredItemX = self._windowManager.centrarItemX(sprite.spriteActual)
        while 1:
            flag = False
            self.basePatch = 1
            if self.dungeon[self._col][self._row] in self._azulejosGrandes:
                if int(self.elevation[self._col][self._row]) > 1:
                    for self.basePatch in range(1, int(self.elevation[self._col][self._row])):
                        self._transpTile = self._azulejos["baseTierra"].convert()
                        self._transpTile.set_alpha(255 * 1)
                        self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - self.basePatch * 20))
                self._transpTile = self._azulejos[self.dungeon[self._col][self._row]].convert()
                self._transpTile.set_alpha(255 * 1)
                self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - 80 - int(self.elevation[self._col][self._row]) * 20))
            elif not self.dungeon[self._col][self._row] == 'vacio':
                if int(self.elevation[self._col][self._row]) > 1:
                    for self.basePatch in range(1, int(self.elevation[self._col][self._row])):
                        self._transpTile = self._azulejos["baseTierra"].convert()
                        self._transpTile.set_alpha(255 * 1)
                        self._screen.blit(self._transpTile, (self._centeredItemX + self._stepX, self._stepY - self.basePatch * 20))
                self._screen.blit(self._azulejos[self.dungeon[self._col][self._row]], (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                print (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20)
            if sprite:
                #print str(self._row) + " " + str(self._col)
                #print sprite.posicion
                if sprite.posicion == [self._row, self._col]:
                    self._screen.blit(sprite.spriteActual, (self._centeredItemX + (sprite.posicion[0] * 19), 110 + (sprite.posicion[1] * 10)))
            self._stepX += 19
            self._stepY += 10
            self._row += 1
            if self._centeredItemX + self._stepX >= 800 - self._patch or self._row is len(self.dungeon[self._col]):
                self._patch += 19
                self._row = self._rowTmp
                self._col += 1
                self.lastValueOfY = self._stepY
                self._rewinderStepX -= 19
                self._stepX = self._rewinderStepX
                self._rewinderStepY += 10
                self._stepY = self._rewinderStepY
                if self._centeredItemX + self._stepX <= 0 or self._col is len(self.dungeon):
                    break
