



import os
import pygame
from spriteManager import spriteManager
import random

class WaterMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Water Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.movement_range=2
        self.move_counter=0
        self.attacks = ["Water Splash", "Tsunami Wave"]

    def load_default_sprites(self):
        """Load default sprite images for general characters."""
        self.spriteFrontLeft = []
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '0.png')),(30, 30)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '1.png')),(30, 30)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '2.png')),(30, 30)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '3.png')),(30, 30)))
        
        self.sprite = self.spriteFrontLeft

    def move_randomly(self, other_monsters, player_units):
        self.move_counter += 1  # Incrémente le compteur à chaque appel

        # Se déplacer uniquement toutes les 20 itérations
        if self.move_counter < 30:
            return  # Ne rien faire si le compteur n'a pas atteint 20

        # Réinitialiser le compteur après déplacement
        self.move_counter = 0

        # Générer un déplacement aléatoire
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        for direction in directions:
            new_row = self.mapPosition[0] + direction[0]
            new_col = self.mapPosition[1] + direction[1]

            # Vérifier les conditions de validité
            if (
                0 <= new_row < len(self.dungeon.dungeon) and
                0 <= new_col < len(self.dungeon.dungeon[0]) and
                abs(new_row - self.mapPosition[0]) <= self.movement_range and
                abs(new_col - self.mapPosition[1]) <= self.movement_range and
                all(monster.mapPosition != [new_row, new_col] for monster in other_monsters) and  # Vérifie les autres monstres
                all(unit.mapPosition != [new_row, new_col] for unit in player_units)   # Vérifie les cases non walkables
            ):
                #print(f"Monster {self.name} moving from {self.mapPosition} to [{new_row}, {new_col}]")
                self.mapPosition = [new_row, new_col]
                break



    def perform_special_attack(self, target):
        #print(f"{self.name} unleashes a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(30)

class FlyMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Fire Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.movement_range=2
        self.move_counter=0
        self.attacks = ["Fireball", "Flame Burst"]
    def load_default_sprites(self):
        """Load default sprite images for general characters."""
        self.spriteFrontLeft = []
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster2_0.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster2_1.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster2_2.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster2_3.png')),(35, 35)))
        self.spriteFrontRight = []
        self.sprite = self.spriteFrontLeft
    def move_randomly(self, other_monsters, player_units):
        self.move_counter += 1  # Incrémente le compteur à chaque appel

        # Se déplacer uniquement toutes les 20 itérations
        if self.move_counter < 5:
            return  # Ne rien faire si le compteur n'a pas atteint 20

        # Réinitialiser le compteur après déplacement
        self.move_counter = 0

        # Générer un déplacement aléatoire
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        for direction in directions:
            new_row = self.mapPosition[0] + direction[0]
            new_col = self.mapPosition[1] + direction[1]

            # Vérifier les conditions de validité
            if (
                0 <= new_row < len(self.dungeon.dungeon) and
                0 <= new_col < len(self.dungeon.dungeon[0]) and
                abs(new_row - self.mapPosition[0]) <= self.movement_range and
                abs(new_col - self.mapPosition[1]) <= self.movement_range and
                all(monster.mapPosition != [new_row, new_col] for monster in other_monsters) and  # Vérifie les autres monstres
                all(unit.mapPosition != [new_row, new_col] for unit in player_units)   # Vérifie les cases non walkables
            ):
                #print(f"Monster {self.name} moving from {self.mapPosition} to [{new_row}, {new_col}]")
                self.mapPosition = [new_row, new_col]
                break
        self.sprite = self.spriteFrontLeft

    def perform_special_attack(self, target):
        #print(f"{self.name} casts {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(35)

class PoisonMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Ice Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.movement_range=2
        self.move_counter=0
        self.attacks = ["Ice Spike", "Blizzard"]
    def load_default_sprites(self):
        """Load default sprite images for general characters."""
        self.spriteFrontLeft = []
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster5_0.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster5_1.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster5_2.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster5_3.png')),(35, 35)))
        self.spriteFrontRight = []
        
        self.sprite = self.spriteFrontLeft
    def move_randomly(self, other_monsters, player_units):
        self.move_counter += 1  # Incrémente le compteur à chaque appel

        # Se déplacer uniquement toutes les 20 itérations
        if self.move_counter < 30:
            return  # Ne rien faire si le compteur n'a pas atteint 20

        # Réinitialiser le compteur après déplacement
        self.move_counter = 0

        # Générer un déplacement aléatoire
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        for direction in directions:
            new_row = self.mapPosition[0] + direction[0]
            new_col = self.mapPosition[1] + direction[1]

            # Vérifier les conditions de validité
            if (
                0 <= new_row < len(self.dungeon.dungeon) and
                0 <= new_col < len(self.dungeon.dungeon[0]) and
                abs(new_row - self.mapPosition[0]) <= self.movement_range and
                abs(new_col - self.mapPosition[1]) <= self.movement_range and
                all(monster.mapPosition != [new_row, new_col] for monster in other_monsters) and  # Vérifie les autres monstres
                all(unit.mapPosition != [new_row, new_col] for unit in player_units)   # Vérifie les cases non walkables
            ):
                #print(f"Monster {self.name} moving from {self.mapPosition} to [{new_row}, {new_col}]")
                self.mapPosition = [new_row, new_col]
                break
    def perform_special_attack(self, target):
        #print(f"{self.name} summons a {self.attacks[1]} on {target.mapPosition}!")
        target.take_damage(25)

class OctopusMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Thunder Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.movement_range=2
        self.move_counter=0
        self.attacks = ["Thunder Strike", "Lightning Storm"]
    def load_default_sprites(self):
        """Load default sprite images for general characters."""
        self.spriteFrontLeft = []
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster6_0.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster6_1.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster6_2.png')),(35, 35)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', 'monster6_3.png')),(35, 35)))
        self.spriteFrontRight = []
        self.sprite = self.spriteFrontLeft

    def move_randomly(self, other_monsters, player_units):
        self.move_counter += 1  # Incrémente le compteur à chaque appel

        # Se déplacer uniquement toutes les 20 itérations
        if self.move_counter < 10:
            return  # Ne rien faire si le compteur n'a pas atteint 20

        # Réinitialiser le compteur après déplacement
        self.move_counter = 0

        # Générer un déplacement aléatoire
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        for direction in directions:
            new_row = self.mapPosition[0] + direction[0]
            new_col = self.mapPosition[1] + direction[1]

            # Vérifier les conditions de validité
            if (
                0 <= new_row < len(self.dungeon.dungeon) and
                0 <= new_col < len(self.dungeon.dungeon[0]) and
                abs(new_row - self.mapPosition[0]) <= self.movement_range and
                abs(new_col - self.mapPosition[1]) <= self.movement_range and
                all(monster.mapPosition != [new_row, new_col] for monster in other_monsters) and  # Vérifie les autres monstres
                all(unit.mapPosition != [new_row, new_col] for unit in player_units)   # Vérifie les cases non walkables
            ):
                #print(f"Monster {self.name} moving from {self.mapPosition} to [{new_row}, {new_col}]")
                self.mapPosition = [new_row, new_col]
                break
    def perform_special_attack(self, target):
        #print(f"{self.name} summons a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(40)

def create_monsters(dungeon, media):
    monsters = [
        WaterMonster(dungeon, media, [3,1]),
        OctopusMonster(dungeon, media, [3, 6]),
        FlyMonster(dungeon, media, [3, 10]),
        PoisonMonster(dungeon, media, [4, 4]),
    ]
    return monsters
