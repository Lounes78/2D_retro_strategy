import pygame
import os

class AttackHighlighter:
    def __init__(self, screen, media, tile_width, tile_height):
        """
        Classe pour gérer les attaques et les surlignages.

        :param screen: L'écran de jeu pour afficher les animations.
        :param media: Un gestionnaire pour charger les médias (images, sons).
        :param tile_width: La largeur d'une tuile.
        :param tile_height: La hauteur d'une tuile.
        """
        self.screen = screen
        self.media = media
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.highlighted_position = [0, 0]  # Case initiale (ligne, colonne)
        self.attacks = {
            "Thunder Strike": {
                "image": media.loadImage(os.path.join('data', 'images', 'effects', 'cloud.jpg')),
                "offset": (-50, 0)  # Décalage (x, y) par rapport à la tuile
            },
            "Fireball": {
                "image": media.loadImage(os.path.join('data', 'images', 'effects', 'fireball.jpg')),
                "offset": (0, 0)  # Aucun décalage
            },
            # Ajoute d'autres attaques ici...
        }
        self.current_attack = "Thunder Strike"  # Attaque par défaut

    def set_attack(self, attack_type):
        """
        Définit le type d'attaque à afficher.

        :param attack_type: Le type d'attaque ("Thunder Strike", "Fireball", etc.).
        """
        if attack_type in self.attacks:
            self.current_attack = attack_type
        else:
            print(f"Attaque non trouvée : {attack_type}")

    def update_highlighted_position(self, key_input):
        """
        Met à jour la position surlignée avec les touches du clavier.

        :param key_input: Entrées du clavier.
        """
        if key_input[pygame.K_UP]:
            self.highlighted_position[0] = max(0, self.highlighted_position[0] - 1)
        elif key_input[pygame.K_DOWN]:
            self.highlighted_position[0] = min(9, self.highlighted_position[0] + 1)  # Limiter à une grille de 10x10 par exemple
        elif key_input[pygame.K_LEFT]:
            self.highlighted_position[1] = max(0, self.highlighted_position[1] - 1)
        elif key_input[pygame.K_RIGHT]:
            self.highlighted_position[1] = min(9, self.highlighted_position[1] + 1)  # Limiter à une grille de 10x10 par exemple

    def draw_highlight(self):
        """
        Dessine le surlignage et l'image associée à l'attaque sur la case surlignée.
        """
        # Dessiner un contour autour de la case
        highlight_rect = pygame.Rect(
            self.highlighted_position[1] * self.tile_width,
            self.highlighted_position[0] * self.tile_height,
            self.tile_width,
            self.tile_height
        )
        pygame.draw.rect(self.screen, (255, 0, 0), highlight_rect, 2)  # Rouge pour le surlignage

        # Dessiner l'image associée à l'attaque
        attack_info = self.attacks[self.current_attack]
        image = attack_info["image"]
        offset_x, offset_y = attack_info["offset"]
        image_x = self.highlighted_position[1] * self.tile_width + offset_x
        image_y = self.highlighted_position[0] * self.tile_height + offset_y
        self.screen.blit(image, (image_x, image_y))
