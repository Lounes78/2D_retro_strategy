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
        """Dessine une barre de vie avec un contour, fond gris et couleur dynamique."""
        bar_width = 60
        bar_height = 8
        bar_x = self.healthBarePosition[0]
        bar_y = self.healthBarePosition[1]

        # Calcul du remplissage de la barre
        fill_width = int((self.health / self.max_health) * bar_width)
        
        # Choix de couleur pour la barre de vie selon le niveau
        if self.health / self.max_health > 0.6:
            health_color = (0, 255, 0)  # Vert
        elif self.health / self.max_health > 0.3:
            health_color = (255, 165, 0)  # Orange
        else:
            health_color = (255, 0, 0)  # Rouge

        # Dessine le contour avec des coins arrondis
        pygame.draw.rect(screen, (50, 50, 50), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2), border_radius=4)

        # Dessine le fond de la barre (gris foncé)
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=4)

        # Dessine la barre de vie remplie avec la couleur dynamique
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height), border_radius=4)



        






        # Green for current health



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

        # Menu background with rounded corners
        menu_rect = pygame.Rect(75, 75, 200, 150)  # Smaller dimensions
        menu_surface = pygame.Surface((menu_rect.width, menu_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(menu_surface, (0, 0, 0, 200), menu_surface.get_rect(), border_radius=15)  # Semi-transparent background
        pygame.draw.rect(menu_surface, (255, 255, 255), menu_surface.get_rect(), 2, border_radius=15)  # White border
        screen.blit(menu_surface, (menu_rect.x, menu_rect.y))
        
        # Title for the menu
        title_font = pygame.font.Font(None, 36)
        title_surface = title_font.render("Attack Menu", True, (173, 216, 230))  # Light blue title color
        title_rect = title_surface.get_rect(center=(menu_rect.x + menu_rect.width // 2, menu_rect.y + 20))
        screen.blit(title_surface, title_rect)

        # Menu options
        option_font = pygame.font.Font(None, 28)  # Slightly smaller font for the options
        for i, attack in enumerate(self.attacks):
            is_selected = self.selected_attack == i
            color = (255, 255, 255) if is_selected else (150, 150, 150)
            bg_color = (0, 100, 255) if is_selected else (0, 0, 0, 0)

            # Draw a background rectangle for selected option
            option_rect = pygame.Rect(menu_rect.x + 10, menu_rect.y + 40 + i * 35, menu_rect.width - 20, 30)
            pygame.draw.rect(screen, bg_color, option_rect, border_radius=10)
            
            # Render the text
            text_surface = option_font.render(attack, True, color)
            text_rect = text_surface.get_rect(center=option_rect.center)
            screen.blit(text_surface, text_rect)




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



