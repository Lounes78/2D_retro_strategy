



import os
import pygame
from spriteManager import spriteManager

class WaterMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Water Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Water Splash", "Tsunami Wave"]

    def load_default_sprites(self):
        """Load default sprite images for general characters."""
        self.spriteFrontLeft = []
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '0.png')),(30, 30)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '1.png')),(30, 30)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '2.png')),(30, 30)))
        self.spriteFrontLeft.append(pygame.transform.scale(self._media.loadImage(os.path.join('data', 'images', 'monsters', '3.png')),(30, 30)))
        
        self.sprite = self.spriteFrontLeft

    def perform_special_attack(self, target):
        print(f"{self.name} unleashes a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(30)

class FireMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Fire Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
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

    def perform_special_attack(self, target):
        print(f"{self.name} casts {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(35)

class IceMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Ice Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
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

    def perform_special_attack(self, target):
        print(f"{self.name} summons a {self.attacks[1]} on {target.mapPosition}!")
        target.take_damage(25)

class ThunderMonster(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name="Thunder Monster"):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
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


    def perform_special_attack(self, target):
        print(f"{self.name} summons a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(40)

def create_monsters(dungeon, media):
    monsters = [
        WaterMonster(dungeon, media, [3,1]),
        IceMonster(dungeon, media, [3, 6]),
        ThunderMonster(dungeon, media, [3, 10]),
        FireMonster(dungeon, media, [4, 4]),
    ]
    return monsters
