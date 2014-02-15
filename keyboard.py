# coding:utf-8

import pygame
from maps import *

class Keyboard:
	def __init__(self):
		# Si hay una flecha pulsada
		self.arrow = [False,False,False,False]
		# Si justo se acaba de pulsar una flecha (solo dura un ciclo)
		self.arrowPressed = [False,False,False,False]
		# Si hay alguna o ninguna flecha pulsada
		self.anyArrow = True in self.arrow
		self.noArrow = False in self.arrow
		# Si hay un botón pulsado
		self.key = {"A": False, "B": False}
		# Si justo se acaba de pulsar un botón
		self.keyPressed = {"A": False, "B": False}
	def update(self,gc):
		# Llevar a cabo tareas de input
		pygame.event.pump()
		for i in range(len(self.arrowPressed)):
			self.arrowPressed[i] = False
		self.keyPressed["A"] = False
		self.keyPressed["B"] = False
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_UP:
					self.arrow[0] = True
					self.arrowPressed[0] = True
				if e.key == pygame.K_DOWN:
					self.arrow[1] = True
					self.arrowPressed[1] = True
				if e.key == pygame.K_LEFT:
					self.arrow[2] = True
					self.arrowPressed[2] = True
				if e.key == pygame.K_RIGHT:
					self.arrow[3] = True
					self.arrowPressed[3] = True
				if e.key == pygame.K_z:
					self.key["A"] = True
					self.keyPressed["A"] = True
				if e.key == pygame.K_x:
					self.key["B"] = True
					self.keyPressed["B"] = True
				if e.key == pygame.K_ESCAPE:
					#return True
					gc.quit = True
				if e.key == pygame.K_PLUS:
					#return "plus"
					gc.screen.increaseSize()
				if e.key == pygame.K_MINUS:
					#return "minus"
					gc.screen.decreaseSize()
			elif e.type == pygame.KEYUP:
				if e.key == pygame.K_UP:
					self.arrow[0] = False
				if e.key == pygame.K_DOWN:
					self.arrow[1] = False
				if e.key == pygame.K_LEFT:
					self.arrow[2] = False
				if e.key == pygame.K_RIGHT:
					self.arrow[3] = False
				if e.key == pygame.K_z:
					self.key["A"] = False
				if e.key == pygame.K_x:
					self.key["B"] = False
			elif e.type == pygame.QUIT:
				gc.quit = True
				#return True
		self.anyArrow = True in self.arrow
		self.noArrow = not True in self.arrow