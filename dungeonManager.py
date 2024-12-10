import os, sys, random
import pygame
from pygame.locals import *
import math
#from attackAnimation import *

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
        self.fireball_group = pygame.sprite.Group()
        self.tsunami_group=pygame.sprite.Group()

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





    def fillDungeon_tiles(self, unit_positions, target_position = False,selected_attack=None):
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
            for dr in [-2, -1, 0,1,2]:
                for dc in [-2, -1, 0,1,2]:
                    if abs(dr) + abs(dc) <= 2:  # Limit to a radius of 2 tiles
                        highlight_positions.add((row + dr, col + dc))
        else:
            highlight_positions.add((row, col))
        
        while True:# boucle pour l'affiche en iso
            current_position = (self._col, self._row)

            # Tile highlight
            if current_position in highlight_positions:
                if not target_position:
                    self._screen.blit(self._dict["R"], (
                    self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                else:
                    self._screen.blit(self._dict["R"], (
                    self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                    if selected_attack=="Thunder Strike":
                        # Example usage in your game loop
                        image = self._media.loadImage(os.path.join('data', 'images', 'effects', 'thunder.png'))
                        #self.play(selected_attack, current_position, image)

                        self._screen.blit(self._dict["C"], (self._centeredItemX + self._stepX + 10,
                                                        self._stepY-40 - int(self.elevation[self._col][self._row]) * 30))

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

    def get_isometric_position(self, row, col):
        """
        Converts grid (row, col) to isometric screen coordinates.
        """
        base_tile = self._dict[self.dungeon[row][col]]
        centered_x = self._windowManager.centerItemX(base_tile) + 20
        x = centered_x + (col - row) * 19.5  # Use float for better alignment
        y = 150 + (row + col) * 10.5 - int(self.elevation[row][col]) * 20
        return x, y


    def play(self, attack_type, target_position, start_position=None):
        """
        Plays an attack animation on the specified tile.
        :param attack_type: The type of attack (e.g., "Thunder Strike").
        :param target_position: The logical grid position (row, col) of the target tile.
        :param start_position: The logical grid position (row, col) of the start tile (for fireball).
        """
        if attack_type == "Thunder Strike":
            # Load the effect image
            image = self._media.loadImage(os.path.join('data', 'images', 'effects', 'thunder.png'))
            target_x, target_y = self.get_isometric_position(*target_position)
            duration = 500  # Duration in milliseconds
            start_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start_time < duration:
                self._screen.blit(image, (target_x, target_y - 50))
                pygame.display.update()
            # Calculate isometric screen coordinates

            self._screen.blit(image, (target_x, target_y-50))

        if attack_type == "Water Splash":
            image = self._media.loadImage(os.path.join('data', 'images', 'effects', 'water splash.png'))

            # Calculate isometric screen coordinates
            target_x, target_y = self.get_isometric_position(*target_position)
            img = pygame.transform.scale(image, (50, 50))
            duration = 500  # Duration in milliseconds
            start_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start_time < duration:
                self._screen.blit(img, (target_x, target_y - 50))
                pygame.display.update()
            #self._screen.blit(img, (target_x, target_y - 50))

        elif attack_type == "Fireball" and start_position:
            # Initialize and add the fireball animation
            fireball = Fireball(start_position, target_position, self)
            self.fireball_group.add(fireball)

        elif attack_type == "Tsunami Wave" and start_position:
            # Initialize and add the fireball animation
            tsunami = Tsunami(start_position, target_position, self)
            self.tsunami_group.add(tsunami)




class Fireball(pygame.sprite.Sprite):
    def __init__(self, start_position, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load fireball images for animation
        self.images = []
        for i in range(1, 5):  # Assuming 5 frames for the explosion
            img = pygame.image.load(f'images/fireball/exp{i}.png')
            img = pygame.transform.scale(img, (50, 50))  # Adjust fireball size
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Get screen positions for start and target
        self.start_x, self.start_y = self.dungeon_manager.get_isometric_position(*start_position)
        self.target_x, self.target_y = self.dungeon_manager.get_isometric_position(*target_position)

        # Set fireball position to start
        self.current_x = float(self.start_x)
        self.current_y = float(self.start_y)

        # Calculate total distance and step increments
        self.total_distance = math.sqrt((self.target_x - self.start_x) ** 2 + (self.target_y - self.start_y) ** 2)
        self.steps = 15  # Adjust for animation smoothness
        self.step_x = (self.target_x - self.start_x) / self.steps
        self.step_y = (self.target_y - self.start_y) / self.steps

        self.counter = 0
        self.finished = False

    def update(self):
        if not self.finished:
            # Move the fireball
            self.current_x += self.step_x
            self.current_y += self.step_y
            self.rect.center = (self.current_x, self.current_y)

            # Update the animation frame
            if self.counter % 2 == 0 and self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]

            # Check if the fireball reached the target
            self.counter += 1
            if self.counter >= self.steps:
                self.finished = True
                self.kill()

class Tsunami2(pygame.sprite.Sprite):
    def __init__(self, start_position, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load tsunami images for animation
        self.images = []
        for i in range(1, 5):  # Assuming 4 frames for the animation
            img = pygame.image.load(f'images/tsunami/tsu{i}.png')
            img = pygame.transform.scale(img, (50, 50))  # Adjust size as needed
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Get isometric screen positions
        self.start_x, self.start_y = self.dungeon_manager.get_isometric_position(*start_position)
        self.target_x, self.target_y = self.dungeon_manager.get_isometric_position(*target_position)

        # Set initial position
        self.current_x = float(self.start_x)
        self.current_y = float(self.start_y)

        # Calculate distance and steps
        self.total_distance = math.sqrt((self.target_x - self.start_x) ** 2 + (self.target_y - self.start_y) ** 2)
        self.steps = 15  # Total animation steps
        self.step_x = (self.target_x - self.start_x) / self.steps
        self.step_y = (self.target_y - self.start_y) / self.steps

        self.step_counter = 0
        self.frame_duration = 4  # Number of steps each frame lasts
        self.finished = False

    def update(self):
        if not self.finished:
            # Move the fireball
            self.current_x += self.step_x
            self.current_y += self.step_y
            self.rect.center = (self.current_x, self.current_y)

            # Update frame based on step count
            if self.step_counter % self.frame_duration == 0 and self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]

            # Check if the fireball has reached the target
            self.step_counter += 1
            if self.step_counter >= self.steps:
                self.finished = True
                self.kill()

class Tsunami(pygame.sprite.Sprite):
    def __init__(self, start_position, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load fireball images for animation
        self.images = []
        for i in range(1, 5):  # Assuming 4 frames for the explosion
            img = pygame.image.load(f'images/tsunami/tsu{i}.png')
            img = pygame.transform.scale(img, (50, 50))  # Adjust fireball size
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Get screen positions for start and target
        self.start_x, self.start_y = self.dungeon_manager.get_isometric_position(*start_position)
        self.target_x, self.target_y = self.dungeon_manager.get_isometric_position(*target_position)

        # Set fireball position to start
        self.current_x = float(self.start_x)
        self.current_y = float(self.start_y)

        # Calculate total distance and step increments
        self.total_distance = math.sqrt((self.target_x - self.start_x) ** 2 + (self.target_y - self.start_y) ** 2)
        self.steps = 15  # Adjust for animation smoothness
        self.step_x = (self.target_x - self.start_x) / self.steps
        self.step_y = (self.target_y - self.start_y) / self.steps

        self.counter = 0
        self.finished = False

    def update(self):
        if not self.finished:
            # Move the fireball
            self.current_x += self.step_x
            self.current_y += self.step_y
            self.rect.center = (self.current_x, self.current_y)

            # Update the animation frame
            if self.counter % 2 == 0 and self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]

            # Check if the fireball reached the target
            self.counter += 1
            if self.counter >= self.steps:
                self.finished = True
                self.kill()







