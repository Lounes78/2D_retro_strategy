import os, sys, random
import pygame
from pygame.locals import *

from ExplostionManager import Explosion
explosion_group = pygame.sprite.Group()

class spriteManager(object):

    def __init__(self, dungeon, media, mapPosition):
        self.max_move = 2
        self.menu_open = False
        self.attacks = ["Fireball", "Ice Spike", "Thunder Strike"]
        self.selected_attack = 0
        self.attack_selected = False
        self.cursor_target_position = []
        self.target_position = None
        
        self.max_health = 100
        self.health = 100
        self.healthBarePosition = [30, 20]
        
        self.dungeon = dungeon
        self._media = media
        self.mapPosition = mapPosition # position of the sprite 

        self.status_effects = {}

        self._tmpAnimateSprite = 0
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
        self.spriteFrontLeftWater = []
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterTwo.png')))
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterOne.png')))
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterTwo.png')))
        self.spriteFrontLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoWaterThree.png')))
        self.spriteFrontRightWater = []
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterTwo.png')))
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterOne.png')))
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterTwo.png')))
        self.spriteFrontRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'frontRightDrackoWaterThree.png')))
        self.spriteBackLeftWater = []
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterTwo.png')))
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterOne.png')))
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterTwo.png')))
        self.spriteBackLeftWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backLeftDrackoWaterThree.png')))
        self.spriteBackRightWater = []
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterTwo.png')))
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterOne.png')))
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterTwo.png')))
        self.spriteBackRightWater.append(self._media.loadImage(os.path.join('data', 'images', 'character', 'backRightDrackoWaterThree.png')))
        self.sprite = self.spriteFrontLeft
        self.mapScrollX = 0
        self.mapScrollY = 0
    
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
        bar_y = self.healthBarePosition[1] - 10
        fill_width = int((self.health / self.max_health) * bar_width)

        # Draw the bar
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red for max health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))  # Green for current health
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_alive(self):
        return self.health > 0


    def is_defeated(self):
        return not(self.is_alive())



    def handle_attacks(self, key_input, screen, attack_position):
        if key_input[K_m]:
            self.menu_open = not self.menu_open
        elif self.menu_open: # choosing the attack
            self.draw_menu(screen)
            if key_input[K_UP] and self.attack_selected == False:
                self.selected_attack = (self.selected_attack - 1)%len(self.attacks)         
            if key_input[K_DOWN] and self.attack_selected == False:
                self.selected_attack = (self.selected_attack + 1)%len(self.attacks)
            elif key_input[K_RETURN] and self.attack_selected == False:
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



    def perform_attack(self, damage, ennemy_sprite, screen):
        print(f"Launching {self.attacks[self.selected_attack]} at {ennemy_sprite.mapPosition}")
        ennemy_sprite.take_damage(damage)

        stepX = 0
        stepY = 150
        rewinderStepX = 0
        rewinderStepY = 150
        patch = 30

        target_row, target_col = ennemy_sprite.mapPosition

        centeredItemX = 400 

        row, col = ennemy_sprite.dungeon._rowTmp, ennemy_sprite.dungeon._colTmp

        # Traverse the dungeon to compute stepX and stepY for the target position
        while True:
            if [col, row] == [target_row, target_col]:
                break

            # Move to the next tile in the row
            stepX += 19
            stepY += 10
            row += 1

            # Check if the end of the row or screen width is reached
            if centeredItemX + stepX >= 800 - patch or row >= len(ennemy_sprite.dungeon.dungeon[col]):
                patch += 19
                row = ennemy_sprite.dungeon._rowTmp
                col += 1
                rewinderStepX -= 19
                stepX = rewinderStepX
                rewinderStepY += 10
                stepY = rewinderStepY

            if centeredItemX + stepX <= 0 or col >= len(ennemy_sprite.dungeon.dungeon):
                raise ValueError("Target position is out of bounds in the dungeon!")

        x = centeredItemX + stepX + 18
        y = stepY - 50 - int(ennemy_sprite.dungeon.elevation[target_row][target_col]) * 20

        explosion_group.add(Explosion(x, y))
        explosion_group.draw(screen)
        explosion_group.update()
        # remove the explosion after being displayed
        explosion_group.empty()



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




    """test for adding the debuff status"""

    def     apply_status_effect(self, effect_name, duration):
        """应用状态效果"""
        self.status_effects[effect_name] = duration
        print(f"{self} is affected by {effect_name} for {duration} turns!")

    def update_status_effects(self):
        """更新所有状态效果的持续时间"""
        expired_effects = []
        for effect, duration in self.status_effects.items():
            # 根据效果处理逻辑
            if effect == "Burn":  # 灼烧：每回合扣血
                self.take_damage(5)
                print(f"{self} suffers 5 damage from Burn!")
            elif effect == "Poison":  # 中毒：持续伤害
                self.take_damage(3)
                print(f"{self} suffers 3 damage from Poison!")
            elif effect == "Frozen":  # 冻结：限制行动
                print(f"{self} is frozen and cannot move this turn!")
            elif effect == "Paralysis":  # 麻痹：随机无法行动
                if random.choice([True, False]):
                    print(f"{self} is paralyzed and skips this turn!")

            # 更新持续时间
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                expired_effects.append(effect)
            # 移除过期的效果
        for effect in expired_effects:
            del self.status_effects[effect]
            print(f"{self} is no longer affected by {effect}!")

    def has_effect(self, effect_name):
        """检查是否有特定效果"""
        return effect_name in self.status_effects
