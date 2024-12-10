import random
import os
import pygame
from pygame.locals import *
from spriteManager import spriteManager  # 引用父类

# 定义水属性子类
class WaterSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Water Splash", "Tsunami Wave"]  # 普通攻击 + 独特技能

    def perform_special_attack(self, target):
        print(f"{self.name} unleashes a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(40)  # 独特技能造成 40 点伤害


# 定义火属性子类
class FireSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Fireball", "Flame Burst"]

    def perform_special_attack(self, target):
        print(f"{self.name} casts {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(45)  # 独特技能造成 45 点伤害
        target.apply_status_effect("Burn", 3)


# 定义冰属性子类
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


# 定义雷属性子类
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

    # 水属性角色
    characters.append(WaterSprite(dungeon, media, [0, 0], "Aqua Warrior"))
    characters.append(WaterSprite(dungeon, media, [0, 3], "Wave Rider"))

    # 火属性角色
    characters.append(FireSprite(dungeon, media, [5, 0], "Flame Knight"))
    characters.append(FireSprite(dungeon, media, [5, 3], "Blaze Mage"))

    # 冰属性角色
    characters.append(IceSprite(dungeon, media, [10, 0], "Frost Guardian"))
    characters.append(IceSprite(dungeon, media, [10, 3], "Snow Sorcerer"))

    # 雷属性角色
    characters.append(ThunderSprite(dungeon, media, [15, 0], "Storm Hunter"))
    characters.append(ThunderSprite(dungeon, media, [15, 3], "Lightning Avenger"))

    return characters