import os, sys, random
import pygame
from pygame.locals import *

from Personaje import *

class ManejadorPersonaje(Personaje):

    VELOCIDAD = 10
    DANO = 30
    DEFENSA = 10
    VIDA = 10000
    INTELIGENCIA = 10
    RESURECCION = 10000
    NIVEL = 1

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(ManejadorPersonaje, self).__init__(mapa, media, x, y, ancho, alto, ['drackoCaminar.bmp', 'drackoGolpear.bmp'])
        personajes.remove(self)
        self.scrollMapaX = 0
        self.scrollMapaY = 0

    def mover(self, direccion):
        """Actualiza la posicion del personaje."""

        if direccion is 1:
            if self.posicion[1] > 0 and not self._siguienteBloqueado(-1, 0) and not self._siguienteAlto(-1, 0) and not self._siguienteOcupado(-1, 0):
                if len([fila[self.posicion[0]] for fila in self.mapa.mapa]) - self.posicion[1] > 16 and self.scrollMapaY > 0:
                    self.scrollMapaY -= 1
        elif direccion is 2:
            if self.posicion[1] < len([fila[self.posicion[0]] for fila in self.mapa.mapa]) - 1 and not self._siguienteBloqueado(1, 0) and not self._siguienteAlto(1, 0) and not self._siguienteOcupado(1, 0):
                if self.posicion[1] > 15 and len([fila[self.posicion[0]] for fila in self.mapa.mapa]) - self.posicion[1] > 4 and len([fila[self.posicion[0]] for fila in self.mapa.mapa][self.scrollMapaY:]) > 20:
                    self.scrollMapaY += 1
        elif direccion is 3:
            if self.posicion[0] > 0 and not self._siguienteBloqueado(0, -1) and not self._siguienteAlto(0, -1) and not self._siguienteOcupado(0, -1):
                if len(self.mapa.mapa[self.posicion[1]]) - self.posicion[0] > 16 and self.scrollMapaX > 0:
                    self.scrollMapaX -= 1
        elif direccion is 4:
            if self.posicion[0] < len(self.mapa.mapa[self.posicion[1]]) - 1 and not self._siguienteBloqueado(0, 1) and not self._siguienteAlto(0, 1) and not self._siguienteOcupado(0, 1):
                if self.posicion[0] > 15 and len(self.mapa.mapa[self.posicion[1]]) - self.posicion[0] >= 4 and len(self.mapa.mapa[self.posicion[1]][self.scrollMapaX:]) > 20:
                    self.scrollMapaX += 1
        super(ManejadorPersonaje, self).mover(direccion)

    def accion(self, accion):
        """Obtiene entrada del teclado para mover al personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return None
        if self != None and self.vida <= 0:
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            print "Juego Terminado"
            self = None
        if self != None and not self._golpeando and not self.vida < 0:
            if accion[K_UP]:
                self.mover(1)
            elif accion[K_DOWN]:
                self.mover(2)
            elif accion[K_LEFT]:
                self.mover(3)
            elif accion[K_RIGHT]:
                self.mover(4)
            elif accion[K_a]:
                self.juntoAPersonaje()
                self.golpear()
        if self != None: self.animacion()