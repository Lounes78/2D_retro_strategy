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
        except pygame.error, message:
            print "Can't Load sound file: ", self._fullName
            raise SystemExit, message
        return self._musicBox

    def loadImage(self, path, colorkey = None):
        """Load an image."""

        self._fullName = path
        try:
            self._image = pygame.image.load(self._fullName)
        except pygame.error, message:
            print "Can't Load Background: ", self._fullName
            raise SystemExit, message
        self._image  = self._image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = self._image.get_at((0, 0))
            self._image.set_colorkey(colorkey, RLEACCEL)
        return self._image

    def loadReadFile(self, name):
        """Loads a file."""

        self._filePath = name
        self._mapFile = open(self._filePath, 'r')
        return self._mapFile
