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
        self.flame_burst_group=pygame.sprite.Group()
        self.ice_spike_group=pygame.sprite.Group()
        self.blizzard_group=pygame.sprite.Group()
        self.light_storm_group=pygame.sprite.Group()

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
                if char != '\n': # less fancy
                    self.nwTiles.append(char)

    def recordDungeon(self, dungeonFile):
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



    def fillDungeon_tiles(self, unit_positions, target_position = False,selected_attack=None, played=False, monsters=None, move_range = 2):
            """Render only the tiles of the dungeon."""
            self._stepX = 0 # en pixel
            self._stepY = 150
            self._rewinderStepX = 0 # At the start of each row, self._stepX is reset to self._rewinderStepX ensuring the rows are correctly spaced.
            self._rewinderStepY = 150
            self._row = self._rowTmp #  the current row in the dungeon map to be rendered.
            self._col = self._colTmp # en terme de nombre de colonnes
            self._patch = 30 # to avoid overlap
            # X-coordinate where the current tile should be rendered, 
            monster_pos=set()
            for monster in monsters:
            #highlight_positions.add((-1, -1))  
                monster_pos.add(tuple(monster.mapPosition))

            self._centeredItemX = self._windowManager.centerItemX(self._dict[self.dungeon[self._col][self._row]]) + 20
                            
            highlight_positions = set()
            if played == 0:    
                row, col = unit_positions
                if not target_position:
                    for dr in range(-move_range, move_range + 1):
                        for dc in range(-move_range, move_range + 1):
                            if abs(dr) + abs(dc) <= move_range:  # Limit to a radius of 2 tiles
                                highlight_positions.add((row + dr, col + dc))
                else:
                    highlight_positions.add((row, col))

                self.previous_highlight_positions = highlight_positions

            else: # utiliser le highlighte_positions precedent
                highlight_positions = self.previous_highlight_positions
            
            while True:# boucle pour l'affiche en iso
                current_position = (self._col, self._row)
                if current_position in (monster_pos-highlight_positions):
                    self._screen.blit(self._dict["S"], (
                        self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                # Tile highlight
                
                elif current_position in highlight_positions:
                    if not target_position:
                        self._screen.blit(self._dict["R"], (
                        self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                    else:
                        #print("test")
                        self._screen.blit(self._dict["W"], (
                        self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                        
                        if selected_attack=="Thunder Strike":

                            image = self._media.loadImage(os.path.join('data', 'images', 'effects', 'thunder.png'))
                            #self.play(selected_attack, current_position, image)
                            self._screen.blit(self._dict["C"], (self._centeredItemX + self._stepX + 10,
                                                            self._stepY-40 - int(self.elevation[self._col][self._row]) * 30))
                
                #if current_position in monster_pos:
                #    self._screen.blit(self._dict["S"], (
                #        self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
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
                    
            return highlight_positions

    def fillDungeon_tiles2(self, unit_positions, target_position = False,selected_attack=None, played=False, monsters=None, move_range = 2):
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
        monster_pos=set()
        for monster in monsters:
            #highlight_positions.add((-1, -1))  
            monster_pos.add(tuple(monster.mapPosition))
            #highlight_positions.add(tuple(monster.mapPosition))
        if played == 0:    
            row, col = unit_positions
            if not target_position:
                for dr in range(-move_range, move_range + 1):
                    for dc in range(-move_range, move_range + 1):
                        if abs(dr) + abs(dc) <= move_range:  
                            highlight_positions.add((row + dr, col + dc))
            else:
                highlight_positions.add((row, col))

            self.previous_highlight_positions = highlight_positions

        else: # utiliser le highlighte_positions precedent
            highlight_positions = self.previous_highlight_positions
        
        # print(highlight_positions)
        while True:# boucle pour l'affiche en iso
            current_position = (self._col, self._row)
            
            # Tile highlight
            if current_position in highlight_positions:
                if any(current_position == tuple(monsters[i].mapPosition) for i in range(len(monsters))):
                    highlight_type = "S"
                else:
                    highlight_type = "R"
                    
                if not target_position:
                    self._screen.blit(self._dict[highlight_type], (
                    self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                else:
                    self._screen.blit(self._dict[highlight_type], (
                    self._centeredItemX + self._stepX, self._stepY - int(self.elevation[self._col][self._row]) * 20))
                    
                    #if selected_attack=="Thunder Strike" and target_position:
                        
                     #   self._screen.blit(self._dict["C"], (self._centeredItemX + self._stepX + 10,
                        #                                self._stepY-40 - int(self.elevation[self._col][self._row]) * 30))
            new_var = highlight_positions.difference(monster_pos)
            if current_position in new_var:
                if target_position:
                    if selected_attack=="Thunder Strike":
                        
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
                
        return highlight_positions
    
    def fillDungeon_attack_tiles(self, unit_position, selected_attack,render=False):
        """
        Affiche la portée d'attaque avec des tuiles statiques (type F)
        et retourne les positions mises en surbrillance.
        """
        # Définir la portée de l'attaque selon le type d'attaque sélectionnée
        attack_range = {  # change here for attack range
            "Water Splash": 1,
            "Tsunami Wave": 2,
            "Fireball": 3,
            "Flame Burst": 1,
            "Thunder Strike": 4,
            "Lightning Strom":2,
            "Ice Spike": 2,
            "Blizzard": 3

        }.get(selected_attack, 2)  # Par défaut, portée de 2

        # Calculer les positions mises en surbrillance
        row, col = unit_position
        highlight_positions = set()
        for dr in range(-attack_range, attack_range + 1):
            for dc in range(-attack_range, attack_range + 1):
                if abs(dr) + abs(dc) <= attack_range:  # Restriction à une zone en losange
                    highlight_positions.add((row + dr, col + dc))
        if render:
            # Parcourir toutes les positions de la carte pour afficher les tuiles
            self._stepX = 0
            self._stepY = 150
            self._rewinderStepX = 0
            self._rewinderStepY = 150
            self._row = self._rowTmp
            self._col = self._colTmp
            self._patch = 30
            self._centeredItemX = self._windowManager.centerItemX(self._dict[self.dungeon[self._col][self._row]]) + 20

            while True:
                current_position = (self._col, self._row)

                # Si la position actuelle est dans la portée d'attaque, afficher une tuile statique (F)
                if current_position in highlight_positions:
                    self._screen.blit(self._dict["X"], (self._centeredItemX + self._stepX + 10,
                                                        self._stepY +10 - int(self.elevation[self._col][self._row]) * 30))  # Tuiles statiques de portée

                # Passer à la prochaine tuile
                self._stepX += 19
                self._stepY += 10
                self._row += 1

                # Vérifier si on atteint la fin de la rangée ou de la carte
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

        return highlight_positions




        
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
                # print(self._stepX, self._stepY)
            # Health bar rendering
            if is_active and sprite.mapPosition == [self._col, self._row]:
                sprite.healthBarePosition = [self._centeredItemX + self._stepX + 7, self._stepY - 30 - int(self.elevation[self._col][self._row]) * 20]
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






    def fillDungeon_monsters(self, monster, screen):
        """Render only the monster in the dungeon."""
        self._stepX = 0
        self._stepY = 150
        self._rewinderStepX = 0
        self._rewinderStepY = 150
        self._row = self._rowTmp
        self._col = self._colTmp
        self._patch = 30
        self._centeredItemX = self._windowManager.centerItemX(self._dict[self.dungeon[self._col][self._row]]) + 20

        while True:
            # Monster rendering
            if monster and monster.mapPosition == [self._col, self._row]:
                self._screen.blit(
                    monster.sprite[monster._tmpAnimateSprite],
                    (self._centeredItemX + self._stepX, self._stepY - 20 - int(self.elevation[self._col][self._row]) * 20)
                )
                monster._tmpAnimateSprite = (monster._tmpAnimateSprite + 1) % len(monster.sprite)

            # Health bar rendering
            if monster.mapPosition == [self._col, self._row]:
                monster.healthBarePosition = [self._centeredItemX + self._stepX +7, self._stepY - 30 - int(self.elevation[self._col][self._row]) * 20]
                monster.draw_health_bar(screen)

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
        x = centered_x + (col - row) * 19.5  
        y = 150 + (row + col) * 10.5 - int(self.elevation[row][col]) * 20
        return x, y

    def display_image_for_one_second(self,position):
        """
        Affiche une image à l'écran pendant 1 seconde.

        :param screen: L'objet surface principal de Pygame
        :param image: L'image à afficher
        :param position: Tuple (x, y) pour la position de l'image
        """
        image = self._media.loadImage(os.path.join('data', 'images', 'effects', 'thunder.png'))
        start_time = pygame.time.get_ticks()  # Obtenez le temps initial
        duration = 1000  # Durée en millisecondes (1 seconde)

        while pygame.time.get_ticks() - start_time < duration:
            self._screen.blit(image, (position[0],position[1] - 50))
            pygame.display.update()
        # Calculate isometric screen coordinates

        #self._screen.blit(image, (position[0], position[1] - 50))


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

            #self._screen.blit(image, (target_x, target_y-50))

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
            #self._screen.blit(image, (target_x, target_y - 50))

        elif attack_type == "Fireball" and start_position:
            # Initialize and add the fireball animation
            fireball = Fireball(start_position, target_position, self)
            self.fireball_group.add(fireball)

        elif attack_type == "Tsunami Wave" and start_position:
            # Initialize and add the fireball animation
            tsunami = Tsunami(start_position, target_position, self)
            self.tsunami_group.add(tsunami)
        elif attack_type == "Flame Burst" and start_position:
            # Initialize and add the fireball animation
            flame = Flameburst(target_position, self)
            self.flame_burst_group.add(flame)
        elif attack_type == "Ice Spike" and start_position:
            # Initialize and add the fireball animation
            ice = Icespike(target_position, self)
            self.ice_spike_group.add(ice)
        elif attack_type == "Blizzard" and start_position:
            # Initialize and add the fireball animation
            bli = Blizzard(start_position, target_position, self)
            self.blizzard_group.add(bli)

        elif attack_type == "Lightning Storm" and start_position:
            # Initialize and add the fireball animation
            sto = Lightstorm(target_position, self)
            self.light_storm_group.add(sto)



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
        self.steps = 5  # Adjust for animation smoothness
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
            if self.counter % 1 == 0 and self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]

            # Check if the fireball reached the target
            self.counter += 1
            if self.counter >= self.steps:
                self.finished = True
                self.kill()

class Flameburst(pygame.sprite.Sprite):
    def __init__(self, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load flame burst images for animation
        self.images = [
            pygame.transform.scale(
                pygame.image.load(f'images/fireburst/flame_burst{i}.png'), (30, 30)
            ) for i in range(6)
        ]

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Get the exact isometric position for the target
        self.target_x, self.target_y = self.dungeon_manager.get_isometric_position(*target_position)

        # Apply a vertical offset for positioning (if needed)
        self.target_y -= 10
        self.target_x += 17  # Adjust for image alignment
        self.rect.center = (self.target_x, self.target_y)

        self.counter = 0
        self.finished = False

    def update(self):
        if not self.finished:
            # Display the animation frame-by-frame
            if self.counter % 1 == 0:  # Adjust frame delay for animation speed
                if self.index < len(self.images) - 1:
                    self.index += 1
                    self.image = self.images[self.index]
                else:
                    self.finished = True
                    self.kill()  # Remove the sprite when animation ends

            # Increment the counter for frame delay
            self.counter += 1


class Tsunami(pygame.sprite.Sprite):
    def __init__(self, start_position, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load fireball images for animation
        self.images = []
        for i in range(1, 5):  # Assuming 4 frames for the explosion
            img = pygame.image.load(f'images/tsunami/tsu{i}.png')
            img = pygame.transform.scale(img, (60, 60))  # Adjust fireball size
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
        self.steps = 5  # Adjust for animation smoothness
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
            if self.counter % 1 == 0 and self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]

            # Check if the fireball reached the target
            self.counter += 1
            if self.counter >= self.steps:
                self.finished = True
                self.kill()

class Icespike(pygame.sprite.Sprite):
    def __init__(self, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load flame burst images for animation
        self.images = [
            pygame.transform.scale(
                pygame.image.load(f'images/icespike/ice_spike{i}.png'), (40, 40)
            ) for i in range(12)
        ]

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Get the exact isometric position for the target
        self.target_x, self.target_y = self.dungeon_manager.get_isometric_position(*target_position)

        # Apply a vertical offset for positioning (if needed)
        self.target_y -= 10
        self.target_x += 17  # Adjust for image alignment
        self.rect.center = (self.target_x, self.target_y)

        self.counter = 0
        self.finished = False

    def update(self):
        if not self.finished:
            # Display the animation frame-by-frame
            if self.counter % 1 == 0:  # Adjust frame delay for animation speed
                if self.index < len(self.images) - 1:
                    self.index += 1
                    self.image = self.images[self.index]
                else:
                    self.finished = True
                    self.kill()  # Remove the sprite when animation ends






class Blizzard(pygame.sprite.Sprite):
    def __init__(self, start_position, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load fireball images for animation
        self.images = []
        for i in range(0, 9):  # Assuming  frames for the explosion
            img = pygame.image.load(f'images/blizzard/blizzard{i}.png')
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
        self.steps = 8  # Adjust for animation smoothness
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
            if self.counter % 1 == 0 and self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]

            # Check if the fireball reached the target
            self.counter += 1
            if self.counter >= self.steps:
                self.finished = True
                self.kill()

class Lightstorm(pygame.sprite.Sprite):
    def __init__(self, target_position, dungeon_manager):
        super().__init__()
        self.dungeon_manager = dungeon_manager

        # Load flame burst images for animation
        self.images = [
            pygame.transform.scale(
                pygame.image.load(f'images/lightstorm/New Piskel-{i}.png.png'), (60, 60)
            ) for i in range(1,8)
        ]

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Get the exact isometric position for the target
        self.target_x, self.target_y = self.dungeon_manager.get_isometric_position(*target_position)

        # Apply a vertical offset for positioning (if needed)
        self.target_y -= 25
        self.target_x += 17  # Adjust for image alignment
        self.rect.center = (self.target_x, self.target_y)

        self.counter = 0
        self.finished = False

    def update(self):
        if not self.finished:
            # Display the animation frame-by-frame
            if self.counter % 1 == 0:  # Adjust frame delay for animation speed
                if self.index < len(self.images) - 1:
                    self.index += 1
                    self.image = self.images[self.index]
                else:
                    self.finished = True
                    self.kill()