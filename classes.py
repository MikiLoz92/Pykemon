# coding: utf-8

import pygame
from rooms import *
from maps import *
from keyboard import *
from hero import *


class Screen:

	def __init__(self,(w,h),scale,full):
		self.size = [w,h]
		self.scale = scale
		self.windowSize = [w*scale,h*scale]
		self.full = full
		self.viewPos = [0,0]
		pygame.display.init()
		pygame.font.init()
		pygame.display.set_caption("The Pykemon Engine")
		self.screen = pygame.display.set_mode((self.size[0]*self.scale,self.size[1]*self.scale), pygame.DOUBLEBUF, 32)
		self.screenBuffer = pygame.Surface(self.size)

	def changeSize(self,how):
		pygame.display.quit()
		pygame.display.init()
		self.size[0] += how*32
		self.size[1] += how*32
		self.windowSize = [self.size[0]*self.scale,self.size[1]*self.scale]
		self.screen = pygame.display.set_mode((self.size[0]*self.scale,self.size[1]*self.scale), pygame.DOUBLEBUF, 32)
		self.screenBuffer = pygame.Surface(self.size)

	def increaseSize(self):
		self.changeSize(1)

	def decreaseSize(self):
		self.changeSize(-1)


class GameContext:

	def __init__(self, screen=Screen((240,144),2,False), hero=Hero(), key = Keyboard()):
		self.screen = screen
		 # Música
		pygame.mixer.pre_init(44100,-16,2,1024)
		pygame.mixer.init()
		pygame.mixer.music.load("music/littleroot_final.mp3")
		pygame.mixer.music.play(-1)
		
		self.room = Room(Map("004.tmx"),[])
		self.hero = hero
		self.key = key
		self.quit = False
		self.screen.viewPos = [-self.hero.tilePos[0]*16+(self.screen.size[0]/16-1)/2*16,-self.hero.tilePos[1]*16+(self.screen.size[1]/16-1)/2*16]

	def update(self):
		############################
		##### 1 - Parte lógica #####
		############################
		# Comprobamos si hay que salir del juego y ya de paso actualizamos el teclado
		self.key.update(self)
		#print self.room.content.instanceList

		#############################
		##### 2 - Parte gráfica #####
		#############################
		# Dibujamos la room y todo lo que contiene en el buffer. Dibujamos al héroe
		if isinstance(self.room.content, Map):
			# Actualizamos el héroe
			self.hero.update(self.key, self.room)	
			# Dibujamos el mapa que hay por debajo del héroe
			self.screen.screenBuffer.blit(self.room.roomSurfaces[0].convert_alpha(),self.screen.viewPos)
			# Posicionamiento de las siguiente rooms (BETA)
			if self.room.nextRoom[0] != None:
				nextRoomPos = (self.screen.viewPos[0], self.screen.viewPos[1]-self.room.nextRoom[0].height*16)
				self.screen.screenBuffer.blit(self.room.nextRoom[0].roomSurfaces[0],nextRoomPos,(0,0,self.room.nextRoom[0].width*16,self.room.nextRoom[0].height*16))
				self.screen.screenBuffer.blit(self.room.nextRoom[0].roomSurfaces[1].convert_alpha(),nextRoomPos,(0,0,self.room.nextRoom[0].width*16,self.room.nextRoom[0].height*16))
			if self.room.nextRoom[1] != None:
				nextRoomPos = (self.screen.viewPos[0], self.screen.viewPos[1]+self.room.nextRoom[1].height*16-32)
				self.screen.screenBuffer.blit(self.room.nextRoom[1].roomSurfaces[0],nextRoomPos,(0,0,self.room.nextRoom[1].width*16,self.room.nextRoom[1].height*16))
				self.screen.screenBuffer.blit(self.room.nextRoom[1].roomSurfaces[1].convert_alpha(),nextRoomPos,(0,0,self.room.nextRoom[1].width*16,self.room.nextRoom[1].height*16))
			if self.room.nextRoom[2] != None:
				nextRoomPos = (self.screen.viewPos[0]-self.room.nextRoom[2].width*16, self.screen.viewPos[1])
				self.screen.screenBuffer.blit(self.room.nextRoom[2].roomSurfaces[0].convert_alpha(),nextRoomPos,(0,0,self.room.nextRoom[2].width*16,self.room.nextRoom[2].height*16))
			if self.room.nextRoom[3] != None:
				nextRoomPos = (self.screen.viewPos[0]+self.room.nextRoom[3].width*16-32, self.screen.viewPos[1])
				self.screen.screenBuffer.blit(self.room.nextRoom[3].roomSurfaces[0].convert_alpha(),nextRoomPos,(0,0,self.room.nextRoom[3].width*16,self.room.nextRoom[3].height*16))
			# Actualizamos y dibujamos las instancias por encima del héroe
			bottomInstances = []
			for i in self.room.instanceList:
				i.update(self)
				if i in self.room.visibleInstances:
					if i.tilePos[1] < self.hero.tilePos[1]:
						self.drawOnRoom(i)
					else:
						bottomInstances.append(i)
			# Dibujamos al héroe
			self.drawOnRoom(self.hero)
			# Dibujamos las instancias por debajo del héroe
			for i in bottomInstances:
				self.drawOnRoom(i)
			# Actualizamos la room
			self.room.update()
			# Comprobamos si se pisa, toca o habla con alguna instancia
			for i in self.room.instanceList:
				if self.key.keyPressed["A"] and self.hero.facingTile() == i.tilePos:
					i.onTalk(self)
			# Dibujamos el mapa que hay por encima del héroe
			self.screen.screenBuffer.blit(self.room.roomSurfaces[1].convert_alpha(),self.screen.viewPos)
			# Dibujamos un texto de prueba ((DEBUG))
			self.font = pygame.font.SysFont("Monospace",10)
			textSurface = self.font.render("Esto es una prueba.",True,(0,0,0))
			self.screen.screenBuffer.blit(textSurface,(0,0))
			# Seguimos al héroe con el view
			self.screen.viewPos = [-self.hero.rect.x+(self.screen.size[0]/16-1)/2*16,-self.hero.rect.y+(self.screen.size[1]/16-1)/2*16]

	def drawOnRoom(self,instance):
		"""
		Dibuja un objeto (sprite) en la room.
		"""
		x = instance.rect.left-instance.spritesheetPos[0]+self.screen.viewPos[0]
		y = instance.rect.top-instance.spritesheetPos[1]+self.screen.viewPos[1]
		if instance.onGrass:
			self.screen.screenBuffer.blit(instance.image,(x,y),(0,0,32,26))
			self.screen.screenBuffer.blit(pygame.image.load("sprites/grass.png").convert_alpha(),(x+7,y+18))
		else:
			self.screen.screenBuffer.blit(instance.image,(x,y))

	def oppositeDirection(self,d):
		"""
		Devuelve la dirección opuesta a d.
		"""
		dic = {
		0:1,
		1:0,
		2:3,
		3:2
		}
		return dic[d]

	def showMessage(self,s):
		"""
		Muestra un mensaje convencional por pantalla.
		"""
		print s

	def toRoomCoord(self,x):
		pass

	def toSurfaceCoord(self,x):
		pass