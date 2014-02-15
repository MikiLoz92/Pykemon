# coding: utf-8

import pygame
from maps import *

class Special:

	def __init__(self):
		self.instanceList = []
	def update(self):
		pass


class Room:

	def __init__(self,content,instanceList=[],recursivity=True):
		# El contenido de la room, si es un mapa, una instancia de tipo Map(), si es una room especial, una instancia de tipo Special()
		self.content = content
		# Lista de instancias de la room
		if isinstance(self.content,Map):
			self.instanceList = self.content.instanceList
			if recursivity:
				self.nextRoom = [None]*4
				print self.nextRoom
				for i in range(4):
					if self.content.limits[i] != None:
						self.nextRoom[i] = Room(Map(self.content.limits[i] + ".tmx"), [], False)
			self.width = self.content.width
			self.height = self.content.height
			self.visibleInstances = pygame.sprite.Group()
			self.instanceMap = [[None for _ in range(self.width)] for _ in range(self.height)]
			self.permissionMap = [[0 for _ in range(self.width)] for _ in range(self.height)]
			for i in self.instanceList:
				try:
					if i.image != None:
						self.visibleInstances.add(i)
				except:
					pass
				self.instanceMap[i.tilePos[1]][i.tilePos[0]] = i
				self.permissionMap[i.tilePos[1]][i.tilePos[0]] = 1
		else:
			self.instanceList = instanceList
		self.roomSurfaces = self.getSurfaces()

	def update(self):
		self.instanceMap = [[None for _ in range(self.width)] for _ in range(self.height)]
		self.permissionMap = [[0 for _ in range(self.width)] for _ in range(self.height)]
		for i in self.instanceList:
			self.instanceMap[i.tilePos[1]][i.tilePos[0]] = i
			self.permissionMap[i.tilePos[1]][i.tilePos[0]] = 1

	def returnTile(self,hero,layer):
		return self.content.map[layer][hero.tilePos[1]][hero.tilePos[0]]

	def returnTileDepth(self,hero):
		depth = 0
		for i in range(len(self.content.map)):
			if self.returnTile(self,hero,i) != 0:
				depth = self.content.tileDepth[self.returnTile(self,hero,i)-1]
		return depth

	def getSurfaces(self):
		"""
		Devuelve una lista con los 2 Surfaces que debe dibujar en la pantalla, uno por
		debajo y otro por encima del héroe.
		"""
		l = [ pygame.Surface((len(self.content.map[0])*16,len(self.content.map[0][0])*16)),
			  pygame.Surface((len(self.content.map[0])*16,len(self.content.map[0][0])*16),pygame.SRCALPHA) ]
		l[0] = l[0].convert_alpha()
		l[1] = l[1].convert_alpha()
		for i in range(len(self.content.map)-1):
			y = 0
			for j in self.content.map[i]:
				x = 0
				for k in j:
					# Las tiles vacías en el Tiled se representan con un 0: aquí serán un -1.
					if k != -1:
						l[0].blit(self.content.tileset.t[k].convert_alpha(),(x,y))
					x += pygame.Surface.get_width(self.content.tileset.t[0])	
				y += pygame.Surface.get_height(self.content.tileset.t[0])
		for i in range(self.content.heroLayer+1,len(self.content.map)):
			y = 0
			for j in self.content.map[i]:
				x = 0
				for k in j:
					# Las tiles vacías en el Tiled se representan con un 0: aquí serán un -1.
					if k != -1:
						l[1].blit(self.content.tileset.t[k].convert_alpha(),(x,y))
					x += pygame.Surface.get_width(self.content.tileset.t[0])	
				y += pygame.Surface.get_height(self.content.tileset.t[0])
		return l

	def getBoundarySurfaces(self):
		"""
		Devuelve el Surface que representa la zona inaccesible del mapa, en los alrededores.
		"""