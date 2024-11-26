import os, sys, random
import pygame
from pygame.locals import *

class Item(pygame.sprite.Sprite):

    global items
    items = pygame.sprite.Group()

    VELOCIDAD = 10
    RESURECCION = 10000
    VALOR = 10

    def __init__(self, mapa, media, x, y, ancho, alto, archivoItems, accion):

        pygame.sprite.Sprite.__init__(self)
        self.sprite = None
        self.mapa = mapa
        self.media = media
        self.spriteActual = pygame.Surface([ancho, alto])
        self._spriteIndice = 0
        self._enAgua = 0
        self.eliminar = True
        self.inicial = [x, y]
        #se puede ciclar infinito
        while self.mapa.mapa[y][x] in self.mapa._azulejosBloqueados or self.mapa.items[y][x] != None or self.mapa.ocupado[y][x] != None:
            if x >= 3 and x < len(mapa.ocupado[0]) - 3: x = random.randint(x - 3, x + 3)
            if y >= 0 and y < len(mapa.ocupado) - 3: y = random.randint(y - 3, y + 3)
        self.mapa.items[y][x] = self
        self.posicion = [x, y]
        sprites = self.media.loadImage(os.path.join('data', 'images', 'character', 'body', archivoItems)).convert()
        sprites.set_colorkey(sprites.get_at((0,0)), RLEACCEL)
        spritesAncho, spritesAlto = sprites.get_size()
        self.item = []
        self._animacionSeq = 1
        for j in xrange(int(spritesAncho/ancho)):
            self.item.append(sprites.subsurface(j * ancho, 0, ancho, alto))
        items.add(self)
        self.spriteActual = pygame.Surface.copy(self.item[0])
        self.accion = accion
        self.valor = self.VALOR
        self._contadorAccion = self.VELOCIDAD
        self.rect = self.spriteActual.get_rect()

    def animacion(self):
        """Crea la animacion del personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return
        self.spriteActual = pygame.Surface.copy(self.item[self._spriteIndice + self._enAgua])
        if self._spriteIndice == 2:
            self._animacionSeq = -1
        elif self._spriteIndice == 0:
            self._animacionSeq = 1
        self._spriteIndice += self._animacionSeq
        self.rect = self.spriteActual.get_rect()
        self._estaEnAgua()

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        if self.mapa.mapa[self.posicion[1]][self.posicion[0]] == "agua":
            self._enAgua = 3
            return True
        else:
            self._enAgua = 0
            return False

    def eliminarItem(self):

        if self.eliminar:
            items.remove(self)
            return True
        return False

    @staticmethod
    def obtenerItems():

        return items