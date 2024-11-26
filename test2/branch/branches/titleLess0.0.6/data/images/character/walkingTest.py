#!/usr/bin/env python

import os, sys, random
import pygame
from pygame.locals import *

class loadMedia(object):
    """Handles media objects."""

    def __init__(self):
        """Loads all the media."""

        self._fullName = None

    def loadSound(self, name):
        """Loads the sound."""

        class NoneSound:
            def play(self): pass
            def stop(self): pass

        if not pygame.mixer:
            return NoneSound()
        self._fullName = name
        try:
            self._musicBox = pygame.mixer
            self._musicBox.init()
            self._musicBox.music.load(self._fullName)
            self._musicBox.music.set_volume(.7)
        except pygame.error, message:
            print "Can't Load sound file: ", self._fullName
            raise SystemExit, message
        return self._musicBox

    def loadImage(self, path, colorkey = None):
        """Load an image."""

        self._fullName = path
        try:
            self._image = pygame.image.load(self._fullName)
        except pygame.error, message:
            print "Can't Load Background: ", self._fullName
            raise SystemExit, message
        self._image  = self._image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = self._image.get_at((0, 0))
            self._image.set_colorkey(colorkey, RLEACCEL)
        return self._image

    def loadReadFile(self, name):
        """Loads a file."""

        self._filePath = name
        self._mapFile = open(self._filePath, 'r')
        return self._mapFile

pygame.init()
screen = pygame.display.set_mode((800, 600))
media = loadMedia()
background = media.loadImage(os.path.join('..', 'background', 'fondoNoche.png'))
mfrlBoth = media.loadImage(os.path.join('body', 'mfrlBoth.png'))
mfrlLeft = media.loadImage(os.path.join('body', 'mfrlLeft.png'))
mfrlRight = media.loadImage(os.path.join('body', 'mfrlRight.png'))
mbBoth = media.loadImage(os.path.join('eye', 'mbBoth.png'))
mbLeftRight = media.loadImage(os.path.join('eye', 'mbLeftRight.png'))
hBoth = media.loadImage(os.path.join('mouth', 'hBoth.png'))
hLeftRight = media.loadImage(os.path.join('mouth', 'hLeftRight.png'))
gaBoth = media.loadImage(os.path.join('shirt', 'gaBoth.png'))
gaLeftRight = media.loadImage(os.path.join('shirt', 'gaLeftRight.png'))
screen.blit(background, (0,0))
screen.blit(mfrlBoth, (70, 50))
screen.blit(mbBoth, (70, 50))
screen.blit(hBoth, (70, 50))
#screen.blit(gaBoth, (70, 50))
pygame.display.update()
dummyCount = 1
while 1:
    pygame.event.pump()
    keyInput = pygame.key.get_pressed()
    screen.blit(background, (0,0))
    if dummyCount == 1:
        screen.blit(mfrlRight, (70, 50))
        screen.blit(mbLeftRight, (70, 50))
        screen.blit(hLeftRight, (70, 50))
        #screen.blit(gaLeftRight, (70, 50))
        dummyCount += 1
    elif dummyCount == 2:
        screen.blit(mfrlBoth, (70, 50))
        screen.blit(mbBoth, (70, 50))
        screen.blit(hBoth, (70, 50))
        screen.blit(hBoth, (70, 50))
        #screen.blit(gaBoth, (70, 50))
        dummyCount += 1
    elif dummyCount == 3:
        screen.blit(mfrlLeft, (70, 50))
        screen.blit(mbLeftRight, (70, 50))
        screen.blit(hLeftRight, (70, 50))
        #screen.blit(gaLeftRight, (70, 50))
        dummyCount += 1
    elif dummyCount == 4:
        screen.blit(mfrlBoth, (70, 50))
        screen.blit(mbBoth, (70, 50))
        screen.blit(hBoth, (70, 50))
        #screen.blit(gaBoth, (70, 50))
        dummyCount = 1
    if keyInput[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit()
    pygame.time.delay(500)
    pygame.display.update()
