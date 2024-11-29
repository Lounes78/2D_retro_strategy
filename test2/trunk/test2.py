import os
import sys
import pygame
from pygame.locals import *

from mediaManager import *
from windowManager import *
from dungeonManager import *
from spriteManager import *

class Unit:
    """Class representing a game unit."""
    
    def __init__(self, dungeon_manager, media):
        # The base
        self.dungeon_manager = dungeon_manager
        self.media = media
        self.sprite_manager = spriteManager(dungeon_manager, media) # we create the character here
        self.sprite_manager2 = spriteManager(dungeon_manager, media) # we create the character here

        
    def update(self, direction):
        """Updates the unit's position based on direction."""
        self.sprite_manager.update(direction)
        self.sprite_manager2.update(direction)
        





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
        self.dungeon_manager = None
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
        self.dracko = Unit(self.dungeon_manager, self.media)
        pygame.display.update()

    def run_game_loop(self):
        """Runs the main game loop."""
        while True:
            pygame.event.pump()
            key_input = pygame.key.get_pressed()
            if key_input[K_UP]:
                self.dracko.update(1)
            elif key_input[K_DOWN]:
                self.dracko.update(2)
            elif key_input[K_LEFT]:
                self.dracko.update(3)
            elif key_input[K_RIGHT]:
                self.dracko.update(4)
            if key_input[K_ESCAPE] or pygame.event.peek(QUIT):
                sys.exit()
            self.screen.blit(self.background, (0, 0))
            self.dungeon_manager.fillDungeon(self.dracko.sprite_manager)
            pygame.display.update()
            pygame.time.delay(120)


if __name__ == "__main__":
    game = Game()
    game.run_hello_screen()
    game.load_game()
    game.run_game_loop()