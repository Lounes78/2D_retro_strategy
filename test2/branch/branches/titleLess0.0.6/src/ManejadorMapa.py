import os, sys, random
import pygame
from pygame.locals import *
from xml.dom.minidom import parse

class ManejadorMapa(object):

    def __init__(self, media, windowManager, screen):
        """Maneja el mapa."""

        #self._windowManager = windowManager
        self._media = media
        self._ventana = screen
        self._azulejos = {}
        #self._rowTmp = 0
        #self._colTmp = 0
        #self._tmpAnimateSprite = 0
        #self._uglyPatch = True
        #self._row = []
        #self._rowTwo = []
        self.mapa = []
        self.elevacion = []
        self.ocupado = []
        self.items = []

    def guardarAzulejos(self, archivo):
        """Guarda los azulejos."""

        archivoAzulejos = parse(archivo)
        listaAzulejos = archivoAzulejos.getElementsByTagName('azulejo')
        for azulejo in listaAzulejos:
            self._azulejos[azulejo.childNodes[0].nodeValue] = self._media.loadImage(os.path.join('data', 'images', 'terrain', azulejo.childNodes[0].nodeValue + '.png'), -1)
            self._azulejos[azulejo.childNodes[0].nodeValue].convert()

    def guardarAzulejosBloqueados(self, archivo):
        """Guarda los azulejos bloqueados."""

        self._azulejosBloqueados = []
        archivoAzulejos = parse(archivo)
        listaAzulejos = archivoAzulejos.getElementsByTagName('azulejo')
        for azulejo in listaAzulejos:
            self._azulejosBloqueados.append(azulejo.childNodes[0].nodeValue)

    def guardarAzulejosGrandes(self, archivo):
        """Guarda los azulejos grandes."""

        self._azulejosGrandes = []
        archivoAzulejos = parse(archivo)
        listaAzulejos = archivoAzulejos.getElementsByTagName('azulejo')
        for azulejo in listaAzulejos:
            self._azulejosGrandes.append(azulejo.childNodes[0].nodeValue)

    def guardarMapa(self, archivo, posicion = 0):
        """Guarda el mapa."""

        self._mapa = []
        archivoMapa = parse(archivo)
        filasMapa = archivoMapa.getElementsByTagName('fila')
        for fila in filasMapa:
            columnasMapa = fila.getElementsByTagName('columna')
            filaMapa = []
            filaAlturaMapa = []
            filaOcupado = []
            filaItem = []
            for columna in columnasMapa:
                filaMapa.append(columna.childNodes[0].nodeName)
                filaAlturaMapa.append(columna.childNodes[0].attributes['altura'].value)
                filaOcupado.append(None)
                filaItem.append(None)
            self.mapa.append(filaMapa)
            self.elevacion.append(filaAlturaMapa)
            self.ocupado.append(filaOcupado)
            self.items.append(filaItem)

    def mostrarMapa(self, sprite = None, items = None, personajes = None):
        """Dibuja el mapa junto con personajes e items."""

        x = 20
        y = 10
        inicioX = 0
        inicioY = 0
        azulejoGrande = azulejoElevacion = 0
        posicionX = posicionY = -1
        scrollMapaX = 0
        scrollMapaY = 0
        ventanaDibujada = pygame.Surface([self._ventana.get_width(), self._ventana.get_height()])
        if sprite:
            scrollMapaX = sprite.scrollMapaX
            scrollMapaY = sprite.scrollMapaY
        for fila in self.mapa[scrollMapaY:]:
            posicionY += 1
            posicionX = -1
            if 380 - (posicionY * x) + (posicionX * x) < -20:
                break
            for azulejo in fila[scrollMapaX:]:
                posicionX += 1
                if int(self.elevacion[posicionY + scrollMapaY][posicionX + scrollMapaX]) > 1:
                    for self.elevacionPos in range(0, int(self.elevacion[posicionY + scrollMapaY][posicionX + scrollMapaX]) - 1):
                        self._ventana.blit(self._azulejos["baseTierra"], (380 - (posicionY * x) + (posicionX * x), 180 + (posicionY * y) + (posicionX * y) - (20 * (int(self.elevacionPos)))))
                    azulejoElevacion -=  20 * int(int(self.elevacion[posicionY + scrollMapaY][posicionX + scrollMapaX]) - 1)
                if self.mapa[posicionY + scrollMapaY][posicionX + scrollMapaX] in self._azulejosGrandes:
                    azulejoGrande -= 80
                if not 380 - (posicionY * x) + (posicionX * x) > 760 - (posicionY * 19):
                    self._ventana.blit(self._azulejos[azulejo], (380 - (posicionY * x) + (posicionX * x), 180 + (posicionY * y) + (posicionX * y) + azulejoGrande + azulejoElevacion))
                    if personajes:
                        for personaje in personajes:
                            if posicionX + scrollMapaX == personaje.posicion[0] and posicionY + scrollMapaY == personaje.posicion[1]:
                                self._ventana.blit(personaje.spriteActual, (380 - (posicionY * x) + ((posicionX) * x), 180 + (posicionY * y) + ((posicionX) * y) - 20 + azulejoElevacion))
                    if sprite:
                        if posicionX + scrollMapaX == sprite.posicion[0] and posicionY + scrollMapaY == sprite.posicion[1]:
                            self._ventana.blit(sprite.spriteActual, (380 - (posicionY * x) + ((posicionX) * x), 180 + (posicionY * y) + ((posicionX) * y) - 20 + azulejoElevacion))
                    if items:
                        for item in items:
                            if posicionX + scrollMapaX == item.posicion[0] and posicionY + scrollMapaY == item.posicion[1]:
                                self._ventana.blit(item.spriteActual, (380 - (posicionY * x) + ((posicionX) * x), 180 + (posicionY * y) + ((posicionX) * y) - 20 + azulejoElevacion))
                azulejoGrande = 0
                azulejoElevacion = 0