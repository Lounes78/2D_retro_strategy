import random
import os
import pygame
from pygame.locals import *
from Type_Effectiveness import calculate_damage_and_effect
from spriteManager import spriteManager  # 引用父类

# define the son class of water
class WaterSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Water Splash", "Tsunami Wave"]
        self.element_type = "Water"

    def perform_special_attack(self, target):
        print(f"{self.name} unleashes a {self.attacks[1]} at {target.mapPosition}!")
        target.take_damage(40)  # 独特技能造成 40 点伤害

        if self.attacks[self.selected_attack] == "Water Splash":
            base_damage = 20
        elif self.attacks[self.selected_attack] == "Tsunami Wave":
            base_damage = 30

        # Calculate damage and effects
        damage, burn, freeze, paralyze = calculate_damage_and_effect(self, target, base_damage)

        # Apply damage or healing
        if damage < 0:
            target.health -= damage
            print(f"{target.name} heals for {-damage} HP!")
        else:
            target.take_damage(damage)

# define the son class of fire
class FireSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Fireball", "Flame Burst"]
        self.element_type = "Fire"

    def perform_special_attack(self, target):
        print(f"{self.name} casts {self.attacks[self.selected_attack]} at {target.mapPosition}!")

        # Set base damage value and initial burn duration based on skill type
        if self.attacks[self.selected_attack] == "Fireball":
            base_damage = 20
            base_burn_duration = 1
        elif self.attacks[self.selected_attack] == "Flame Burst":
            base_damage = 10
            base_burn_duration = 3

        # Calculate damage and effects
        damage, burn_turn, freeze_turn, paralyze_turn = calculate_damage_and_effect(self, target, base_damage, burn=base_burn_duration)

        # Apply damage or healing
        if damage < 0:
            target.health -= damage
            print(f"{target.name} heals for {-damage} HP!")
        else:
            target.take_damage(damage)

        # Apply status effects
        if burn_turn > 0:
            target.apply_status_effect("Burn", burn_turn)
        """if freeze > 0:
            target.apply_status_effect("Frozen", freeze)
        if paralyze > 0:
            target.apply_status_effect("Paralyzed", paralyze)"""


# define the son class of ice
class IceSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Ice Spike", "Blizzard"]
        self.element_type = "Ice"


    def perform_special_attack(self, target):
        print(f"{self.name} summons a {self.selected_attack} on {target.mapPosition}!")

        # Set base damage value and initial burn duration based on skill type
        if self.attacks[self.selected_attack] == "Ice Spike":
            base_damage = 20
            base_frozen_duration = 1
        elif self.attacks[self.selected_attack] == "Blizzard":
            base_damage = 10
            base_frozen_duration = 3

        # Calculate damage and effects
        damage, burn_turn, freeze_turn, paralyze_turn = calculate_damage_and_effect(self, target, base_damage, freeze=base_frozen_duration)

        # Apply damage or healing
        if damage < 0:
            target.health -= damage
            print(f"{target.name} heals for {-damage} HP!")
        else:
            target.take_damage(damage)

        # Apply status effects
        if freeze_turn > 0:
            target.apply_status_effect("Frozen", freeze_turn)

    def freeze(self):
        print(f"{self.name}'s target is frozen and loses their next turn!")


# define the son class of thunder
class ThunderSprite(spriteManager):
    def __init__(self, dungeon, media, mapPosition, name):
        super().__init__(dungeon, media, mapPosition)
        self.name = name
        self.attacks = ["Thunder Strike", "Lightning Storm"]
        self.element_type = "Thunder"


    def perform_special_attack(self, target):
        print(f"{self.name} summons a {self.selected_attack} at {target.mapPosition}!")

        # Set base damage value and initial burn duration based on skill type
        if self.attacks[self.selected_attack] == "Thunder Strike":
            base_damage = 20
            base_paralyze_duration = 1 # 1 turn
        elif self.attacks[self.selected_attack] == "Lightning Storm":
            base_damage = 10
            base_paralyze_duration = 3  # 3 turn

        # Calculate damage and effects
        damage, burn_turn, freeze_turn, paralyze_turn = calculate_damage_and_effect(self, target, base_damage, paralyze=base_paralyze_duration)

        # Apply damage or healing
        if damage < 0:
            target.health -= damage
            print(f"{target.name} heals for {-damage} HP!")
        else:
            target.take_damage(damage)

        # Apply status effects
        if paralyze_turn > 0:
            target.apply_status_effect("Paralyze", paralyze_turn)


# Create character instances

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
