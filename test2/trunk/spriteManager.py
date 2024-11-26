import os, sys, random
import pygame
from pygame.locals import *

class spriteManager(object):

    def __init__(self, dungeon, media):

        self.dungeon = dungeon
        self._media = media
        self.mapPosition = [0, 0]
        self.spriteFrontLeft = []
        self.spriteFrontLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoTwo.png')))
        self.spriteFrontLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoOne.png')))
        self.spriteFrontLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoTwo.png')))
        self.spriteFrontLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoThree.png')))
        self.spriteFrontRight = []
        self.spriteFrontRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'front-right-dracko2.png')))
        self.spriteFrontRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'front-right-dracko1.png')))
        self.spriteFrontRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'front-right-dracko2.png')))
        self.spriteFrontRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'front-rigth-dracko3.png')))
        self.spriteBackLeft = []
        self.spriteBackLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoTwo.png')))
        self.spriteBackLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoOne.png')))
        self.spriteBackLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoTwo.png')))
        self.spriteBackLeft.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoThree.png')))
        self.spriteBackRight = []
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoThree.png')))
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoThree.png')))
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoThree.png')))
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoThree.png')))
        self.spriteFrontLeftWater = []
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoThree.png')))
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoThree.png')))
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterTwo.png')))
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterThree.png')))
        self.spriteFrontRightWater = []
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterTwo.png')))
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterOne.png')))
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterTwo.png')))
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterThree.png')))
        self.spriteBackLeftWater = []
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterTwo.png')))
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterOne.png')))
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterTwo.png')))
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterThree.png')))
        self.spriteBackRightWater = []
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterTwo.png')))
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterOne.png')))
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterTwo.png')))
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterThree.png')))
        self.sprite = self.spriteFrontLeft
        self.mapScrollX = 0
        self.mapScrollY = 0

    def update(self, direction):
        """Moves the sprites."""

        if direction is 1:
            if self.mapPosition[0] > 0 and not self._nextNotWalkable(-1, 0):
                self.mapPosition[0] -= 1
                self.mapScrollY = -1
            if self._isInWater():
                self.sprite = self.spriteBackRightWater
            else:
                self.sprite = self.spriteBackRight
        elif direction is 2:
            if self.mapPosition[0] < len(self.dungeon.dungeon) - 1 and not self._nextNotWalkable(1, 0):
                self.mapPosition[0] += 1
                self.mapScrollY = 1
            if self._isInWater():
                self.sprite = self.spriteFrontLeftWater
            else:
                self.sprite = self.spriteFrontLeft
        elif direction is 3:
            if self.mapPosition[1] > 0 and not self._nextNotWalkable(0, -1):
                self.mapPosition[1] -= 1
                self.mapScrollX = -1
            if self._isInWater():
                self.sprite = self.spriteBackLeftWater
            else:
                self.sprite = self.spriteBackLeft
        elif direction is 4:
            if self.mapPosition[1] < len(self.dungeon.dungeon[0]) - 1 and not self._nextNotWalkable(0, 1):
                self.mapPosition[1] += 1
                self.mapScrollX = 1
            if self._isInWater():
                self.sprite = self.spriteFrontRightWater
            else:
                self.sprite = self.spriteFrontRight

    def _nextNotWalkable(self, row, col):
        """Checks if next tilde is deep water."""

        if self.dungeon.dungeon[self.mapPosition[0] + row][self.mapPosition[1] + col] in self.dungeon.nwTiles:
            return True
        else:
            return False

    def _isInWater(self):
        """Checks if the character is walking in water."""

        if self.dungeon.dungeon[self.mapPosition[0]][self.mapPosition[1]] is "W":
            return True
        else:
            return False
