import os, sys, random
import pygame
from pygame.locals import *

from Item import *

class Personaje(pygame.sprite.Sprite):

    global personajes
    personajes = pygame.sprite.Group()

    VELOCIDAD = 10
    DANO = 10
    DEFENSA = 10
    VIDA = 10
    INTELIGENCIA = 10
    RESURECCION = 10000
    NIVEL = 1

    def __init__(self, mapa, media, x, y, ancho, alto, archivosSprites):

        pygame.sprite.Sprite.__init__(self)
        self.sprite = None
        self.mapa = mapa
        self.media = media
        self.spriteActual = pygame.Surface([ancho, alto])
        self._spriteIndice = 0
        self.inicial = [x, y]
        #se puede ciclar infinito
        while self.mapa.mapa[y][x] in self.mapa._azulejosBloqueados or self.mapa.ocupado[y][x] != None:
            if x >= 3 and x < len(mapa.ocupado[0]) - 3: x = random.randint(x - 3, x + 3)
            if y >= 0 and y < len(mapa.ocupado) - 3: y = random.randint(y - 3, y + 3)
        self.mapa.ocupado[y][x] = self
        self.posicion = [x, y]
        self._golpeando = False
        self._golpeado = False
        self._direccion = 0
        self.vidaInicial = self.VIDA
        self.vida = self.vidaInicial
        self.dano = self.DANO
        self.defensa = self.DEFENSA
        self.velocidad = self.VELOCIDAD
        self.inteligencia = self.INTELIGENCIA
        self._contadorAccion = self.VELOCIDAD
        self.contadorBajar = 0
        sprites = self.media.loadImage(os.path.join('data', 'images', 'character', 'body', archivosSprites[0])).convert()
        sprites.set_colorkey(sprites.get_at((0,0)), RLEACCEL)
        spritesAncho, spritesAlto = sprites.get_size()
        self.personajeCaminando = []
        self._animacionSeq = 1
        self._enAgua = 0
        self._golpeandoA = None
        personajes.add(self)
        for i in xrange(int(spritesAlto/alto)):
            self.personajeCaminando.append([])
            for j in xrange(int(spritesAncho/ancho)):
                self.personajeCaminando[i].append(sprites.subsurface(j * ancho, i * alto, ancho, alto))
        sprites = self.media.loadImage(os.path.join('data', 'images', 'character', 'body', archivosSprites[1])).convert()
        sprites.set_colorkey(sprites.get_at((0,0)), RLEACCEL)
        spritesAncho, spritesAlto = sprites.get_size()
        self.personajeGolpeando = []
        self._animacionSeq = 1
        self._golpeando = False
        for i in xrange(int(spritesAlto/alto)):
            self.personajeGolpeando.append([])
            for j in xrange(int(spritesAncho/ancho)):
                self.personajeGolpeando[i].append(sprites.subsurface(j * ancho, i * alto, ancho, alto))
        self.personaje = self.personajeCaminando
        self.sprite = self.personaje[0][1]
        if self._estaEnAgua():
            self.sprite = self.personaje[0][4]
        self.rect = self.spriteActual.get_rect()

    def mover(self, direccion):
        """Actualiza la posicion del personaje."""

        incX = incY = 0
        if direccion is 1:
            self._direccion = 2
            if self.posicion[1] > 0:
                incY = -1
                incX = 0
        elif direccion is 2:
            self._direccion = 1
            if self.posicion[1] < len([fila[self.posicion[0]] for fila in self.mapa.mapa]) - 1:
                incY = 1
                incX = 0
        elif direccion is 3:
            self._direccion = 3
            if self.posicion[0] > 0:
                incY = 0
                incX = -1
        elif direccion is 4:
            self._direccion = 0
            if self.posicion[0] < len(self.mapa.mapa[self.posicion[1]]) - 1:
                incY = 0
                incX = 1
        if incX != 0 or incY != 0: self.contadorBajar = 0
        if not self._siguienteBloqueado(incY, incX) and not self._siguienteAlto(incY, incX) and not self._siguienteOcupado(incY, incX):
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            self.posicion[1] += incY
            self.posicion[0] += incX
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = self
        self._estaEnAgua()

    def _siguienteBloqueado(self, fila, columna):
        """Valida si el siguiente azulejo es valido para caminar."""

        if self.mapa.mapa[self.posicion[1] + fila][self.posicion[0] + columna] in self.mapa._azulejosBloqueados:
            return True
        else:
            return False

    def _siguienteAlto(self, fila, columna):
        """Valida que la diferencia entre elevacion no sea grande."""

        self._validation = int(self.mapa.elevacion[self.posicion[1]][self.posicion[0]]) - int(self.mapa.elevacion[self.posicion[1] + fila][self.posicion[0] + columna])
        if self._validation > 1 or self._validation < -1:
            return True
        else:
            return False

    def _siguienteOcupado(self, fila, columna):

        if self.mapa.ocupado[self.posicion[1] + fila][self.posicion[0] + columna] != None:
            return True
        else:
            return False

    def _estaEnAgua(self):
        """Valida si el personaje esta en agua."""

        if self.mapa.mapa[self.posicion[1]][self.posicion[0]] == "agua":
            self._enAgua = 3
            return True
        else:
            self._enAgua = 0
            return False

    def accion(self, accion):
        """Obtiene entrada del teclado para accionar al personaje."""

        if self._contadorAccion >= self.VELOCIDAD:
            self._contadorAccion = 0
        else:
            self._contadorAccion += 1
            return
        if self != None and self.vida < 0:
            self.mapa.ocupado[self.posicion[1]][self.posicion[0]] = None
            personajes.remove(self)
            self = None
        if self != None and not self._golpeando and not self.vida < 0:
            if random.randint(1, 6) == 3 and isinstance(self._golpeandoA, Personaje):
                self.golpear()
            if random.randint(1, 6) == 3:
                self.mover(random.randint(0, 4))
        if self != None: self.animacion()

    def golpear(self):

        if not self._golpeando:
            viendo = self.ver()
            self.viendoAPersonaje()
            if self._golpeandoA != self and self._golpeandoA != None and abs(int(self.mapa.elevacion[self._golpeandoA.posicion[1]][self._golpeandoA.posicion[0]]) - int(self.mapa.elevacion[self.posicion[1]][self.posicion[0]])) < 2:
                if isinstance(self._golpeandoA, Personaje):
                    self._golpeandoA._siendoGolpeado(self.DANO)
                    self._golpeandoA = None
            self._golpeando = True
            self.personaje = self.personajeGolpeando
            self._spriteIndice = 0

    def _siendoGolpeado(self, dano):

        try:
            self.vida -= dano
            self._golpeado = True
            fuente = pygame.font.SysFont("Courier New", 8, True)
            fuente = fuente.render(str((dano * -1)), 0, (0, 0, 0), (255, 255, 255))
            self.spriteActual.blit(fuente, (self.spriteActual.get_width() / 2 - len(str((dano * -1))), 4))
        except:
            pass

    def _dejarGolpear(self):

        if self._golpeandoA != None:
            self._golpeandoA._golpeado = False
        self._golpeandoA = None

    def animacion(self):
        """Crea la animacion del personaje."""

        self.spriteActual = pygame.Surface.copy(self.personaje[self._direccion][self._spriteIndice + self._enAgua])
        if self.juntoAPersonaje() or self._golpeado:
            pygame.draw.polygon(self.spriteActual, (0, 0, 0), ((6, 0), (4, 4), (self.spriteActual.get_width() - 6, 4), (self.spriteActual.get_width() - 4, 0)))
            pygame.draw.polygon(self.spriteActual, (255, 0, 0), ((8, 1), (6, 3), (self.spriteActual.get_width() - 7, 3), (self.spriteActual.get_width() - 5, 1)))
            if self.vida >= 0:
                pygame.draw.polygon(self.spriteActual, (0, 255, 0), ((8, 1), (6, 3), (((((self.vida * 100) / self.vidaInicial) * (self.spriteActual.get_width() - 13)) / 100) + 6, 3), (((((self.vida * 100) / self.vidaInicial) * (self.spriteActual.get_width() - 13)) / 100) + 8, 1)))
        if self._spriteIndice == 2:
            self._animacionSeq = -1
        elif self._spriteIndice == 0:
            self._animacionSeq = 1
        self._spriteIndice += self._animacionSeq
        if self._golpeando and self._spriteIndice == 0:
            self._golpeando = False
            self.personaje = self.personajeCaminando
            self._dejarGolpear()
        self._golpeado = False
        self.rect = self.spriteActual.get_rect()
        if isinstance(self.mapa.items[self.posicion[1]][self.posicion[0]], Item):
            item = self.mapa.items[self.posicion[1]][self.posicion[0]]
            if item.accion == 'recuperaVida' and self.vida < self.vidaInicial:
                if item.eliminarItem():
                    self.mapa.items[self.posicion[1]][self.posicion[0]] = None
                if item.valor > self.vidaInicial - self.vida: self._siendoGolpeado(-(self.vidaInicial - self.vida))
                else: self._siendoGolpeado(-item.valor)
            if item.accion == 'quitaVida':
                if self.contadorBajar == 0:
                    if self.vida - item.valor < 0: self.vida = self._siendoGolpeado(self.vida)
                    else: self._siendoGolpeado(item.valor)
                    if item.eliminarItem():
                        self.mapa.items[self.posicion[1]][self.posicion[0]] = None
                self.contadorBajar += 1
                if self.contadorBajar > item.VELOCIDAD: self.contadorBajar = 0
        else:
            self.contadorBajar = 0

    def viendoAPersonaje(self):

        viendo = self.ver()
        if self.mapa.ocupado[viendo[1]][viendo[0]] != self and self.mapa.ocupado[viendo[1]][viendo[0]] != None and abs(int(self.mapa.elevacion[viendo[1]][viendo[0]]) - int(self.mapa.elevacion[self.posicion[1]][self.posicion[0]])) < 2 and isinstance(self.mapa.ocupado[viendo[1]][viendo[0]], Personaje):
            self._golpeandoA = self.mapa.ocupado[viendo[1]][viendo[0]]
            return True
        self._golpeandA = None
        return False

    def juntoAPersonaje(self):

        if self.posicion[1] > 0:
            if isinstance(self.mapa.ocupado[self.posicion[1] - 1][self.posicion[0]], Personaje): return True
        if self.posicion[1] < len(self.mapa.ocupado) - 1:
            if isinstance(self.mapa.ocupado[self.posicion[1] + 1][self.posicion[0]], Personaje): return True
        if self.posicion[0] > 0:
            if isinstance(self.mapa.ocupado[self.posicion[1]][self.posicion[0] - 1], Personaje): return True
        if self.posicion[0] < len(self.mapa.ocupado[0]) - 1:
            if isinstance(self.mapa.ocupado[self.posicion[1]][self.posicion[0] + 1], Personaje): return True
        return False

    def ver(self):

        viendo = [self.posicion[0], self.posicion[1]]
        if self._direccion == 2 and self.posicion[1] > 0: viendo = [self.posicion[0], self.posicion[1] - 1]
        if self._direccion == 1 and self.posicion[1] < len(self.mapa.ocupado) - 1: viendo = [self.posicion[0], self.posicion[1] + 1]
        if self._direccion == 3 and self.posicion[0] > 0: viendo = [self.posicion[0] - 1, self.posicion[1]]
        if self._direccion == 0 and self.posicion[0] < len(self.mapa.ocupado[0]) - 1: viendo = [self.posicion[0] + 1, self.posicion[1]]
        return viendo

    def subirNivel(self):

        pass

    @staticmethod
    def obtenerPersonajes():

        return personajes