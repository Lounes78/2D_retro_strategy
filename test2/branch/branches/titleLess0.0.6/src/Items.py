import os, sys, random
import pygame
from pygame.locals import *

from Item import *

class Pocion(Item):

    RESURECCION = 10000
    VALOR = 100

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Pocion, self).__init__(mapa, media, x, y, ancho, alto, 'pocion.bmp', 'recuperaVida')
        for imagen in self.item:
            imagen.set_alpha(255 * .8)


class Fuego(Item):

    VALOR = 100
    RESURECCION = 5000

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Fuego, self).__init__(mapa, media, x, y, ancho, alto, 'fuego.bmp', 'quitaVida')
        for imagen in self.item:
            imagen.set_alpha(255 * .8)

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        pass

class Pico(Item):

    VELOCIDAD = 10
    VALOR = 70
    RESURECCION = 0

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Pico, self).__init__(mapa, media, x, y, ancho, alto, 'pico.bmp', 'quitaVida')
        self.eliminar = False

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        pass

class PicoFuerte(Item):

    VELOCIDAD = 15
    VALOR = 100
    RESURECCION = 0

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(PicoFuerte, self).__init__(mapa, media, x, y, ancho, alto, 'picoFuerte.bmp', 'quitaVida')
        self.eliminar = False

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        pass

class PicoRapido(Item):

    VELOCIDAD = 5
    VALOR = 60
    RESURECCION = 0

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(PicoRapido, self).__init__(mapa, media, x, y, ancho, alto, 'PicoRapido.bmp', 'quitaVida')
        self.eliminar = False

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        pass

class Piedra(Item):

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Piedra, self).__init__(mapa, media, x, y, ancho, alto, 'piedra.bmp', 'bloquea')
        self.eliminar = False
        self.mapa.ocupado[y][x] = True

    def animacion(self):

        self._estaEnAgua()
        self.spriteActual = pygame.Surface.copy(self.item[self._enAgua])
        self.rect = self.spriteActual.get_rect()

    def _estaEnAgua(self):

        if self.mapa.mapa[self.posicion[1]][self.posicion[0]] == "agua":
            self._enAgua = 1
            return True
        else:
            self._enAgua = 0
            return False

class Veneno(Item):

    VELOCIDAD = 5
    VALOR = 50
    RESURECCION = 0

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Veneno, self).__init__(mapa, media, x, y, ancho, alto, 'veneno.bmp', 'quitaVida')
        for imagen in self.item:
            imagen.set_alpha(255 * .6)
        self.eliminar = True

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        pass