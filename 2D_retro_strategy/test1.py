import pygame
from pytmx import load_pygame
from pygame.math import Vector2
from os.path import join

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 1000
TILE_SIZE = 30

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)




class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Apply the camera offset to a sprite."""
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """Update the camera position based on the player's position."""
        x = -target.rect.centerx + WINDOW_WIDTH // 2
        y = -target.rect.centery + WINDOW_HEIGHT // 2

        # Clamp the camera so it doesn't go outside the map bounds
        x = min(0, max(-(self.width - WINDOW_WIDTH), x))
        y = min(0, max(-(self.height - WINDOW_HEIGHT), y))

        self.camera = pygame.Rect(x, y, self.width, self.height)













class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
        # Movement attributes
        self.direction = Vector2()
        self.speed = 200
        self.state = 'idle'
        self.frame = 0
        self.animation_speed = 0.15
        
        # Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(-20, -10)  # Create a smaller hitbox for better collision feel
        
        # Load the images for the four directions
        self.down_images = [pygame.image.load(join('images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)]
        self.up_images = [pygame.image.load(join('images', 'player', 'up', f'{i}.png')).convert_alpha() for i in range(4)]
        self.left_images = [pygame.image.load(join('images', 'player', 'left', f'{i}.png')).convert_alpha() for i in range(4)]
        self.right_images = [pygame.image.load(join('images', 'player', 'right', f'{i}.png')).convert_alpha() for i in range(4)]
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.state = 'walking'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.state = 'walking'
        else:
            self.direction.x = 0
        
        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.state = 'walking'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.state = 'walking'
        else:
            self.direction.y = 0
        
        # If no movement, set state to idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = 'idle'
    
        # Normalize diagonal movement
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

    def move(self, dt):
        # Move horizontally and check for collisions
        self.hitbox.x += self.direction.x * self.speed * dt
        self.check_collisions('horizontal')
        
        # Move vertically and check for collisions
        self.hitbox.y += self.direction.y * self.speed * dt
        self.check_collisions('vertical')
        
        # Update rect position to match hitbox
        self.rect.center = self.hitbox.center

    def check_collisions(self, direction):
        for sprite in self.collision_sprites.sprites():
            if self.hitbox.colliderect(sprite.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.rect.right
                
                elif direction == 'vertical':
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.rect.bottom
    
    def update(self, dt):
        self.input()
        self.move(dt)
        
        # Handle animation frames
        self.frame += self.animation_speed
        if self.frame >= len(self.down_images):
            self.frame = 0
        
        if self.state == 'idle':
            self.update_idle_image()
        elif self.state == 'walking':
            self.update_walking_image()
    
    def update_idle_image(self):
        if self.direction.x == 0 and self.direction.y == 1:
            self.image = self.down_images[0]
        elif self.direction.x == 0 and self.direction.y == -1:
            self.image = self.up_images[0]
        elif self.direction.x == -1:
            self.image = self.left_images[0]
        elif self.direction.x == 1:
            self.image = self.right_images[0]
    
    def update_walking_image(self):
        if self.direction.y == 1:
            self.image = self.down_images[int(self.frame)]
        elif self.direction.y == -1:
            self.image = self.up_images[int(self.frame)]
        elif self.direction.x == -1:
            self.image = self.left_images[int(self.frame)]
        elif self.direction.x == 1:
            self.image = self.right_images[int(self.frame)]



class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Map size (adjust to your map's dimensions in tiles)
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.map_width = map.width * TILE_SIZE
        self.map_height = map.height * TILE_SIZE

        # Camera
        self.camera = Camera(self.map_width, self.map_height)

        # Setup the game
        self.setup()

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        # Create ground tiles (background)
        ground_layer = map.get_layer_by_name('Ground')
        for x, y, image in ground_layer.tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        # Create collision objects
        object_layer = map.get_layer_by_name('Objects')
        for obj in object_layer:
            image = obj.image if hasattr(obj, 'image') else pygame.Surface((TILE_SIZE, TILE_SIZE))
            CollisionSprite((obj.x, obj.y), image, (self.all_sprites, self.collision_sprites))

        # Create the player after the map setup, passing collision_sprites
        self.player = Player((400, 300), self.all_sprites, self.collision_sprites)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # Time in seconds since last frame
            self.handle_events()
            self.update(dt)
            self.render()

    def update(self, dt):
        self.all_sprites.update(dt)
        self.camera.update(self.player)

    def render(self):
        self.display_surface.fill((0, 0, 0))  # Clear the screen with a black background
        for sprite in self.all_sprites:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()










if __name__ == '__main__':
    game = Game()
    game.run()