import pygame
from pygame.locals import *

class windowManager(object):
    """Handles the window."""

    def __init__(self, screen):
        """Handles window."""

        self._screen = screen

    def centerItemX(self, item):
        """Centers an image in the X plane."""

        self._item = item
        self._screenX = self._screen.get_width()
        self._itemX = self._item.get_width()
        return (self._screenX / 2) - (self._itemX / 2)

    def centerItemY(self, item):
        """Centers an image in the Y plane."""

        self._item = item
        self._screenY = self._screen.get_height()
        self._itemY = self._item.get_height()
        return (self._screenY / 2) - (self._itemY / 2)
