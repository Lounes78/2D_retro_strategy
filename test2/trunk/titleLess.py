#!/usr/bin/env python

import os, sys, random
import pygame
from pygame.locals import *

if os.path.isdir(sys.path[0]):
    os.chdir(sys.path[0])
sys.path.append("src")

from mediaManager import *
from windowManager import *
from dungeonManager import *
from spriteManager import *

# Pygame initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))


# Loading multiple things
media = loadMedia()
windowManager = windowManager(screen)
background = media.loadImage(os.path.join('data', 'images', 'background', 'firstDungeon.png'))
logo = []
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessOne.png')))
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessTwo.png')))
logo.append(media.loadImage(os.path.join('data', 'logo', 'titleLessThree.png')))
characterInto = []
characterInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoOne.png')))
characterInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackotwo.png')))
characterInto.append(media.loadImage(os.path.join('data', 'images', 'character', 'frontLeftDrackoThree.png')))
font = pygame.font.SysFont("Courier New", 15)
font = font.render("Press Enter to continue or Esc to Exit.", 1, (255, 255, 255))
sound = media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_no_survivors_.mid'))
sound.music.play(-1)


# Positionement of the elements (logos, heros, text) 
dummyCounter = 0
spriteCounter = 0
# Logo
centeredLogoX = windowManager.centerItemX(logo[spriteCounter])
centeredLogoY = windowManager.centerItemY(logo[spriteCounter])
# Character
centeredCharacterX = windowManager.centerItemX(characterInto[spriteCounter]) + logo[spriteCounter].get_width() / 2 - 10
centeredCharacterY = windowManager.centerItemY(characterInto[spriteCounter]) + logo[spriteCounter].get_height() / 2 - 30
# Font
centerFontX = windowManager.centerItemX(font)
centerFontY = windowManager.centerItemY(font) + windowManager.centerItemX(logo[spriteCounter]) / 4


while 1:  # First loop for the hello screen 
    pygame.event.pump()
    keyInput = pygame.key.get_pressed() # returns a list of all keys' states
    screen.blit(background, (0, 0))
    dummyCounter += 1
    flag = False
    if dummyCounter >= 1 and dummyCounter < 300 and not spriteCounter == 0:
        spriteCounter = 0
        flag = True
    elif dummyCounter >= 300 and dummyCounter < 600 and not spriteCounter == 1:
        spriteCounter = 1
        flag = True
    elif dummyCounter >= 600 and dummyCounter < 900 and not spriteCounter == 2:
        spriteCounter = 2
        flag = True
    elif dummyCounter >= 900 and dummyCounter < 1200 and not spriteCounter == 1:
        spriteCounter = 1
        flag = True
    elif dummyCounter == 1200:
        dummyCounter = 0
        
    if flag:
        screen.blit(logo[spriteCounter], (centeredLogoX, centeredLogoY))
        screen.blit(characterInto[spriteCounter], (centeredCharacterX, centeredCharacterY))
        screen.blit(font, (centerFontX, centerFontY))
        pygame.display.update() # Update the content of the screen 
    if keyInput[K_RETURN]:
        break
    elif keyInput[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit()
        
        
# Loading the game
pygame.time.delay(500)
sound.music.stop()
sound = media.loadSound(os.path.join('data', 'music', 'bjorn__lynne-_the_long_journey_home.mid'))
sound.music.play(-1)

tildeFile = media.loadReadFile(os.path.join('data', 'maps', 'tiles.txt'))
dungeonFile = media.loadReadFile(os.path.join('data', 'maps', 'firstDungeon.txt'))
nwTiles = media.loadReadFile(os.path.join('data', 'maps', 'tiles.txt'))

firstDungeon = dungeonManager(media, windowManager, screen)
firstDungeon.recordNonWalkableTiles(nwTiles)
firstDungeon.recordTiles(tildeFile)
firstDungeon.recordDungeon(dungeonFile)

screen.blit(background, (0, 0))
dracko = spriteManager(firstDungeon, media)
pygame.display.update()


while 1:
    pygame.event.pump()
    keyInput = pygame.key.get_pressed()
    if keyInput[K_UP]:
        dracko.update(1)
    elif keyInput[K_DOWN]:
        dracko.update(2)
    elif keyInput[K_LEFT]:
        dracko.update(3)
    elif keyInput[K_RIGHT]:
        dracko.update(4)
    if keyInput[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit()
    screen.blit(background, (0, 0))
    firstDungeon.fillDungeon(dracko)
    pygame.display.update()
    pygame.time.delay(25)  # for the speed 
sound.music.stop()
pygame.time.delay(1000)
