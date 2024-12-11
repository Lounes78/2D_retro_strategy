import random
import os
import pygame
from pygame.locals import *
from spriteManager import spriteManager  # 引用父类

# define the son class of water
class WaterSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Water Splash", "Tsunami Wave"]  # 普通攻击 + 独特技能

    def perform_special_attack(self, target):
        print(f"{self.name} unleashes a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(40)  # 独特技能造成 40 点伤害


# define the son class of fire
class FireSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Fireball", "Flame Burst"]

    def perform_special_attack(self, target):
        print(f"{self.name} casts {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(45)  # 独特技能造成 45 点伤害
        target.apply_status_effect("Burn", 3)


# define the son class of ice
class IceSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Ice Spike", "Blizzard"]

    def perform_special_attack(self, target):
        print(f"{self.name} summons a {self.attacks[1]} on {target.mapPosition}!")
        target.take_damage(35)  # 独特技能造成 35 点伤害
        target.apply_status_effect("Frozen", 2)  # 附加冰冻效果

    def freeze(self):
        print(f"{self.name}'s target is frozen and loses their next turn!")


# define the son class of thunder
class ThunderSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Thunder Strike", "Lightning Storm"]

    def perform_special_attack(self, target):
        print(f"{self.name} summons a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(50)  # 独特技能造成 50 点伤害


# 创建角色实例
# 假设已经加载了地牢对象 dungeon 和媒体对象 media

def create_characters(dungeon, media):
    characters = []

    # the heros of first group
    characters.append(WaterSprite(dungeon, media, [0, 0], "Aqua Warrior")) #eau
    characters.append(FireSprite(dungeon, media, [0, 2], "Flame Knight")) #feu
    characters.append(IceSprite(dungeon, media, [0, 4], "Frost Guardian")) #ice
    characters.append(ThunderSprite(dungeon, media, [0, 6], "Storm Hunter")) #thunder

    # the heros in the second group
    characters.append(WaterSprite(dungeon, media, [20, 0], "Wave Rider"))
    characters.append(FireSprite(dungeon, media, [20, 2], "Blaze Mage"))
    characters.append(IceSprite(dungeon, media, [20, 4], "Snow Sorcerer"))
    characters.append(ThunderSprite(dungeon, media, [20, 6], "Lightning Avenger"))

    return characters
