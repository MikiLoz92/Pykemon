#coding: utf-8

from objects import *
from utils import override

class Mail1(Text):
	def onTalk(self,gc):
		gc.showMessage("Residencia de Brendan")

class Mail2(Text):
	def onTalk(self,gc):
		gc.showMessage("Residencia de May")

class Magma1(Animated):
	def __init__(self):
		self.spritesheet = "005"
		super(Magma1,self).__init__(self.spritesheet)
	def update(self, gc):
		super(Magma1,self).update(gc)
	def onTalk(self,gc):
		self.facing = gc.oppositeDirection(gc.hero.facing)
		gc.showMessage("¡Hola!")