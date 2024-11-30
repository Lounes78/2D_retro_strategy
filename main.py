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
        self.sound.music.play(-1)

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

        pygame.display.update()



    def run_game_loop(self):
        """Runs the main game loop."""
        # Start with Dracko's turn
        players = [self.dracko_player, self.second_player]
        active_player_index = 0
        players[active_player_index].set_active(True)
        
        current_unit_index = 0
        last_turn_switch_time = 0  # Timestamp for the last turn switch
        switch_cooldown = 700  # Cooldown in milliseconds for switching turns

        while True:
            pygame.event.pump()
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


            # Process movement only for the active player
            if players[active_player_index].is_turn():
                if key_input[K_UP]:
                    players[active_player_index].take_turn(1, current_unit_index)
                elif key_input[K_DOWN]:
                    players[active_player_index].take_turn(2, current_unit_index)
                elif key_input[K_LEFT]:
                    players[active_player_index].take_turn(3, current_unit_index)
                elif key_input[K_RIGHT]:
                    players[active_player_index].take_turn(4, current_unit_index)

            if key_input[K_ESCAPE] or pygame.event.peek(QUIT):
                sys.exit()

            # Update the game screen
            self.screen.blit(self.background, (0, 0))

            active_unit = players[active_player_index].sprite_managers[current_unit_index]
            unit_position = active_unit.mapPosition 
            # Update dungeon based on unit positions
            unit_position = players[active_player_index].sprite_managers[current_unit_index].mapPosition
            
            self.dungeon_manager.fillDungeon_tiles(unit_position)
            # Updates the units
            for player in players:
                for sprite in player.sprite_managers:
                    sprite.dungeon.fillDungeon_sprites(sprite, sprite == active_unit, self.screen)
            






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





# import os
# import pygame
# import datetime

# def save_sprite_images(sprite, unit, folder_base="rendered_sprites"):
#     """Saves the current sprite image being rendered to a unique folder with unique names."""

#     # Check if sprite is valid and has the necessary map position
#     if sprite and hasattr(sprite, 'mapPosition'):
#         # Create a folder with a timestamp if it doesn't exist
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         folder_path = os.path.join(folder_base, timestamp)
#         os.makedirs(folder_path, exist_ok=True)

#         # Get the current sprite surface using its animation frame
#         sprite_surface = sprite.sprite[unit._tmpAnimateSprite]

#         # Render the sprite to a temporary surface
#         temp_surface = pygame.Surface((sprite_surface.get_width(), sprite_surface.get_height()), pygame.SRCALPHA)
#         temp_surface.blit(sprite_surface, (0, 0))

#         # Generate a unique filename for each sprite using its animation frame
#         file_name = f"sprite_{unit._tmpAnimateSprite}.png"
#         file_path = os.path.join(folder_path, file_name)

#         # Save the image to the file
#         pygame.image.save(temp_surface, file_path)
#         print(f"Sprite image saved as '{file_path}'")



if __name__ == "__main__":
    game = Game()
    game.run_hello_screen()
    game.load_game()
    game.run_game_loop()
