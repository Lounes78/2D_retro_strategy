import os, sys, random
import pygame
from pygame.locals import *

class dungeonManager(object):
    """Manages the dungeon drawing."""

    def __init__(self, media, windowManager, screen):
        """Manages the dungeon."""

        self._windowManager = windowManager
        self._media = media
        self._screen = screen
        self._dict = {}
        self._rowTmp = 0
        self._colTmp = 0
        self._tmpAnimateSprite = 0

    def recordTiles(self, tileFile): # create a dictionary of terrain tiles from the tiles.txt file
        """Seeks usable tiles."""
        
        for line in tileFile: # Each tile has a key (G, M, ...)
            if len(line.split()) == 2:
                # G grass.png
                self._dict[line.split()[0]] = self._media.loadImage(os.path.join('data', 'images', 'terrain', line.split()[1]))
            else:
                print ("Theres an error in the tile file.")
                sys.exit()

    def recordNonWalkableTiles(self, nwtFile):

        self.nwTiles = []
        for line in nwtFile:
            for char in line:
                # if not ord(char) is 10: # ord(10) is the ascii code for '\n'
                if char != '\n': # less fancy
                    self.nwTiles.append(char)

    def recordDungeon(self, dungeonFile):
        """Records a dungeon."""

        self._row = []
        self._rowTwo = []                                           # line 1         line 2    etc
        self.dungeon = [] # For terrain data EX: self.dungeon = [['G', 'G', 'M'], ['M', 'G' etc]]
        self.elevation = [] # For elevation data EX: self.elevation = [['2', '1', '0'], ['1', '0', etc]]
        for line in dungeonFile:  # [2:G] -> 2: elevation | G: grass.png
            self._row = []
            self._rowTwo = []
            self._tokenStart = 1 # to exclude the [
            self._tokenEnd = 4 # the position of the data
            while line[self._tokenStart:self._tokenEnd]: # as long as it is a valid tile definition 
                self._row.append(line[self._tokenStart + 2:self._tokenEnd])  # get the type of the tile
                self._rowTwo.append(line[self._tokenStart:self._tokenEnd - 2]) # get the elevation of the tile
                self._tokenStart += 5
                self._tokenEnd += 5
            self.dungeon.append(self._row)
            self.elevation.append(self._rowTwo)


    # Draw the actual map
    def fillDungeon(self, sprite = None):
        """ Fills the dungeon maps.
            It processes each tile in the dungeon map and displays it with appropriate visual elements
            e.g., elevation, items, and a sprite representing a player or object.
        """
        
        self._sprite = sprite # The character or object being rendered, has prop like mapPosition, ...
        self._stepX = 0         # Track the current screen position for rendering tiles
        self._stepY = 150       # """"""""
        self._rewinderStepX = 0
        self._rewinderStepY = 150
        self._decreaseY = 0
        self.lastValueOfY = 150
        self._tmp = 0
        self._moveMapX = self._sprite.mapPosition[1] - 17
        self._moveMapY = self._sprite.mapPosition[0] - 19
        
        if self._sprite:
            if self._tmpAnimateSprite == 4:
                self._tmpAnimateSprite = 0
            if self._sprite.mapPosition[1] >= 18 and self._sprite.mapScrollX == 1 and self._moveMapX < len(self.dungeon[0]) - 19 and self._sprite.mapPosition[1] > self._rowTmp + 17:
                self._rowTmp = self._moveMapX
            elif self._sprite.mapPosition[1] - 1 > self._rowTmp:
                self._rowTmp = self._rowTmp
            elif not self._rowTmp == 0:
                self._rowTmp -= 1
            if self._sprite.mapPosition[0] >= 20 and self._sprite.mapScrollY == 1 and self._moveMapY < len(self.dungeon) - 21 and self._sprite.mapPosition[0] > self._colTmp + 19:
                self._colTmp = self._moveMapY
            elif self._sprite.mapPosition[0] - 1 > self._colTmp:
                self._colTmp = self._colTmp
            elif not self._colTmp == 0:
                self._colTmp -= 1
                
        self._row = self._rowTmp
        self._col = self._colTmp
        self._patch = 30
        self._centeredItemX = self._windowManager.centerItemX(self._dict[self.dungeon[self._col][self._row]]) + 20
        
        while 1: #  iterates through the dungeon map, rendering one tile at a time
            
            # Tile rendering
            if self.dungeon[self._col][self._row] is 'M':
                if int(self.elevation[self._col][self._row]) > 1:
                    for basePatch in range(1, int(self.elevation[self._col][self._row])):
                        self._screen.blit(self._dict["B"], (self._centeredItemX + self._stepX, self._stepY - basePatch * 20))
                self._screen.blit(self._dict[self.dungeon[self._col][self._row]], (self._centeredItemX + self._stepX, self._stepY - 80 - int(self.elevation[self._col][self._row]) * 20))            
            elif not self.dungeon[self._col][self._row] is ' ':
                if int(self.elevation[self._col][self._row]) > 1:
                    for basePatch in range(1, int(self.elevation[self._col][self._row])):
                        self._screen.blit(self._dict["B"], (self._centeredItemX + self._stepX, self._stepY - basePatch * 20))
                self._screen.blit(self._dict[self.dungeon[self._col][self._row]], (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
            
            # Sprite rendering
            if self._sprite:
                if self._sprite.mapPosition == [self._col, self._row]:
                    self._screen.blit(self._sprite.sprite[self._tmpAnimateSprite], (self._centeredItemX + self._stepX, self._stepY - 20 - (int(self.elevation[self._col][self._row]) * 20)))
                    self._tmpAnimateSprite += 1
                    
            # Move to the next tile in the row 
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
