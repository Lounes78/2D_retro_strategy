import pygame
from pygame.locals import *

class ManejadorVentana(object):

    def __init__(self, ventana):

        self._ventana = ventana

    def centrarItemX(self, item):
        """Centra una imagen en el plano X."""

        self._item = item
        self._screenX = self._ventana.get_width()
        self._itemX = self._item.get_width()
        return (self._screenX / 2) - (self._itemX / 2)

    def centrarItemY(self, item):
        """Centra una imagen en el plano Y."""

        self._item = item
        self._screenY = self._ventana.get_height()
        self._itemY = self._item.get_height()
        return (self._screenY / 2) - (self._itemY / 2)
