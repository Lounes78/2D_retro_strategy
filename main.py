import os
import sys
import pygame
from pygame.locals import *

from mediaManager import *
from windowManager import *
from dungeonManager import *
from spriteManager import *





current_turn = 0  # 0 for player 1 and 1 for player 2


class Player():
    def __init__(self, name, sprite_managers):
        self.name = name
        self.played = False
        self.sprite_managers = sprite_managers if sprite_managers else []  # List of unit sprite managers
        self.is_active = False # False by default
    
    def take_turn(self, action, unit_index=0):
        if unit_index < len(self.sprite_managers):  # Ensure the unit exists
            self.played = True
            if action == 1:  # Move up
                self.sprite_managers[unit_index].update(1)
            elif action == 2:  # Move down
                self.sprite_managers[unit_index].update(2)
            elif action == 3:  # Move left
                self.sprite_managers[unit_index].update(3)
            elif action == 4:  # Move right
                self.sprite_managers[unit_index].update(4)
    
    
    def set_active(self, active):
        self.is_active = active
        
    def is_turn(self): # checks if it is the player turn
        return self.is_active

    def get_units_positions(self):
        return [sprite_manager.mapPosition for sprite_manager in self.sprite_managers] 
        
        

class Game:
    """Class representing the main game."""

    def __init__(self):
        pygame.init()
        self.target_position = []
        self.menu_open = False
        self.screen = pygame.display.set_mode((800, 600))
        self.media = loadMedia()
        

        self.window_manager = windowManager(self.screen)
        self.background = self.media.loadImage(os.path.join('data', 'images', 'background', 'firstDungeon.png'))
        self.logo = [
            self.media.loadImage(os.path.join('data', 'logo', f'titleLess{num}.png'))
            for num in ["One", "Two", "Three"]
        ]
        self.character_into = [
            self.media.loadImage(os.path.join('data', 'images', 'character', f'frontLeftDracko{num}.png'))
            for num in ["One", "two", "Three"]
        ]
        self.font = pygame.font.SysFont("Courier New", 15).render(
            "Press Enter to continue or Esc to Exit.", True, (255, 255, 255)
        )
        self.sound = self.media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_no_survivors_.mid'))
        self.sound.music.play(-1)
        self.dummy_counter = 0
        self.sprite_counter = 0
        self.dracko = None
        self.second_character = None
        self.dungeon_manager = None
        self.active_player = None  # Variable to track the active player
        self.init_positions()

    def init_positions(self):
        """Initializes positions for logos, characters, and fonts."""
        self.centered_logo_x = self.window_manager.centerItemX(self.logo[self.sprite_counter])
        self.centered_logo_y = self.window_manager.centerItemY(self.logo[self.sprite_counter])
        self.centered_character_x = (
            self.window_manager.centerItemX(self.character_into[self.sprite_counter])
            + self.logo[self.sprite_counter].get_width() / 2 - 10
        )
        self.centered_character_y = (
            self.window_manager.centerItemY(self.character_into[self.sprite_counter])
            + self.logo[self.sprite_counter].get_height() / 2 - 30
        )
        self.center_font_x = self.window_manager.centerItemX(self.font)
        self.center_font_y = (
            self.window_manager.centerItemY(self.font)
            + self.window_manager.centerItemX(self.logo[self.sprite_counter]) / 4
        )

    def run_hello_screen(self):
        """Displays the hello screen."""
        while True:
            pygame.event.pump()
            key_input = pygame.key.get_pressed()
            self.screen.blit(self.background, (0, 0))
            self.dummy_counter += 1

            flag = self.update_sprite_counter()
            if flag:
                self.screen.blit(self.logo[self.sprite_counter], (self.centered_logo_x, self.centered_logo_y))
                self.screen.blit(self.character_into[self.sprite_counter],
                                 (self.centered_character_x, self.centered_character_y))
                self.screen.blit(self.font, (self.center_font_x, self.center_font_y))
                pygame.display.update()

            if key_input[K_RETURN]:
                break
            elif key_input[K_ESCAPE] or pygame.event.peek(QUIT):
                sys.exit()

    def update_sprite_counter(self):
        """Updates the sprite counter based on dummy_counter."""
        flag = False
        if self.dummy_counter < 300 and self.sprite_counter != 0:
            self.sprite_counter = 0
            flag = True
        elif 300 <= self.dummy_counter < 600 and self.sprite_counter != 1:
            self.sprite_counter = 1
            flag = True
        elif 600 <= self.dummy_counter < 900 and self.sprite_counter != 2:
            self.sprite_counter = 2
            flag = True
        elif 900 <= self.dummy_counter < 1200 and self.sprite_counter != 1:
            self.sprite_counter = 1
            flag = True
        elif self.dummy_counter >= 1200:
            self.dummy_counter = 0
        return flag



    def load_game(self):
        """Loads the game after the hello screen."""
        pygame.time.delay(500)
        self.sound.music.stop()
        self.sound = self.media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_the_long_journey_home.mid'))
        #self.sound.music.play(-1)

        tilde_file = self.media.loadReadFile(os.path.join('data', 'maps', 'tiles.txt'))
        dungeon_file = self.media.loadReadFile(os.path.join('data', 'maps', 'firstDungeon.txt'))
        nw_tiles = self.media.loadReadFile(os.path.join('data', 'maps', 'tiles.txt'))

        self.dungeon_manager = dungeonManager(self.media, self.window_manager, self.screen)
        self.dungeon_manager.recordNonWalkableTiles(nw_tiles)
        self.dungeon_manager.recordTiles(tilde_file)
        self.dungeon_manager.recordDungeon(dungeon_file)
        self.screen.blit(self.background, (0, 0))

        # Create units for each player with unique media instances
        dracko_units = [spriteManager(self.dungeon_manager, self.media, [0, 3 * i]) for i in range(4)]
        second_character_units = [spriteManager(self.dungeon_manager, self.media, [10, 3 * i]) for i in range(4)]


        # Initialize players with their respective units
        self.dracko_player = Player("Dracko", dracko_units)
        self.second_player = Player("Second Player", second_character_units)

        # highlighted target position
        self.target_position_sprite = spriteManager(self.dungeon_manager, self.media, [0, 0])
        pygame.display.update()



    def run_game_loop(self):
        """Runs the main game loop."""
        # Start with Dracko's turn
        players = [self.dracko_player, self.second_player]
        active_player_index = 0
        players[active_player_index].set_active(True)

        attack_animation_playing = False
        attack_animation_position = None
        attack_animation_type = None

        self.fireball_group = pygame.sprite.Group()

        current_unit_index = 0
        last_turn_switch_time = 0  # Timestamp for the last turn switch
        switch_cooldown = 700  # Cooldown in milliseconds for switching turns

        while True:
            pygame.event.pump() # updating the events queue from the os
            key_input = pygame.key.get_pressed()

            # Get the current time
            current_time = pygame.time.get_ticks()

            # Handle unit switching within the active player
            if key_input[K_TAB]:
                current_unit_index = (current_unit_index + 1) % len(players[active_player_index].sprite_managers)

                self.poll_events_with_timeout(20)  # Short delay for unit switching, interruptible

            # Handle turn switching with cooldown
            if (
                (players[active_player_index].is_turn
                and players[active_player_index].played
                and current_time - last_turn_switch_time > switch_cooldown)
                or (players[active_player_index].played)
            ):
                players[active_player_index].played = False
                players[active_player_index].set_active(False)
                active_player_index = (active_player_index + 1) % len(players)
                players[active_player_index].set_active(True)
                last_turn_switch_time = current_time  # Update the timestamp

            if current_unit_index >=len(players[active_player_index].sprite_managers):
                current_unit_index = 0
            active_unit = players[active_player_index].sprite_managers[current_unit_index]
            unit_position = active_unit.mapPosition
            #unit_position = players[active_player_index].sprite_managers[current_unit_index].mapPosition


            # Process movement only for the active player
            self.menu_open = active_unit.menu_open


            if not self.menu_open:
                if players[active_player_index].is_turn():
                    if key_input[K_UP]:
                        players[active_player_index].take_turn(1, current_unit_index)
                    elif key_input[K_DOWN]:
                        players[active_player_index].take_turn(2, current_unit_index)
                    elif key_input[K_LEFT]:
                        players[active_player_index].take_turn(3, current_unit_index)
                    elif key_input[K_RIGHT]:
                        players[active_player_index].take_turn(4, current_unit_index)
                self.target_position_sprite.mapPosition = [active_unit.mapPosition[0], active_unit.mapPosition[1]]

            # Update the game screen
            self.screen.blit(self.background, (0, 0))


            if active_unit.attack_selected:
                if key_input[K_UP]:
                    self.target_position_sprite.update(1)
                elif key_input[K_DOWN]:
                    self.target_position_sprite.update(2)
                elif key_input[K_LEFT]:
                    self.target_position_sprite.update(3)
                elif key_input[K_RIGHT]:
                    self.target_position_sprite.update(4)
                unit_position = self.target_position_sprite.mapPosition



            attack_position = active_unit.handle_attacks(key_input, self.screen, self.target_position_sprite.mapPosition)
            #print(active_unit.selected_attack)
            selected_attack = active_unit.attacks[active_unit.selected_attack]
            #print(selected_attack)
            # find the ennemy and attack it
            if attack_position != None:
                for enemy_sprite in players[not(active_player_index)].sprite_managers:
                    if enemy_sprite.mapPosition == attack_position:
                        print(f"this is the {attack_position}")

                        damage = 30 # par exemple
                        #attack_animation.play(
                         #   attack_type=active_unit.attacks[active_unit.selected_attack],
                         #   start_position=active_unit.mapPosition,
                           # target_position=attack_position,
                           # tile_width=50,  # Adapter à la taille de tes tuiles
                          #  tile_height=50
                        #)
                        #image = self.media.loadImage(os.path.join('data', 'images', 'effects', 'thunder.png'))
                        #self.dungeon_manager.play(selected_attack, attack_position)
                        attack_animation_playing = True
                        attack_animation_position = attack_position
                        attack_animation_type = selected_attack
                        attack_animation_start_position = active_unit.mapPosition
                        active_unit.perform_attack(damage, enemy_sprite)

                        if enemy_sprite.is_defeated():
                            players[1 - active_player_index].sprite_managers.remove(enemy_sprite)
                            #if current_unit_index >= len(players[active_player_index].sprite_managers):
                                #current_unit_index = 0
                            #if len(players[1 - active_player_index].sprite_managers) == 0:
                                #print(f"{players[active_player_index].name} wins!")
                                #sys.exit()

                        #change the player once attacked
                        players[active_player_index].played = False
                        players[active_player_index].set_active(False)
                        active_player_index = (active_player_index + 1) % len(players)
                        players[active_player_index].set_active(True)
                        last_turn_switch_time = current_time


            #print(unit_position)
            #print(active_unit.attack_selected) # true or false selon si on a activé un attaque,true quand mon bouge la highlighted tile
            self.dungeon_manager.fillDungeon_tiles(unit_position, active_unit.attack_selected,selected_attack)
            # Updates the units
            for player in players:
                for sprite in player.sprite_managers:
                    sprite.dungeon.fillDungeon_sprites(sprite, sprite == active_unit, self.screen)

            if attack_animation_playing:
                if attack_animation_type == "Thunder Strike":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position)
                elif attack_animation_type == "Fireball":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position,
                                              start_position=attack_animation_start_position)
                attack_animation_playing = False

            self.dungeon_manager.fireball_group.update()
            self.dungeon_manager.fireball_group.draw(self.screen)

            if key_input[K_ESCAPE] or pygame.event.peek(QUIT):
                sys.exit()
            #cloud_positions = [[3, 4]  # Example: positions of clouds
            #cloud_position = [0, 1]  # Logical position of the cloud
            #cloud_image = self.media.loadImage(os.path.join('data', 'images', 'character', 'back-left-dracko.png'))
            #cloud_image_resized = pygame.transform.scale(cloud_image, (300, 100))  # Resize to tile size

            # Draw the cloud

            #self.dungeon_manager.draw_cloud(self.screen, cloud_position, cloud_image)

            # Cloud image

            # Call the method to draw the cloud
            #self.dungeon_manager.draw_cloud(self.screen, cloud_position, cloud_image)

            pygame.display.update()
            #self.dungeon_manager.fillDungeon_effects(cloud_position, cloud_image)

            self.poll_events_with_timeout(185)  # General delay, interruptible



    def poll_events_with_timeout(self, timeout):
        """Polls for events during a timeout and breaks if a key is pressed."""
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < timeout:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    return  # Stop delay if a key is pressed or quit event is detected
            pygame.time.wait(1)  # Small wait to avoid busy-waiting




if __name__ == "__main__":
    game = Game()
    game.run_hello_screen()
    game.load_game()
    game.run_game_loop()
