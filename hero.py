# coding: utf-8

import pygame
from objects import ripSpriteSheet

class Hero(pygame.sprite.Sprite):

	def __init__(self):
		self.images = [ [], [] ]
		self.spritesheet = pygame.image.load("sprites/001.png")
		self.images[0] = ripSpriteSheet(self.spritesheet)
		self.images[1] = ripSpriteSheet(pygame.image.load("sprites/002.png"))

		self.image = self.images[0][0][0]
		self.facing = 1
		self.tilePos = [9,12]
		self.nextTile = [9,12]
		self.walkDelay = 0
		self.onDelay = False
		self.canMove = True
		self.moving = False
		self.running = False
		self.step = False
		self.hitBlock = False
		self.cycling = False
		self.spriteIndex = 0
		self.imageIndex = 0
		self.moveSpeed = 2
		self.speed = 0
		self.onGrass = False
		self.slow = False

		self.rect = pygame.Rect(self.tilePos[0]*16,self.tilePos[1]*16,16,16)
		# Posición del rectángulo 16x16 en cada cuadrícula de sprites de 32x32
		self.spritesheetPos = [7,14]

	def update(self, keyboard, room):

		self.updateMovement(keyboard)

		# North
		if self.nextTile[1] < 0:
			self.hitBlock = False
			print "YO"
			"""
			#PREVIOUSLY ON PYKEMON
			if room.nextRoom[0] != None and room.nextRoom[0].content.permissionMap[room.nextRoom[0].height-1][self.nextTile[0]] == 0:
				print "HEY!"
				self.hitBlock = True
				self.running = False
				self.speed = 0
			else:
				self.moving = True
				return "cr"
			"""
			
		elif self.nextTile[1] >= room.height:
			self.hitBlock = False
			pass
		elif self.nextTile[0] < 0:
			self.hitBlock = False
			pass
		elif self.nextTile[0] >= room.width:
			self.hitBlock = False
			pass
		else:
			#print "ELSE"
			if room.content.permissionMap[self.nextTile[1]][self.nextTile[0]] == 0 or room.permissionMap[self.nextTile[1]][self.nextTile[0]] == 1:
				#print "cASnFOÑAS"
				self.hitBlock = True
				self.running = False
				self.speed = 0
				#self.imageSpeed = 32
			else:
				self.hitBlock = False
			if room.content.permissionMap[self.nextTile[1]][self.nextTile[0]] == 2:
				self.onGrass = True
				if self.nextTile[1] < self.tilePos[1] and room.content.permissionMap[self.tilePos[0]][self.tilePos[1]] != 2:
					self.onGrass = False
			elif room.content.permissionMap[self.tilePos[1]][self.tilePos[0]] == 2 and self.nextTile[1] < self.tilePos[1] and self.facing == 1:
				self.onGrass = True
			else:
				self.onGrass = False

			if room.content.permissionMap[self.nextTile[1]][self.nextTile[0]] == 3 or room.content.permissionMap[self.tilePos[1]][self.tilePos[0]] == 3:
				self.slow = True
		
		#print self.moving
		#print self.hitBlock

		if self.nextTile == self.tilePos and (self.nextTile[0] < 0 or self.nextTile[1] < 0):
			# CAMBIAR TODO EL SISTEMA DE COORDENADAS, TILEPOS, NEXTTILE, ETC.
			pass

		if self.facing == 0:
			self.rect.y -= self.speed
		elif self.facing == 1:
			self.rect.y += self.speed
		elif self.facing == 2:
			self.rect.x -= self.speed
		elif self.facing == 3:
			self.rect.x += self.speed

		# -- RUTINA DE DIBUJADO DE SPRITE --
		self.image = self.images[self.spriteIndex][self.facing][self.imageIndex]

	def setNextTile(self, i):
		if i == 0:
			self.nextTile[1] -= 1
		elif i == 1:
			self.nextTile[1] += 1
		elif i == 2:
			self.nextTile[0] -= 1
		elif i == 3:
			self.nextTile[0] += 1

	def setFacing(self):
		if keyboard.arrow[0]:
			self.facing = 0
		elif keyboard.arrow[1]:
			self.facing = 1
		elif keyboard.arrow[2]:
			self.facing = 2
		elif keyboard.arrow[3]:
			self.facing = 3

	def jumpTo(self,tile):
		self.tilePos = [tile[0],tile[1]]
		self.nextTile = [tile[0],tile[1]]
		self.rect.x = self.tilePos[0]*16
		self.rect.y = self.tilePos[1]*16

	def facingTile(self):
		if self.facing == 0:
			return [self.tilePos[0],self.tilePos[1]-1]
		elif self.facing == 1:
			return [self.tilePos[0],self.tilePos[1]+1]
		elif self.facing == 2:
			return [self.tilePos[0]-1,self.tilePos[1]]
		elif self.facing == 3:
			return [self.tilePos[0]+1,self.tilePos[1]]

	def updateMovement(self,keyboard):
		if self.walkDelay != 0:
			self.walkDelay += 1
			if self.walkDelay == 10:
				if self.rect.x%16 == 0 and self.rect.y%16 == 0 and keyboard.anyArrow:
					self.moving = True
				self.imageIndex = 0
				self.walkDelay = 0
		if self.walkDelay == 0:
			if self.rect.x%16 == 0 and self.rect.y%16 == 0 and self.canMove:
				self.tilePos = [self.rect.x/16,self.rect.y/16]
				self.nextTile = [self.rect.x/16,self.rect.y/16]
				if self.moving and not self.hitBlock and not self.cycling:
					self.running = keyboard.key['B']
				"""if not self.moving and keyboard.keyPressed["A"]:
					self.cycling = not self.cycling"""
				if self.moving and keyboard.noArrow:
					self.moving = False
					self.running = False
					self.imageIndex = 0
				for i in [0,1,2,3]:
					if keyboard.arrow[i]:
						if self.moving:
							self.facing = i
							self.setNextTile(i)
							break
						if not self.moving:
							if self.facing == i:
								self.step = not self.step
								if not self.step:
									self.imageIndex = 1
									self.i = 0
								else:
									self.imageIndex = 3
									self.i = 0
								self.moving = True
								self.setNextTile(i)
							else:
								if keyboard.arrowPressed[i]:
									self.walkDelay += 1
								self.facing = i
								self.imageIndex = 3
				self.spriteIndex = 0
				if self.running:
					self.spriteIndex = 1
			#self.hitBlock = False
			if self.running or self.cycling:
				self.moveSpeed = 2
			if not self.running and not self.cycling:
				self.moveSpeed = 1
			if self.moving and self.canMove and not self.hitBlock:
				self.imageSpeed = 8
				self.speed = self.moveSpeed
				if self.running or self.cycling:
					self.imageSpeed = 8
			elif self.hitBlock:
				self.imageSpeed = 16
			else:
				self.speed = 0
				self.imageSpeed = 0

			if self.imageSpeed != 0:
				if self.i < self.imageSpeed:
					self.i += 1
				else:
					self.i = 0
					self.imageIndex += 1
					if self.imageIndex > 3:
						self.imageIndex = 0
			else:
				self.imageIndex = 0
				self.i = 0