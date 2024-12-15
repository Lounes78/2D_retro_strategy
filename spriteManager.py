import os, sys, random
import pygame
from pygame.locals import *

class spriteManager(object):

    def __init__(self, dungeon, media, mapPosition):
        self.menu_open = False
        self.attacks = ["Fireball", "Ice Spike", "Thunder Strike"]
        self.selected_attack = 0
        self.attack_selected = False
        self.cursor_target_position = []
        self.target_position = None

        # key parameters for hero design
        self.status_effects = {}
        self.is_frozen = False  # frozen status
        self.is_burning = False  # burn status
        self.is_paralyze = False # paralyze status
        self.Trigger_paralysis = False # use to check paralyze status
        self.element_type = "Neutral"
        self.defense = False

        self.max_move = 2
        
        self.marked_for_removal = False
        #self.removal_time = None
        #self.marked_for_removal = False
        self.max_health = 100
        self.health = 100
        self.healthBarePosition = [30, 20]
        
        self.dungeon = dungeon
        self._media = media
        self.mapPosition = mapPosition # position of the sprite 
        
        self._tmpAnimateSprite = 0
        self.mapScrollX = 0
        self.mapScrollY = 0
        self.load_default_sprites()

    def load_default_sprites(self):
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
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoTwo.png')))
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoOne.png')))
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoTwo.png')))
        self.spriteBackRight.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoThree.png')))
        #self.spriteFrontLeftWater = []
        #self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterTwo.png')))
        #self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterOne.png')))
        #self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterTwo.png')))
        #self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterThree.png')))
        #self.spriteFrontRightWater = []
        #self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterTwo.png')))
        #self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterOne.png')))
        #self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterTwo.png')))
        #self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterThree.png')))
        #self.spriteBackLeftWater = []
        #self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterTwo.png')))
        #self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterOne.png')))
        #self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterTwo.png')))
        #self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterThree.png')))
        #self.spriteBackRightWater = []
        #self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterTwo.png')))
        #self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterOne.png')))
        #self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterTwo.png')))
        #self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterThree.png')))
        self.sprite = self.spriteFrontLeft
        
    

    
    def update(self, direction):
        """Moves the sprites."""    
        if direction == 1:
            if self.mapPosition[0] > 0 and not self._nextNotWalkable(-1, 0):
                self.mapPosition[0] -= 1
                self.mapScrollY = -1
            if self._isInWater():
                self.sprite = self.spriteBackRightWater
            else:
                self.sprite = self.spriteBackRight
        elif direction == 2:
            if self.mapPosition[0] < len(self.dungeon.dungeon) - 1 and not self._nextNotWalkable(1, 0):
                self.mapPosition[0] += 1
                self.mapScrollY = 1
            if self._isInWater():
                self.sprite = self.spriteFrontLeftWater
            else:
                self.sprite = self.spriteFrontLeft
        elif direction == 3:
            if self.mapPosition[1] > 0 and not self._nextNotWalkable(0, -1):
                self.mapPosition[1] -= 1
                self.mapScrollX = -1
            if self._isInWater():
                self.sprite = self.spriteBackLeftWater
            else:
                self.sprite = self.spriteBackLeft
        elif direction == 4:
            if self.mapPosition[1] < len(self.dungeon.dungeon[0]) - 1 and not self._nextNotWalkable(0, 1):
                self.mapPosition[1] += 1
                self.mapScrollX = 1
            if self._isInWater():
                self.sprite = self.spriteFrontRightWater
            else:
                self.sprite = self.spriteFrontRight

    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 5
        bar_x = self.healthBarePosition[0]
        bar_y = self.healthBarePosition[1]
        fill_width = int((self.health / self.max_health) * bar_width)

        #print(f"this is the bar position: {bar_x, bar_y}")
        # Draw the bar
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red for max health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))
        # Green for current health

    def is_alive(self):
        return self.health > 0

    def is_defeated(self):
        return not(self.is_alive())


    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.marked_for_removal = True
            if not hasattr(self, 'removal_time') or self.removal_time is None:
                self.removal_time = pygame.time.get_ticks()  # 初始化移除时间

    def handle_attacks(self, key_input, screen, attack_position):
        if key_input[K_m]:
            if self.is_frozen :
                print(f"{self.name} is frozen and cannot take actions this turn.")
            elif self.is_paralyze :
                if self.Trigger_paralysis :
                    print(f"{self.name} is paralyzed and cannot take actions this turn.")
                else:
                    print(f"{self.name} resists paralysis and can act this turn!")
                    self.menu_open = not self.menu_open
            else:
                self.menu_open = not self.menu_open
        elif self.menu_open: # choosing the attack
            self.draw_menu(screen)
            if key_input[K_UP] and self.attack_selected == False:
                self.selected_attack = (self.selected_attack - 1)%len(self.attacks)         
            if key_input[K_DOWN] and self.attack_selected == False:
                self.selected_attack = (self.selected_attack + 1)%len(self.attacks)
            elif key_input[K_RETURN] and self.attack_selected == False:

                if self.attacks[self.selected_attack] == "Defense":
                    print(f"{self.name} is defending this turn!")
                    self.defense = True  # 激活防御状态
                    self.menu_open = False  # 关闭菜单
                    return attack_position
                else:
                    self.attack_selected = True

            elif key_input[K_RETURN] and self.attack_selected == True: # ATTACK
                self.attack_selected = False
                self.menu_open = False
                return attack_position
                # attack_position = 
                # Perform the attack
                # self.perform_attack(ennemy_sprite)



    def draw_menu(self, screen):
        if not self.menu_open:
            return 
        # Menu background
        menu_rect = pygame.Rect(50, 50, 200, 150)
        pygame.draw.rect(screen, (0, 0, 0), menu_rect)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 2)
    
        # Menu options
        font = pygame.font.Font(None, 36)
        for i, attack in enumerate(self.attacks):
            color = (255, 255, 255) if self.selected_attack == i else (150, 150, 150)
            text_surface = font.render(attack, True, color)
            screen.blit(text_surface, (menu_rect.x + 10, menu_rect.y + 10 + i*30))



    def perform_attack(self, damage, ennemy_sprite):
        print(f"Launching {self.attacks[self.selected_attack]} at {ennemy_sprite.mapPosition}")
        ennemy_sprite.take_damage(damage)





    def _nextNotWalkable(self, row, col):
        """Checks if next tilde is deep water."""

        if self.dungeon.dungeon[self.mapPosition[0] + row][self.mapPosition[1] + col] in self.dungeon.nwTiles:
            return False
        else:
            return False

    def _isInWater(self):
        """Checks if the character is walking in water."""

        if self.dungeon.dungeon[self.mapPosition[0]][self.mapPosition[1]] == "W":
            return True
        else:
            return False



        """----------------------------------------test-----------------------------------------------"""
    def apply_status_effect(self, effect_name, duration):
        """
        施加一个状态效果。
        :param effect_name: 状态名称，例如 "Frozen", "Burning", "Slowed"
        :param duration: 状态持续的回合数
        """
        self.status_effects[effect_name] = duration
        if effect_name == "Burn":
            self.is_burning = True
        elif effect_name == "Frozen":
            self.is_frozen = True
        elif effect_name == "Paralyze":
            self.is_paralyze = True

    def update_status_effects(self):
        """
        每回合更新状态效果，例如减少持续时间，取消到期的效果。
        """
        expired_effects = []

        for effect, duration in self.status_effects.items():
            if self.status_effects[effect] % 2 == 0 :
                print(f"{self.status_effects[effect]/2} turns remaining, health is {self.health}")
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                print(f"{effect} is expired")
                expired_effects.append(effect)

        for effect in expired_effects:
            print(expired_effects)
            del self.status_effects[effect]
            if effect == "Frozen":
                self.is_frozen = False
            elif effect == "Burn":
                self.is_burning = False
            elif effect == "Paralyze":
                self.is_paralyze = False

        # Persistent damage for burning
        if self.is_burning:
            self.take_damage(10)  # 每回合燃烧扣10点血量
            print(f"{self.name} is burned!")

        # Frozen effect: Cannot move
        if self.is_frozen:
            print(f"{self.name} is frozen at {self.mapPosition}!")

        # Paralyze effect: 50% chance to lose action
        if self.is_paralyze:
            if random.random() < 0.5:  # 50% chance
                print(f"{self.name} is paralyzed and cannot take actions this turn!")
            else:
                print(f"{self.name} resists paralysis and can act this turn!")