#!/usr/bin/env python

import os, sys

try:
    from xml.dom.minidom import parse
except ImportError:
    print "Error: xml.dom.minidom module not found. Verify your python instalation."
    sys.exit(1)

try:
    import random
except ImportError:
    print "Error: random module not found. Verify your python instalation."
    sys.exit(1)

try:
    import pygame
except ImportError:
    print "Error: pygame module not installed. Install pygame module."
    sys.exit(1)

try:
    from pygame.locals import *
except ImportError:
    print "Error: pygame.locals not found. Verify your pygame instalation."
    sys.exit(1)

if os.path.isdir(sys.path[0]):
    os.chdir(sys.path[0])
sys.path.append("src")

from mediaManager import *
from ManejadorVentana import *
from ManejadorMapa import *
from ManejadorPersonaje import *
from Personaje import *
from Personajes import *
from Item import *
from Items import *
from ManejadorPersonajes import *
from ManejadorItems import *

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
media = loadMedia()
ventana = ManejadorVentana(pantalla)
background = media.loadImage(os.path.join('data', 'images', 'background', 'fondoNoche.png'))
logo = []
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessOne.png')))
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessTwo.png')))
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessThree.png')))
personajeInto = []
personajeInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'uno.png')))
personajeInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'dos.png')))
personajeInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'tres.png')))
fuente = pygame.font.SysFont("Courier New", 15)
fuente = fuente.render("Press Enter to continue or Esc to Exit.", 1, (255, 255, 255))
contTmp = 0
contSprite = 0
sonido = media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_no_survivors_.mid'))
#sonido.music.play(-1)
logoCentradoX = ventana.centrarItemX(logo[contSprite])
logoCentradoY = ventana.centrarItemY(logo[contSprite])
personajeCentradoX = ventana.centrarItemX(personajeInto[contSprite]) + logo[contSprite].get_width() / 2 - 10
personajeCentradoY = ventana.centrarItemY(personajeInto[contSprite]) + logo[contSprite].get_height() / 2 - 30
fuenteCentradaX = ventana.centrarItemX(fuente)
fuenteCentradaY = ventana.centrarItemY(fuente) + ventana.centrarItemX(logo[contSprite]) / 4
while 1:
    pygame.event.pump()
    keyInput = pygame.key.get_pressed()
    pantalla.blit(background, (0, 0))
    contTmp += 1
    flag = False
    if contTmp >= 1 and contTmp < 300 and not contSprite == 0:
        contSprite = 0
        flag = True
    elif contTmp >= 300 and contTmp < 600 and not contSprite == 1:
        contSprite = 1
        flag = True
    elif contTmp >= 600 and contTmp < 900 and not contSprite == 2:
        contSprite = 2
        flag = True
    elif contTmp >= 900 and contTmp < 1200 and not contSprite == 1:
        contSprite = 1
        flag = True
    elif contTmp == 1200:
        contTmp = 0
    if flag:
        pantalla.blit(logo[contSprite], (logoCentradoX, logoCentradoY))
        pantalla.blit(personajeInto[contSprite], (personajeCentradoX, personajeCentradoY))
        pantalla.blit(fuente, (fuenteCentradaX, fuenteCentradaY))
        pygame.display.update()
    if keyInput[K_RETURN]:
        break
    elif keyInput[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit()
pygame.time.delay(500)
sonido.music.stop()

sonido = media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_the_long_journey_home.mid'))
#sonido.music.play(-1)
azulejos = media.loadReadFile(os.path.join('data', 'maps', 'azulejos.xml'))
azulejosBloqueados = media.loadReadFile(os.path.join('data', 'maps', 'azulejosBloqueados.xml'))
azulejosGrandes = media.loadReadFile(os.path.join('data', 'maps', 'azulejosGrandes.xml'))
dungeonFile = media.loadReadFile(os.path.join('data', 'maps', 'demo.xml'))
mapa = ManejadorMapa(media, ventana, pantalla)
mapa.guardarAzulejos(azulejos)
mapa.guardarAzulejosBloqueados(azulejosBloqueados)
mapa.guardarAzulejosGrandes(azulejosGrandes)
mapa.guardarMapa(dungeonFile)
pantalla.blit(background, (0, 0))
dracko = ManejadorPersonaje(mapa, media, 0, 0, 40, 40)
pygame.display.update()
pygame.display.update()

items = []
[Piedra(mapa, media, random.randint(0, 15), random.randint(0, 20), 40, 40) for i in range(0, 2)]
[Pocion(mapa, media, random.randint(0, len(mapa.ocupado) - 2), random.randint(0, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 2)]
[Fuego(mapa, media, random.randint(0, len(mapa.ocupado) - 2), random.randint(0, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 2)]
[Pico(mapa, media, random.randint(0, len(mapa.ocupado) - 2), random.randint(0, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 2)]
[PicoFuerte(mapa, media, random.randint(0, len(mapa.ocupado) - 2), random.randint(0, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 2)]
[PicoRapido(mapa, media, random.randint(0, len(mapa.ocupado) - 2), random.randint(0, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 2)]

[Piedra(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 30)]
[Pocion(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 30)]
[Fuego(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 30)]
[Pico(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 30)]
[PicoFuerte(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 30)]
[PicoRapido(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 30)]

for item in Item.obtenerItems():
    items.append(item)
manejadorItems = ManejadorItems(items)

personajes = []
[Vivora(mapa, media, random.randint(0, 15), random.randint(0, 20), 40, 40) for i in range(0, 3)]
[VivoraRapida(mapa, media, random.randint(0, 15), random.randint(0, 20), 40, 40) for i in range(0, 3)]
[VivoraFuerte(mapa, media, random.randint(0, 15), random.randint(0, 20), 40, 40) for i in range(0, 3)]
[VivoraJefe(mapa, media, random.randint(0, 15), random.randint(0, 20), 40, 40) for i in range(0, 1)]
[Demonio(mapa, media, random.randint(0, 15), random.randint(0, 20), 40, 40) for i in range(0, 3)]

[Vivora(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 60)]
[VivoraRapida(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 60)]
[VivoraFuerte(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 60)]
[VivoraJefe(mapa, media, random.randint(16, len(mapa.ocupado) - 2), random.randint(21, len(mapa.ocupado[0]) - 2), 40, 40) for i in range(0, 20)]

for personaje in Personaje.obtenerPersonajes():
    personajes.append(personaje)
manejadorPersonajes = ManejadorPersonajes(personajes)

while 1:
    manejadorPersonajes.actualizarPersonajes()
    manejadorItems.actualizarItems()
    pygame.event.pump()
    keyInput = pygame.key.get_pressed()
    for personaje in Personaje.obtenerPersonajes():
        personaje.accion(keyInput)
    for item in Item.obtenerItems():
        item.animacion()
    dracko.accion(keyInput)
    if keyInput[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit()
    pantalla.blit(background, (0, 0))
    mapa.mostrarMapa(dracko, Item.obtenerItems(), Personaje.obtenerPersonajes())
    pygame.display.update()
    if dracko.vida <= 0:
        break

pygame.time.delay(500)
sonido.music.stop()