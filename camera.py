import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)  # La vue de la caméra (zone visible)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height
        self.zoom_factor = 1.0  # Facteur de zoom initial (1 = normal)

    def apply(self, surface):
        """Applique la caméra à la surface (découpe la portion visible de l'écran)."""
        return surface.subsurface(self.camera)

    def apply_zoom(self, surface):
        """Applique le zoom à la surface du jeu."""
        if self.zoom_factor != 1:
            # Appliquer un zoom sur la surface
            new_width = int(self.width * self.zoom_factor)
            new_height = int(self.height * self.zoom_factor)

            # Limiter la taille pour ne pas rendre la carte trop petite
            if new_width < self.width or new_height < self.height:
                new_width = self.width
                new_height = self.height

            zoomed_surface = pygame.transform.scale(surface, (new_width, new_height))  # Appliquer le zoom
            return zoomed_surface
        return surface

    def zoom_in(self):
        """Augmente le facteur de zoom."""
        self.zoom_factor += 0.1
        if self.zoom_factor > 2.0:  # Limiter le zoom pour éviter un zoom excessif
            self.zoom_factor = 2.0

    def zoom_out(self):
        """Diminue le facteur de zoom."""
        self.zoom_factor -= 0.1
        if self.zoom_factor < 0.5:  # Limiter le dézoom pour ne pas rendre trop petit
            self.zoom_factor = 0.5
