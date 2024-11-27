import pygame
import random

from unit import *


class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy')]

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)



    def flip_display(self):
        """Renders the game with an enhanced battleground."""

        # Fill the screen with a base color or textured background
        self.screen.fill((30, 30, 30))  # Dark grey background for a better aesthetic

        # Draw the grid with slight color variations to simulate terrain
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Alternate colors for the grid
                color = (50, 50, 50) if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0 else (60, 60, 60)
                pygame.draw.rect(self.screen, color, rect)

                # Draw grid lines
                pygame.draw.rect(self.screen, (80, 80, 80), rect, 1)

        # Add obstacles or terrain features (example: rocks, trees)
        for _ in range(10):  # Example: random decorations
            obstacle_x = random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE
            obstacle_y = random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE
            obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, CELL_SIZE, CELL_SIZE)
            pygame.draw.ellipse(self.screen, (100, 100, 100), obstacle_rect)  # Example: stone

        # Highlight the selected unit (if any)
        for unit in self.player_units:
            if unit.is_selected:
                rect = pygame.Rect(unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)  # Highlight with yellow

        # Draw units
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Refresh the display
        pygame.display.flip()



    # def flip_display(self):
    #     """Affiche le jeu."""
    #     # Affiche la grille
    #     self.screen.fill(BLACK)
    #     for x in range(0, WIDTH, CELL_SIZE):
    #         for y in range(0, HEIGHT, CELL_SIZE):
    #             rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    #             pygame.draw.rect(self.screen, WHITE, rect, 1)

    #     # Affiche les unités
    #     for unit in self.player_units + self.enemy_units:
    #         unit.draw(self.screen)

    #     # Rafraîchit l'écran
    #     pygame.display.flip()


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
