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





    def fillDungeon_tiles(self, unit_positions, target_position = False):
        """Render only the tiles of the dungeon."""
        self._stepX = 0 # en pixel
        self._stepY = 150
        self._rewinderStepX = 0 # At the start of each row, self._stepX is reset to self._rewinderStepX ensuring the rows are correctly spaced.
        self._rewinderStepY = 150
        self._row = self._rowTmp #  the current row in the dungeon map to be rendered.
        self._col = self._colTmp # en terme de nombre de colonnes
        self._patch = 30 # to avoid overlap
        # X-coordinate where the current tile should be rendered, 
        self._centeredItemX = self._windowManager.centerItemX(self._dict[self.dungeon[self._col][self._row]]) + 20
                        
        highlight_positions = set()
        row, col = unit_positions
        if not target_position:
            for dr in [-2, -1, 0]:
                for dc in [-2, -1, 0]:
                    if abs(dr) + abs(dc) <= 2:  # Limit to a radius of 2 tiles
                        highlight_positions.add((row + dr, col + dc))
        else:
            highlight_positions.add((row, col))
        
        while True:
            current_position = (self._col, self._row)

            # Tile highlight
            if current_position in highlight_positions:
                self._screen.blit(self._dict["R"], (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
            # Tile rendering
            elif self.dungeon[self._col][self._row] == 'M':
                if int(self.elevation[self._col][self._row]) > 1:
                    for basePatch in range(1, int(self.elevation[self._col][self._row])):
                        self._screen.blit(self._dict["B"], (self._centeredItemX + self._stepX, self._stepY - basePatch * 20)) #   -80 cause it should appear higher
                self._screen.blit(self._dict[self.dungeon[self._col][self._row]], (self._centeredItemX + self._stepX, self._stepY - 80 - int(self.elevation[self._col][self._row]) * 20))
            elif self.dungeon[self._col][self._row] != ' ':
                if int(self.elevation[self._col][self._row]) > 1:
                    for basePatch in range(1, int(self.elevation[self._col][self._row])):
                        self._screen.blit(self._dict["B"], (self._centeredItemX + self._stepX, self._stepY - basePatch * 20))
                self._screen.blit(self._dict[self.dungeon[self._col][self._row]], (self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))

            # Move to the next tile in the row
            self._stepX += 19
            self._stepY += 10
            self._row += 1

            # Check if the end of the row or screen width is reached
            if self._centeredItemX + self._stepX >= 800 - self._patch or self._row >= len(self.dungeon[self._col]):
                self._patch += 19
                self._row = self._rowTmp
                self._col += 1
                self._rewinderStepX -= 19
                self._stepX = self._rewinderStepX
                self._rewinderStepY += 10
                self._stepY = self._rewinderStepY

                if self._centeredItemX + self._stepX <= 0 or self._col >= len(self.dungeon):
                    break



        
    def fillDungeon_sprites(self, sprite, is_active, screen):
        """Render only the sprite in the dungeon and highlight specific tiles."""
        self._stepX = 0
        self._stepY = 150
        self._rewinderStepX = 0
        self._rewinderStepY = 150
        self._row = self._rowTmp
        self._col = self._colTmp
        self._patch = 30
        self._centeredItemX = self._windowManager.centerItemX(self._dict[self.dungeon[self._col][self._row]]) + 20

        while True:
            # Sprite rendering
            if sprite and sprite.mapPosition == [self._col, self._row]:
                self._screen.blit(
                    sprite.sprite[sprite._tmpAnimateSprite],
                    (self._centeredItemX + self._stepX, self._stepY - 20 - int(self.elevation[self._col][self._row]) * 20)
                )
                sprite._tmpAnimateSprite = (sprite._tmpAnimateSprite + 1) % len(sprite.sprite)

            # Health bar rendering
            if is_active and sprite.mapPosition == [self._col, self._row]:
                sprite.healthBarePosition = [self._centeredItemX + self._stepX - 6, self._stepY - 20 - int(self.elevation[self._col][self._row]) * 20]
                sprite.draw_health_bar(screen)


            # Move to the next tile in the row
            self._stepX += 19
            self._stepY += 10
            self._row += 1
            # Check if the end of the row or screen width is reached
            if self._centeredItemX + self._stepX >= 800 - self._patch or self._row >= len(self.dungeon[self._col]):
                self._patch += 19
                self._row = self._rowTmp
                self._col += 1
                self._rewinderStepX -= 19
                self._stepX = self._rewinderStepX
                self._rewinderStepY += 10
                self._stepY = self._rewinderStepY

            # Break if we reach the end of the dungeon
            if self._centeredItemX + self._stepX <= 0 or self._col >= len(self.dungeon):
                break
            
            


