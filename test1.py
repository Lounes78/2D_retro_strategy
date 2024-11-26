import pygame
from pygame.math import Vector2
from pytmx import load_pygame
from os.path import join

# --- Constants ---
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 1000
TILE_SIZE = 32  # Taille d'une tuile
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# --- Classes ---

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, health=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

        # Points de vie (facultatif)
        self.max_hp = health
        self.current_hp = health

    def take_damage(self, damage):
        """Réduit les points de vie si le sprite en a."""
        if self.current_hp is not None:
            self.current_hp -= damage
            if self.current_hp <= 0:
                self.kill()  # Supprime le sprite du jeu

    def draw_health_bar(self, surface):
        """Affiche une barre de vie si le sprite en a."""
        if self.current_hp is not None:
            bar_width = self.rect.width
            bar_height = 5
            bar_x = self.rect.x
            bar_y = self.rect.y - 10

            # Fond de la barre (rouge)
            pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

            # Barre de vie actuelle (vert)
            health_ratio = self.current_hp / self.max_hp
            pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))


class Player(Sprite):
    def __init__(self, pos, groups, collision_sprites):
        # Appel au constructeur de Sprite
        surf = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        super().__init__(pos, surf, groups)

        # Chargement de l'image par défaut et du rectangle associé
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        # Attributs de mouvement
        self.direction = Vector2()
        self.speed = 200
        self.state = 'idle'
        self.frame = 0
        self.animation_speed = 0.15

        # Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(-20, -10)  # Réduction du hitbox pour une meilleure précision

        # Chargement des images pour les quatre directions
        self.down_images = [pygame.image.load(join('images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)]
        self.up_images = [pygame.image.load(join('images', 'player', 'up', f'{i}.png')).convert_alpha() for i in range(4)]
        self.left_images = [pygame.image.load(join('images', 'player', 'left', f'{i}.png')).convert_alpha() for i in range(4)]
        self.right_images = [pygame.image.load(join('images', 'player', 'right', f'{i}.png')).convert_alpha() for i in range(4)]

    def input(self):
        keys = pygame.key.get_pressed()

        # Détection des mouvements horizontaux
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.state = 'walking'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.state = 'walking'
        else:
            self.direction.x = 0

        # Détection des mouvements verticaux
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.state = 'walking'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.state = 'walking'
        else:
            self.direction.y = 0

        # Si aucun mouvement, le joueur est à l'arrêt
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = 'idle'

        # Normalisation des mouvements diagonaux
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

    def move(self, dt):
        # Mouvement horizontal avec vérification des collisions
        self.hitbox.x += self.direction.x * self.speed * dt
        self.check_collisions('horizontal')

        # Mouvement vertical avec vérification des collisions
        self.hitbox.y += self.direction.y * self.speed * dt
        self.check_collisions('vertical')

        # Mise à jour de la position du rectangle
        self.rect.center = self.hitbox.center

    def check_collisions(self, direction):
        for sprite in self.collision_sprites.sprites():
            if self.hitbox.colliderect(sprite.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Déplacement vers la droite
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # Déplacement vers la gauche
                        self.hitbox.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:  # Déplacement vers le bas
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # Déplacement vers le haut
                        self.hitbox.top = sprite.rect.bottom

    def animate(self):
        """Gère l'animation en fonction de l'état et de la direction."""
        self.frame += self.animation_speed
        if self.frame >= len(self.down_images):
            self.frame = 0

        if self.state == 'idle':
            self.update_idle_image()
        elif self.state == 'walking':
            self.update_walking_image()

    def update_idle_image(self):
        """Met à jour l'image quand le joueur est immobile."""
        if self.direction.y == 1:
            self.image = self.down_images[0]
        elif self.direction.y == -1:
            self.image = self.up_images[0]
        elif self.direction.x == -1:
            self.image = self.left_images[0]
        elif self.direction.x == 1:
            self.image = self.right_images[0]

    def update_walking_image(self):
        """Met à jour l'image quand le joueur marche."""
        if self.direction.y == 1:
            self.image = self.down_images[int(self.frame)]
        elif self.direction.y == -1:
            self.image = self.up_images[int(self.frame)]
        elif self.direction.x == -1:
            self.image = self.left_images[int(self.frame)]
        elif self.direction.x == 1:
            self.image = self.right_images[int(self.frame)]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate()



class TransitionZone(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, action):
        super().__init__(groups)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.action = action  # Fonction à exécuter lors de l'interaction


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Open World to Turn-Based Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()

        # Game states
        self.state = "exploration"  # Can be "exploration" or "combat"

        # Map setup
        self.tmx_data = load_pygame("data/maps/world.tmx")  # Charger la carte
        self.setup()

    def setup(self):
        """Initialise la carte et les objets."""
        # Charger les calques de la carte
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, image in layer.tiles():
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        # Ajouter un buisson interactif
        self.bush = TransitionZone((800, 800), (TILE_SIZE, TILE_SIZE), self.interactable_sprites, self.start_combat)
        bush_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        bush_surface.fill(GREEN)
        self.bush_sprite = Sprite((800, 800), bush_surface, self.all_sprites)

        # Ajouter le joueur
        self.player = Player((400, 300), self.all_sprites, self.collision_sprites)

    def start_combat(self):
        """Passe en mode combat."""
        self.state = "combat"

    def handle_events(self):
        """Gère les événements."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "exploration":
                    # Vérifie si le joueur interagit avec le buisson
                    for sprite in self.interactable_sprites:
                        if self.player.rect.colliderect(sprite.rect):
                            sprite.action()  # Exécute l'action du buisson

    def update(self, dt):
        """Met à jour le jeu en fonction de l'état."""
        if self.state == "exploration":
            self.all_sprites.update(dt)
        elif self.state == "combat":
            pass  # Ajoute ici la logique de combat si nécessaire

    def render(self):
        """Affiche les éléments à l'écran."""
        self.display_surface.fill(WHITE)

        if self.state == "exploration":
            # Dessiner la carte
            for layer in self.tmx_data.visible_layers:
                if hasattr(layer, "tiles"):
                    for x, y, image in layer.tiles():
                        self.display_surface.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

            # Dessiner les sprites
            for sprite in self.all_sprites:
                self.display_surface.blit(sprite.image, sprite.rect)
        elif self.state == "combat":
            # Afficher un message "C'EST L'HEURE DU DUEL"
            font = pygame.font.Font(None, 50)
            text_surface = font.render("C'EST L'HEURE DU DUEL", True, RED)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.display_surface.blit(text_surface, text_rect)

        pygame.display.flip()

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.render()


# --- Main ---
if __name__ == "__main__":
    game = Game()
    game.run()
