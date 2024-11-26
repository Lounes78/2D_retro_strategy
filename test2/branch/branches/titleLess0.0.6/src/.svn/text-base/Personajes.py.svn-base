import os, sys, random
import pygame
from pygame.locals import *

from Personaje import *
from Items import *

class Vivora(Personaje):

    VELOCIDAD = 10
    DANO = 30
    DEFENSA = 10
    VIDA = 200
    INTELIGENCIA = 10
    RESURECCION = 2000
    NIVEL = 1

    def __init__(self, mapa, media, x, y, ancho, alto, archivosSprites = ['vivoraCaminar.bmp', 'vivoraGolpear.bmp']):

        super(Vivora, self).__init__(mapa, media, x, y, ancho, alto, archivosSprites)
        self.items = ["Pocion", "Veneno", "Veneno", "Veneno", "Veneno", "Veneno"]

    def accion(self, accion):
        """Obtiene entrada del teclado para accionar al personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return
        if self != None and self.vida <= 0:
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            personajes.remove(self)
            eval(self.items[random.randint(0, 5)])(self.mapa, self.media, self.posicion[0], self.posicion[1], 40, 40)
            self = None
        if self != None and not self._golpeando and not self.vida < 0:
            atacando = self.viendoAPersonaje()
            if isinstance(self._golpeandoA, Vivora): atacando = False
            if atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, Vivora): self.golpear()
            if random.randint(1, 6) == 6 and not atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, Vivora):
                if self.posicion[1] > 0:
                    if self.mapa.ocupado[self.posicion[1] - 1][self.posicion[0]] != None: self.mover(1)
                if self.posicion[1] < len(self.mapa.ocupado) - 1:
                    if self.mapa.ocupado[self.posicion[1] + 1][self.posicion[0]] != None: self.mover(2)
                if self.posicion[0] > 0:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] - 1] != None: self.mover(3)
                if self.posicion[0] < len(self.mapa.ocupado[0]) - 1:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] + 1] != None: self.mover(4)
            if random.randint(1, 6) == 3 and not atacando or isinstance(self._golpeandoA, Vivora):
                self._dejarGolpear()
                movimiento = random.randint(1, 4)
                if movimiento == 1 and self.posicion[1] - 1 < self.inicial[1] - 3:
                    return
                if movimiento == 2 and self.posicion[1] + 1 > self.inicial[1] + 3:
                    return
                if movimiento == 3 and self.posicion[0] - 1 < self.inicial[0] - 3:
                    return
                if movimiento == 4 and self.posicion[0] + 1 > self.inicial[0] + 3:
                    return
                self.mover(movimiento)
        if self != None: self.animacion()

class VivoraFuerte(Vivora):

    VELOCIDAD = 12
    DANO = 50
    DEFENSA = 10
    VIDA = 200
    INTELIGENCIA = 10
    RESURECCION = 8000
    NIVEL = 1

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(VivoraFuerte, self).__init__(mapa, media, x, y, ancho, alto, ['vivoraCaminar2.bmp', 'vivoraGolpear2.bmp'])
        self.items = ["Pocion", "Pocion", "Veneno", "Veneno", "Veneno", "Veneno"]

    def accion(self, accion):
        """Obtiene entrada del teclado para accionar al personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return
        if self != None and self.vida <= 0:
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            personajes.remove(self)
            eval(self.items[random.randint(0, 5)])(self.mapa, self.media, self.posicion[0], self.posicion[1], 40, 40)
            self = None
        if self != None and not self._golpeando and not self.vida < 0:
            atacando = self.viendoAPersonaje()
            if isinstance(self._golpeandoA, VivoraFuerte) or isinstance(self._golpeandoA, VivoraJefe): atacando = False
            if atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraFuerte) and not isinstance(self._golpeandoA, VivoraJefe): self.golpear()
            if random.randint(1, 7) == 7 and not atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraFuerte) and not isinstance(self._golpeandoA, VivoraJefe):
                if self.posicion[1] > 0:
                    if self.mapa.ocupado[self.posicion[1] - 1][self.posicion[0]] != None: self.mover(1)
                if self.posicion[1] < len(self.mapa.ocupado) - 1:
                    if self.mapa.ocupado[self.posicion[1] + 1][self.posicion[0]] != None: self.mover(2)
                if self.posicion[0] > 0:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] - 1] != None: self.mover(3)
                if self.posicion[0] < len(self.mapa.ocupado[0]) - 1:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] + 1] != None: self.mover(4)
            if random.randint(1, 5) == 3 and not atacando or isinstance(self._golpeandoA, VivoraFuerte) or isinstance(self._golpeandoA, VivoraJefe):
                self._dejarGolpear()
                movimiento = random.randint(1, 4)
                if movimiento == 1 and self.posicion[1] - 1 < self.inicial[1] - 2:
                    return
                if movimiento == 2 and self.posicion[1] + 1 > self.inicial[1] + 2:
                    return
                if movimiento == 3 and self.posicion[0] - 1 < self.inicial[0] - 2:
                    return
                if movimiento == 4 and self.posicion[0] + 1 > self.inicial[0] + 2:
                    return
                self.mover(movimiento)
        if self != None: self.animacion()


class VivoraRapida(Vivora):

    VELOCIDAD = 8
    DANO = 20
    DEFENSA = 10
    VIDA = 200
    INTELIGENCIA = 10
    RESURECCION = 6000
    NIVEL = 1

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(VivoraRapida, self).__init__(mapa, media, x, y, ancho, alto, ['vivoraCaminar3.bmp', 'vivoraGolpear3.bmp'])
        self.items = ["Pocion", "Pocion", "Pocion", "Veneno", "Veneno", "Veneno"]

    def accion(self, accion):
        """Obtiene entrada del teclado para accionar al personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return
        if self != None and self.vida <= 0:
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            personajes.remove(self)
            eval(self.items[random.randint(0, 5)])(self.mapa, self.media, self.posicion[0], self.posicion[1], 40, 40)
            self = None
        if self != None and not self._golpeando and not self.vida < 0:
            atacando = self.viendoAPersonaje()
            if isinstance(self._golpeandoA, VivoraFuerte) or isinstance(self._golpeandoA, VivoraJefe): atacando = False
            if atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraFuerte) and not isinstance(self._golpeandoA, VivoraJefe): self.golpear()
            if random.randint(1, 4) == 4 and not atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraFuerte) and not isinstance(self._golpeandoA, VivoraJefe):
                if self.posicion[1] > 0:
                    if self.mapa.ocupado[self.posicion[1] - 1][self.posicion[0]] != None: self.mover(1)
                if self.posicion[1] < len(self.mapa.ocupado) - 1:
                    if self.mapa.ocupado[self.posicion[1] + 1][self.posicion[0]] != None: self.mover(2)
                if self.posicion[0] > 0:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] - 1] != None: self.mover(3)
                if self.posicion[0] < len(self.mapa.ocupado[0]) - 1:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] + 1] != None: self.mover(4)
            if random.randint(1, 4) == 3 and not atacando or isinstance(self._golpeandoA, VivoraFuerte) or isinstance(self._golpeandoA, VivoraJefe):
                self._dejarGolpear()
                movimiento = random.randint(1, 4)
                if movimiento == 1 and self.posicion[1] - 1 < self.inicial[1] - 4:
                    return
                if movimiento == 2 and self.posicion[1] + 1 > self.inicial[1] + 4:
                    return
                if movimiento == 3 and self.posicion[0] - 1 < self.inicial[0] - 4:
                    return
                if movimiento == 4 and self.posicion[0] + 1 > self.inicial[0] + 4:
                    return
                self.mover(movimiento)
        if self != None: self.animacion()

class VivoraJefe(Vivora):

    VELOCIDAD = 10
    DANO = 100
    DEFENSA = 10
    VIDA = 500
    INTELIGENCIA = 10
    RESURECCION = 10000
    NIVEL = 1

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(VivoraJefe, self).__init__(mapa, media, x, y, ancho, alto, ['vivoraCaminar4.bmp', 'vivoraGolpear4.bmp'])
        self.items = ["Pocion", "Pocion", "Pocion", "Pocion", "Veneno", "Veneno"]

    def accion(self, accion):
        """Obtiene entrada del teclado para accionar al personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return
        if self != None and self.vida <= 0:
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            personajes.remove(self)
            eval(self.items[random.randint(0, 5)])(self.mapa, self.media, self.posicion[0], self.posicion[1], 40, 40)
            self = None
        if self != None and not self._golpeando and not self.vida < 0:
            atacando = self.viendoAPersonaje()
            if isinstance(self._golpeandoA, VivoraJefe): atacando = False
            if atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraJefe): self.golpear()
            if random.randint(1, 2) == 2 and not atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraJefe):
                if self.posicion[1] > 0:
                    if self.mapa.ocupado[self.posicion[1] - 1][self.posicion[0]] != None: self.mover(1)
                if self.posicion[1] < len(self.mapa.ocupado) - 1:
                    if self.mapa.ocupado[self.posicion[1] + 1][self.posicion[0]] != None: self.mover(2)
                if self.posicion[0] > 0:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] - 1] != None: self.mover(3)
                if self.posicion[0] < len(self.mapa.ocupado[0]) - 1:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] + 1] != None: self.mover(4)
            if random.randint(1, 4) == 3 and not atacando or isinstance(self._golpeandoA, VivoraJefe):
                self._dejarGolpear()
                movimiento = random.randint(1, 4)
                if movimiento == 1 and self.posicion[1] - 1 < self.inicial[1] - 8:
                    return
                if movimiento == 2 and self.posicion[1] + 1 > self.inicial[1] + 8:
                    return
                if movimiento == 3 and self.posicion[0] - 1 < self.inicial[0] - 8:
                    return
                if movimiento == 4 and self.posicion[0] + 1 > self.inicial[0] + 8:
                    return
                self.mover(movimiento)
        if self != None: self.animacion()

class Demonio(Personaje):

    VELOCIDAD = 10
    DANO = 100
    DEFENSA = 10
    VIDA = 500
    INTELIGENCIA = 10
    RESURECCION = 2000
    NIVEL = 1

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Demonio, self).__init__(mapa, media, x, y, ancho, alto, ['demonioCaminar.bmp', 'demonioGolpear.bmp'])
        self.items = ["Pocion", "Fuego", "Fuego", "Fuego", "Fuego", "Fuego"]

    def accion(self, accion):
        """Obtiene entrada del teclado para accionar al personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return
        if self != None and self.vida <= 0:
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            personajes.remove(self)
            eval(self.items[random.randint(0, 5)])(self.mapa, self.media, self.posicion[0], self.posicion[1], 40, 40)
            self = None
        if self != None and not self._golpeando and not self.vida < 0:
            atacando = self.viendoAPersonaje()
            if isinstance(self._golpeandoA, VivoraJefe): atacando = False
            if atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraJefe): self.golpear()
            if random.randint(1, 2) == 2 and not atacando and isinstance(self._golpeandoA, Personaje) and not isinstance(self._golpeandoA, VivoraJefe):
                if self.posicion[1] > 0:
                    if self.mapa.ocupado[self.posicion[1] - 1][self.posicion[0]] != None: self.mover(1)
                if self.posicion[1] < len(self.mapa.ocupado) - 1:
                    if self.mapa.ocupado[self.posicion[1] + 1][self.posicion[0]] != None: self.mover(2)
                if self.posicion[0] > 0:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] - 1] != None: self.mover(3)
                if self.posicion[0] < len(self.mapa.ocupado[0]) - 1:
                    if self.mapa.ocupado[self.posicion[1]][self.posicion[0] + 1] != None: self.mover(4)
            if random.randint(1, 4) == 3 and not atacando or isinstance(self._golpeandoA, VivoraJefe):
                self._dejarGolpear()
                movimiento = random.randint(1, 4)
                if movimiento == 1 and self.posicion[1] - 1 < self.inicial[1] - 8:
                    return
                if movimiento == 2 and self.posicion[1] + 1 > self.inicial[1] + 8:
                    return
                if movimiento == 3 and self.posicion[0] - 1 < self.inicial[0] - 8:
                    return
                if movimiento == 4 and self.posicion[0] + 1 > self.inicial[0] + 8:
                    return
                self.mover(movimiento)
        if self != None: self.animacion()

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        pass

class Humano(Personaje):

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Humano, self).__init__(mapa, media, x, y, ancho, alto, ['caminar.bmp', 'golpear.bmp'])
        self.vidaInicial = 10
        self.vida = self.vidaInicial

class Megaterio(Personaje):

    def __init__(self, mapa, media, x, y, ancho, alto):

        super(Megaterio, self).__init__(mapa, media, x, y, ancho, alto, ['megaterioCaminar.bmp', 'megaterioCaminar.bmp'])
        self.vidaInicial = 60
        self.vida = self.vidaInicial

class Neandertal(Personaje):

    def __init__(self, mapa, media, x, y):

        super(Neandertal, self).__init__(mapa, media, x, y)