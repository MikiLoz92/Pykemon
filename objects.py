# coding: utf-8

import pygame
import xml.etree.ElementTree as ET
import random

class RoomObject(pygame.sprite.Sprite):
	def __init__(self):
		"""
		Código que se carga nada más iniciar el mapa e instanciar el objeto. ¡SI DA PROBLEMAS: ELIMINAR!
		"""
		pygame.sprite.Sprite.__init__(self)
	def update(self, gc):
		"""
		Código que se ejecuta a cada momento del juego mientras el objeto esté instanciado y en el mapa actual.
		"""
		pass
	def onTalk(self, gc):
		"""
		Código que se ejecuta cuando el héroe habla con este objeto.
		"""
		pass
	def onWalk(self, gc):
		"""
		Código que se ejecuta cuando el héroe llega al tile donde está este objeto.
		"""
		pass
	def onTouch(self, gc):
		"""
		Código que se ejecuta cuando el héroe intenta avanzar al tile donde está este objeto.
		"""
		pass

class Animated(RoomObject):
	def __init__(self, spritesheet="005"):
		pygame.sprite.Sprite.__init__(self)
		self.spritesheet = pygame.image.load("sprites/"+spritesheet+".png")
		self.images = ripSpriteSheet(self.spritesheet)
		self.facing = 1
		self.image = self.images[self.facing][0]
		# Posición del rectángulo 16x16 en cada cuadrícula de sprites de 32x32
		self.spritesheetPos = [7,15]
		self.onGrass = False
	def update(self, gc):
		rand = random.randint(0,59)
		if rand == 0:
			self.facing = random.randint(0,3)
		self.image = self.images[self.facing][0]


class Warp(RoomObject):
	def onContact(self):
		gc.currentMap = True

class Text(RoomObject):
	pass

typeToClass = {"Text": Text}

# Ejemplo de RoomObject, un árbol que cada 10 segundos (600f) pierde las hojas.
class Arbol(RoomObject):
	def __init__(self):
		self.hojas = True
		self.timer = 600
	def update(self):
		if self.timer == 0:
			self.hojas = False
			self.timer = 600
		else:
			self.timer -= 1
			self.hojas = True
	def onTalk(self):
		gc.showMessage("Perderé las hojas en " + self.timer/60.0 + " segundos.")

def ripSpriteSheet(s):
	"""
	Dado un Surface que representa un spritesheet, lo ripea y devuelve una matriz 4x4 de Surfaces.
	"""
	images = []
	for i in range(4):
		images.append([])
		for j in range(4):
			tempS = pygame.Surface((32,32),pygame.SRCALPHA)
			tempS.blit(s,(0,0),(32*j,32*i,32,32))
			images[i].append(tempS)
	images.insert(0,images[3])
	del images[4]
	return images