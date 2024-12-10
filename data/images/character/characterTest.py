#!/usr/bin/env python

import os, sys, random
import pygame
from pygame.locals import *

class loadMedia(object):
    """Handles media objects."""

    def __init__(self):
        """Loads all the media."""

        self._fullName = None

    def loadSound(self, name):
        """Loads the sound."""

        class NoneSound:
            def play(self): pass
            def stop(self): pass

        if not pygame.mixer:
            return NoneSound()
        self._fullName = name
        try:
            self._musicBox = pygame.mixer
            self._musicBox.init()
            self._musicBox.music.load(self._fullName)
            self._musicBox.music.set_volume(.7)
        except pygame.error as message:
            print ("Can't Load sound file: ", self._fullName)
            raise SystemExit(message)
        return self._musicBox

    def loadImage(self, path, colorkey = None):
        """Load an image."""

        self._fullName = path
        try:
            self._image = pygame.image.load(self._fullName)
        except pygame.error as message:
            print ("Can't Load Background: ", self._fullName)
            raise SystemExit(message)
        # self._image  = self._image.convert_alpha()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = self._image.get_at((0, 0))
            self._image.set_colorkey(colorkey, RLEACCEL)
        return self._image

    def loadReadFile(self, name):
        """Loads a file."""

        self._filePath = name
        self._mapFile = open(self._filePath, 'r')
        return self._mapFile
pygame.init()

# Dimensions exactes pour le personnage
character_width, character_height = 40, 40  # Dimensions estimées (ajustez si nécessaire)
character_surface = pygame.Surface((character_width, character_height), pygame.SRCALPHA)  # Surface avec transparence

media = loadMedia()

# Charger les images du personnage
body = media.loadImage(os.path.join('body', 'front', 'left', 'American.png'))
eye = media.loadImage(os.path.join('eye', 'madRed.png'))
mouth = media.loadImage(os.path.join('mouth', 'normal.png'))
shirt = media.loadImage(os.path.join('shirt', 'grayArmor.png'))
pants = media.loadImage(os.path.join('pants', 'grayArmor.png'))
shoes = media.loadImage(os.path.join('shoes', 'grayShoes.png'))
hair = media.loadImage(os.path.join('hair', 'mohawk.png'))
cape = media.loadImage(os.path.join('cape', 'knight.png'))

# Dessiner uniquement le personnage sur la surface dédiée
character_surface.blit(cape, (0, 0))  # Ajustez les positions selon les dimensions
character_surface.blit(body, (0, 0))
character_surface.blit(eye, (0, 0))
character_surface.blit(mouth, (0, 0))
character_surface.blit(shirt, (0, 0))
character_surface.blit(pants, (0, 0))
character_surface.blit(shoes, (0, 0))
character_surface.blit(hair, (0, 0))

# Sauvegarde de la surface du personnage en PNG
output_path = os.path.join('output', 'character.png')  # Définir le chemin de sauvegarde
os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Créer le dossier si nécessaire
pygame.image.save(character_surface, output_path)

print(f"Image sauvegardée sous {output_path}")

# back  left one 
# back  left two 
# back  left three 

# back  right one 
# back  right two 
# back  right three 


# front  left 
# front  right 
