import os
import sys
import pygame
from pygame.locals import *
from monsters import *
from mediaManager import *
from windowManager import *
from dungeonManager import *
from spriteManager import *
from HerosGenerator import *
from utils import *


current_turn = 0  # 0 for player 1 and 1 for player 2



class Player():
    def __init__(self, name, sprite_managers):
        self.number_of_moves = 1
        self.name = name
        self.played = 0 # False
        self.sprite_managers = sprite_managers if sprite_managers else []  # List of unit sprite managers
        self.is_active = False
        self.score = 0
    def take_turn(self, action, unit_index, highlighted_positions, active_unit_mapPosition):
        if unit_index < len(self.sprite_managers):
            if action == 0: 
                self.number_of_moves = 0
                self.played = 1 # True
            else:
                self.played = 2 # Val intermediaire Z

            self.number_of_moves += 1
            if action == 1:  # Move up
                self.sprite_managers[unit_index].update(1)
            elif action == 2:  # Move down
                self.sprite_managers[unit_index].update(2)
            elif action == 3:  # Move left
                self.sprite_managers[unit_index].update(3)
            elif action == 4:  # Move right
                self.sprite_managers[unit_index].update(4)
                
            if tuple(active_unit_mapPosition) not in highlighted_positions:
                if action == 1:  # Move up
                    self.sprite_managers[unit_index].update(2)
                elif action == 2:  # Move down
                    self.sprite_managers[unit_index].update(1)
                elif action == 3:  # Move left
                    self.sprite_managers[unit_index].update(4)
                elif action == 4:  # Move right
                    self.sprite_managers[unit_index].update(3)
    

    def set_active(self, active):
        self.is_active = active

    def is_turn(self):  # checks if it is the player turn
        return self.is_active

    def get_units_positions(self):
        return [sprite_manager.mapPosition for sprite_manager in self.sprite_managers]


class Game:
    """Class representing the main game."""

    def __init__(self):
        pygame.init()
        # self.highlighted_positions = set()
        self.n_winning_units = 0
        self.add_zone = False # Check if we should add a zone
        self.already_occupied = []
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
        self.monsters=[]
        self.init_positions()

    def display_scores(self):
        """Affiche les scores de chaque joueur à l'écran avec un design amélioré."""
        font = pygame.font.SysFont("Courier New", 22, bold=True)
        
        # Semi-transparent background panel for the scores
        panel_width, panel_height = 250, 70
        score_panel_rect = pygame.Rect(540, 0, panel_width, panel_height)
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 30))  # Black with transparency (180 alpha)
        self.screen.blit(panel_surface, (score_panel_rect.x, score_panel_rect.y))
        
        # Border for the panel
        pygame.draw.rect(self.screen, (200, 200, 200), score_panel_rect, 2)  # Light gray border
        
        # Score du joueur 1
        player1_score_text = f"{self.dracko_player.name}: {self.dracko_player.score}"
        player1_surface = font.render(player1_score_text, True, (135, 206, 250))  # Sky blue
        player1_rect = player1_surface.get_rect(topleft=(score_panel_rect.x + 15, score_panel_rect.y + 10))
        self.screen.blit(player1_surface, player1_rect)
        
        # Score du joueur 2
        player2_score_text = f"{self.second_player.name}: {self.second_player.score}"
        player2_surface = font.render(player2_score_text, True, (255, 160, 122))  # Light salmon
        player2_rect = player2_surface.get_rect(topleft=(score_panel_rect.x + 15, player1_rect.bottom + 5))
        self.screen.blit(player2_surface, player2_rect)



 # En dessous du score du joueur 1

    def show_image_with_effects(self, image_path, duration=2000, message="Start to Dominate"):
        """
        Displays an image with a black transparent background, shaking effect, and a message for a specified duration.

        :param image_path: Path to the image file.
        :param duration: Duration to display the image (in milliseconds).
        :param message: Text to display on the screen.
        """
        # Load the image
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (300, 300))  # Resize the image
        image_rect = image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Create a semi-transparent black background
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 

        # Get the start time
        start_time = pygame.time.get_ticks()

        # Font for the message
        font = pygame.font.Font(None, 50)  # Adjust font size
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 150))

        # Shaking parameters
        shake_amplitude = 5
        shake_frequency = 100  
        # Shake every 100ms

        while True:
            current_time = pygame.time.get_ticks()
            if current_time - start_time > duration:
                break  # Exit after the duration

            # Handle shaking
            shake_offset_x = shake_amplitude if (current_time // shake_frequency) % 2 == 0 else -shake_amplitude
            shake_offset_y = shake_amplitude if (current_time // shake_frequency) % 2 == 0 else -shake_amplitude

            # Draw the transparent background
            self.screen.blit(self.background, (0, 0))  # Draw the game background
            self.screen.blit(overlay, (0, 0))  # Draw the black transparent overlay

            # Draw the image with shaking effect
            self.screen.blit(image, (image_rect.x + shake_offset_x, image_rect.y + shake_offset_y))

            # Draw the message
            self.screen.blit(text_surface, text_rect)

            pygame.display.update()  # Update the display

            # Process events to avoid "Not Responding" issues
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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

            #self.dummy_counter += 1

   
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
        # self.sound.music.play(-1)
        
        # Initial version of the map
        self.file_path = "data/maps/firstDungeon.txt"
        self.flag_initial_position = (5, 7)
        self.already_occupied.append(self.flag_initial_position)
        self.map = update_map(self.file_path, None, 'N', self.flag_initial_position, [], distance=2)
        tilde_file = self.media.loadReadFile(os.path.join('data', 'maps', 'tiles.txt'))
        # dungeon_file = self.media.loadReadFile(os.path.join('data', 'maps', 'firstDungeon.txt'))
        nw_tiles = self.media.loadReadFile(os.path.join('data', 'maps', 'tiles.txt'))
        #self.init_monsters()
        self.dungeon_manager = dungeonManager(self.media, self.window_manager, self.screen)
        self.dungeon_manager.recordNonWalkableTiles(nw_tiles)
        self.dungeon_manager.recordTiles(tilde_file)
        self.dungeon_manager.recordDungeon(self.map)
        self.screen.blit(self.background, (0, 0))
        #init monsters
        self.monsters = create_monsters(self.dungeon_manager, self.media)
        #init units
        all_characters = create_characters(self.dungeon_manager, self.media)
        # Player 1 gets the first 4 characters
        dracko_units = all_characters[:4]
        # Player 2 gets the next 4 characters
        second_character_units = all_characters[4:]
        """-----------------------------------------------------------------"""
        self.all_sprites = all_characters  # 玩家单位 + 怪物单位(未实装)
        print("All sprites:", self.all_sprites)

        # Initialize players with their respective units
        self.dracko_player = Player("Dracko", dracko_units)
        self.second_player = Player("Second Player", second_character_units)

        # highlighted target position
        self.target_position_sprite = spriteManager(self.dungeon_manager, self.media, [0, 0])
        
        pygame.display.update()
        
        
        
        
    def handle_zone(self, players, new_zone_position=None):        
        # Updating the map if necessary
        if self.add_zone == True:
            self.add_zone = False
            if new_zone_position is not None and new_zone_position not in self.already_occupied:
                self.map = update_map(self.file_path, self.map, 'N', new_zone_position, self.already_occupied, distance=2)
                self.dungeon_manager.recordDungeon(self.map)
                self.already_occupied.append(new_zone_position)

        for zone_position in self.already_occupied:
            zone_x, zone_y = zone_position
            flag1 = False
            flag2 = False
            
            for player in players:
                for unit in player.sprite_managers:
                    unit_x, unit_y = unit.mapPosition
            
                    if player.name == "Dracko":
                        distance_x = abs(unit_x - zone_x)
                        distance_y = abs(unit_y - zone_y)
                        # if flag1 == False:
                        flag1 = flag1 or distance_x <= 2 and distance_y <= 2
                        
                    
                    elif player.name == "Second Player":
                        distance_x = abs(unit_x - zone_x)
                        distance_y = abs(unit_y - zone_y)
                        # if flag2 == False:
                        flag2 = flag2 or distance_x <= 2 and distance_y <= 2
            
            # print(flag1, flag2)
            if flag1 == flag2: # Give the correct color to the zone and start / restart the score
                updated_map = update_map(self.file_path, self.map, 'N', zone_position, self.already_occupied, distance=2)
                self.dungeon_manager.recordDungeon(self.map)
                if flag1 and flag2: # Both players are close to the zone so MINUS 1 point for each at each iteration
                    for player in players:
                        player.score -= 1
            elif flag1:
                updated_map = update_map(self.file_path, self.map, 'L', zone_position, self.already_occupied, distance=2)
                self.dungeon_manager.recordDungeon(self.map)
                players[0].score += 5
                # return 1
            elif flag2: 
                updated_map = update_map(self.file_path, self.map, 'Q', zone_position, self.already_occupied, distance=2)
                players[1].score += 5

            self.map = updated_map
            self.dungeon_manager.recordDungeon(self.map)

                # return 2
        # print("\n")
        # print(f"unit {unit_x, unit_y} is close to zone {zone_x, zone_y}")







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
        self.tsunami_group = pygame.sprite.Group()
        self.flame_burst_group = pygame.sprite.Group()
        self.ice_spike_group = pygame.sprite.Group()
        self.blizzard_group = pygame.sprite.Group()
        self.light_storm_group = pygame.sprite.Group()
        current_unit_index = 0
        last_turn_switch_time = 0  # Timestamp for the last turn switch
        switch_cooldown = 700
        # Cooldown in milliseconds for switching turns


        highlighted_positions = set()
        
        new_zone_position = None
        
        while True:




            pygame.event.pump()  # updating the events queue from the os
            key_input = pygame.key.get_pressed()

            current_time = pygame.time.get_ticks()
            # print(current_time)



            # Handle zone things
            score_to_add_new_zone = 200
            if players[0].score >= score_to_add_new_zone or players[1].score >= score_to_add_new_zone:
                self.add_zone = True
                new_zone_position = (15, 14)
            self.handle_zone(players, new_zone_position)




            # Handle unit switching within the active player
            if key_input[K_TAB]:
                current_unit_index = (current_unit_index + 1) % len(players[active_player_index].sprite_managers)

                self.poll_events_with_timeout(20)  # Short delay for unit switching, interruptible

            # Handle turn switching with cooldown
            if (
                (players[active_player_index].is_turn
                and players[active_player_index].played == 1
                and current_time - last_turn_switch_time > switch_cooldown)
                or (players[active_player_index].played == 1)
            ):
                players[active_player_index].played = 0
                players[active_player_index].set_active(False)

                """-----------------------------"""
                for sprite in players[active_player_index].sprite_managers:
                    sprite.update_status_effects()

                active_player_index = (active_player_index + 1) % len(players)
                players[active_player_index].set_active(True)
                last_turn_switch_time = current_time  # Update the timestamp

            if current_unit_index >= len(players[active_player_index].sprite_managers):
                current_unit_index = 0
            active_unit = players[active_player_index].sprite_managers[current_unit_index]
            unit_position = active_unit.mapPosition
            # unit_position = players[active_player_index].sprite_managers[current_unit_index].mapPosition

            # Process movement only for the active player
            # Flag to store paralysis check result for the current turn
            if not hasattr(active_unit, "paralyze_checked"):
                active_unit.paralyze_checked = False
                active_unit.Trigger_paralysis = False

            if active_unit.is_paralyze and not active_unit.paralyze_checked:
                # Perform paralysis check once per turn
                active_unit.paralyze_checked = True
                if random.random() < 0.5:  # 50% chance
                    active_unit.Trigger_paralysis = True
                    print(f"{active_unit.name} is paralyzed and cannot take actions this turn.")
                else:
                    active_unit.Trigger_paralysis = False
                    print(f"{active_unit.name} resists paralysis and can act this turn!")
            self.menu_open = active_unit.menu_open # mode menu ou pas recuperer des que je clique sur m ca devient True
            # print(f"menu{active_unit.menu_open}")
            if not self.menu_open:
                if players[active_player_index].is_turn() :

                    if not active_unit.Trigger_paralysis:
                        if key_input[K_UP]:
                            if active_unit.is_frozen :
                                print(f"{active_unit.name} is frozen and cannot take actions this turn.")
                            else:
                                players[active_player_index].take_turn(1, current_unit_index, highlighted_positions, active_unit.mapPosition)
                        elif key_input[K_DOWN]:
                            if active_unit.is_frozen :
                                print(f"{active_unit.name} is frozen and cannot take actions this turn.")
                            else :
                                players[active_player_index].take_turn(2, current_unit_index, highlighted_positions, active_unit.mapPosition)
                        elif key_input[K_LEFT]:
                            if active_unit.is_frozen :
                                print(f"{active_unit.name} is frozen and cannot take actions this turn.")
                            else:
                                players[active_player_index].take_turn(3, current_unit_index, highlighted_positions, active_unit.mapPosition)
                        elif key_input[K_RIGHT]:
                            if active_unit.is_frozen :
                                print(f"{active_unit.name} is frozen and cannot take actions this turn.")
                            else:
                                players[active_player_index].take_turn(4, current_unit_index, highlighted_positions, active_unit.mapPosition)
                        elif key_input[K_SPACE]:
                            if active_unit.is_frozen :
                                print(f"{active_unit.name} is frozen and cannot take actions this turn.")
                            else :
                                players[active_player_index].take_turn(0, current_unit_index, highlighted_positions, active_unit.mapPosition)
                            for enemy_sprite in players[not (active_player_index)].sprite_managers:
                                enemy_sprite.defense = False
                """else:
                    print(f"{active_unit.name} is frozen and cannot take actions this turn.")"""
                self.target_position_sprite.mapPosition = [active_unit.mapPosition[0], active_unit.mapPosition[1]]

            # Update the game screen
            self.screen.blit(self.background, (0, 0))
            #for monster in self.monsters:
                #monster.draw(self.screen)

            if active_unit.attack_selected: # gerer une seule tuile apres avoir choisi une attaque
                if key_input[K_UP]:
                    self.target_position_sprite.update(1)
                elif key_input[K_DOWN]:
                    self.target_position_sprite.update(2)
                elif key_input[K_LEFT]:
                    self.target_position_sprite.update(3)
                elif key_input[K_RIGHT]:
                    self.target_position_sprite.update(4)
                unit_position = self.target_position_sprite.mapPosition

            attack_position = active_unit.handle_attacks(key_input, self.screen, unit_position)  # ou est ce que tu as appuyé sur entrée quand tu geres une suile pour lattaque
            # print(active_unit.selected_attack)
            if active_unit.defense:
                attack_position = None
                # change the player once defense
                players[active_player_index].played = 0
                players[active_player_index].set_active(False)
                active_player_index = (active_player_index + 1) % len(players)
                players[active_player_index].set_active(True)
                last_turn_switch_time = current_time
                #print(f"{active_unit.name} is defense and cannot take actions this turn.")
            selected_attack = active_unit.attacks[active_unit.selected_attack]
            # print(f"selected attack{selected_attack}")
            # find the ennemy and attack it

            if attack_position != None:
                attack_animation_playing = True
                attack_animation_position = attack_position
                attack_animation_type = selected_attack
                attack_animation_start_position = active_unit.mapPosition
                animation_start_time = pygame.time.get_ticks()
                for enemy_sprite in players[not (active_player_index)].sprite_managers:
                    if enemy_sprite.mapPosition == attack_position:
                        # print(f"this is the {attack_position}")
                        if hasattr(active_unit, 'perform_special_attack'):
                            print(f"{enemy_sprite.defense}")
                            if not enemy_sprite.defense :
                                active_unit.perform_special_attack(enemy_sprite)
                            else:
                                print(f"{enemy_sprite.name} is in a defensive state and will not take damage. ")
                                enemy_sprite.defense = False
                        else:
                            active_unit.perform_attack(30, enemy_sprite)

                        if not enemy_sprite.is_alive() and not enemy_sprite.marked_for_removal:
                            enemy_sprite.marked_for_removal = True
                            enemy_sprite.removal_time = pygame.time.get_ticks()
                            #players[active_player_index].score += 1

                        #change the player once attacked
                        players[active_player_index].played = 0
                        players[active_player_index].set_active(False)
                        active_player_index = (active_player_index + 1) % len(players)
                        players[active_player_index].set_active(True)
                        last_turn_switch_time = current_time

                for monster in self.monsters[:]:
                    
                    if monster.mapPosition == attack_position:
                        damage=30
                        #attack_animation_playing = True
                        active_unit.perform_attack(damage, monster)
                        if not monster.is_alive()and not monster.marked_for_removal:
                            monster.marked_for_removal = True
                            monster.removal_time = pygame.time.get_ticks()
                            players[active_player_index].score += 500
                            #self.monsters.remove(monster)
                        players[active_player_index].played = 0
                        players[active_player_index].set_active(False)
                        active_player_index = (active_player_index + 1) % len(players)
                        players[active_player_index].set_active(True)
                        last_turn_switch_time = current_time
                            # Increment player score
                            #players[active_player_index].score += 1

            
            highlighted_positions = self.dungeon_manager.fillDungeon_tiles(unit_position, active_unit.attack_selected, selected_attack, players[active_player_index].played, active_unit.move_range)
            # print(highlighted_positions)
            # Updates the units
            for player in players:
                for sprite in player.sprite_managers:
                    sprite.dungeon.fillDungeon_sprites(sprite, sprite == active_unit, self.screen)
            for monster in self.monsters:
                other_monsters = [m for m in self.monsters if m != monster]  # Liste des autres monstres
                player_units = [unit for player in players for unit in player.sprite_managers]  # Toutes les unités des joueurs
                monster.move_randomly(other_monsters, player_units)

                #print(f"{monster.name} new position: {monster.mapPosition}")        
            for monster in self.monsters:
                self.dungeon_manager.fillDungeon_monsters(monster, self.screen)
                

            if attack_animation_playing:
                if attack_animation_type == "Thunder Strike":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position)
                elif attack_animation_type == "Fireball":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position,
                                              start_position=attack_animation_start_position)

                elif attack_animation_type == "Water Splash":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position)
                elif attack_animation_type == "Tsunami Wave":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position,
                                              start_position=attack_animation_start_position)
                elif attack_animation_type == "Flame Burst":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position,
                                              start_position=attack_animation_start_position)
                elif attack_animation_type == "Ice Spike":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position,
                                              start_position=attack_animation_start_position)
                elif attack_animation_type == "Blizzard":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position,
                                              start_position=attack_animation_start_position)
                elif attack_animation_type == "Lightning Storm":
                    self.dungeon_manager.play(attack_animation_type, attack_animation_position,
                                              start_position=attack_animation_start_position)
                attack_animation_playing = False
                # attack_animation_playing = False
            self.dungeon_manager.tsunami_group.update()
            self.dungeon_manager.tsunami_group.draw(self.screen)
            self.dungeon_manager.fireball_group.update()
            self.dungeon_manager.fireball_group.draw(self.screen)
            self.dungeon_manager.flame_burst_group.update()
            self.dungeon_manager.flame_burst_group.draw(self.screen)
            self.dungeon_manager.ice_spike_group.update()
            self.dungeon_manager.ice_spike_group.draw(self.screen)
            self.dungeon_manager.blizzard_group.update()
            self.dungeon_manager.blizzard_group.draw(self.screen)
            self.dungeon_manager.light_storm_group.update()
            self.dungeon_manager.light_storm_group.draw(self.screen)
            for player in players:
                for sprite in player.sprite_managers[:]:
                    if sprite.marked_for_removal:
                        delay = 1000  # 1 seconds delay
                        if pygame.time.get_ticks() - sprite.removal_time > delay:
                            player.sprite_managers.remove(sprite)
            for monster in self.monsters[:]:
                if monster.marked_for_removal and pygame.time.get_ticks() - monster.removal_time > 500:
                    self.monsters.remove(monster)
            self.display_scores()



            if key_input[K_ESCAPE] or pygame.event.peek(QUIT):
                # update_map(self.file_path, None, '*', (8, 10), distance=2)
                sys.exit()
            #self.dungeon_manager.play("Water Splash", (0,0))
            #self.scree n.blit(self.background, (100, 0))
            #screen = pygame.display.set_mode((800, 600))
            #image = pygame.image.load("data/images/effects/thunder.png")  # Chargez votre image
            #position = (200, 150)  # Position de l'image

            #self.dungeon_manager.display_image_for_one_second([0,0])
            pygame.display.update()


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
    #buff_image = game.media.loadImage("data/images/effects/nuage.png") 
    #game.run_buff_animation(buff_image, "You won a key!")

    game.run_hello_screen()
    game.show_image_with_effects("data/images/background/domination_bg.png", duration=500)
    #game.run_hello_screen()

    game.load_game()
    game.run_game_loop()
