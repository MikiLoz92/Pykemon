# coding: utf-8

import pygame

from maps import *
from objects import *
from rooms import *
from keyboard import *
from hero import *
from classes import *

from time import sleep

gc = GameContext( Screen((288,192),2,False) , Hero() , Keyboard() )
clock = pygame.time.Clock()

while not gc.quit:
	
	gc.update()

	# Dibujamos el buffer en la pantalla y lo limpiamos
	pygame.transform.scale(gc.screen.screenBuffer,gc.screen.windowSize,gc.screen.screen)
	gc.screen.screenBuffer = pygame.Surface(gc.screen.size)
	# Controlamos el framerate
	clock.tick(60)

	# Refrescamos la pantalla
	pygame.display.flip()