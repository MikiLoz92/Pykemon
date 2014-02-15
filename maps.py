# coding: utf-8

import pygame
import os
import xml.etree.ElementTree as ET
import sys
sys.path.append('./maps')
from objects import *
from resources import *


class Tileset:
	"""
	Define un tileset con un Surface s, que por defecto está vacío (utiliza el método "load" para cargar uno del FS o el método loadFromFolder para cargar un archivo desde la carpeta por defecto, que es "tilesets".
	"""

	def __init__(self, fname, sep = 0, wtile = 16, htile = 16, nrows = 1024, ncols = 14):
		self.loadFromFolder(fname)
		self.process(sep,wtile,htile,nrows,ncols)
	
	def load(self, dest):
		self.s = pygame.image.load(dest)
	
	def loadFromFolder(self, fname):
		self.s = pygame.image.load(os.path.join("tilesets",fname))
		
	def process(self,sep,wtile,htile,nrows,ncols):
		"""
		Convierte una imagen, dados unos parámetros de calibraje, en una lista de surfaces que conformarán el objeto tileset.
		"""
		self.t = []
		y = 0
		for i in range(nrows):
			x = 0
			for j in range(ncols):
				tempS = pygame.Surface((16,16),pygame.SRCALPHA)
				tempS.blit(self.s,(0,0),(x,y,x+wtile,y+htile))
				self.t.append(tempS)
				x += wtile + sep
			y += htile + sep


class Map:
	"""
	Define un mapa con una información de mapa m, dada como una lista de listas, y un tileset t, definido como un objeto Tileset.
	"""

	def __init__(self, m = [], t = Tileset("001.png",1,16,16,6,6), n = ""):
		if isinstance(m,str):
			self.loadFromFolder(m)
		else:
			self.map = m
			self.name = n
			self.tileset = t
			self.heroLayer = 0
			
	def __getitem__(self,i):
		# Funciona como [CAPA][fila][columna]
		return self.map[i]
	
	def loadFromFolder(self, fname):
		self.map = []
		self.permissionMap = []

		self.filename = fname
		
		tree = ET.parse(os.path.join("maps",fname))
		root = tree.getroot()
		layers = root.findall("layer")

		self.width = int(layers[0].attrib["width"])
		self.height = int(layers[0].attrib["height"])

		# Buscamos cuál es el número de la primera tile del tileset de permisos
		for i in root.findall("tileset"):
			if i.attrib["name"] == "Permissions":
				firstPermissionTile = int(i.attrib["firstgid"])
				print firstPermissionTile

		for i in range(len(layers)):
			w = int(layers[i].attrib["width"])
			h = int(layers[i].attrib["height"])
			text = layers[i].findall("data")[0].text
			l = text.split()
			if layers[i].attrib["name"] == "Permissions":
				for j in range(h):
					self.permissionMap.append([])
					l2 = l[j].split(",")
					for k in range(w):
						self.permissionMap[j].append(int(l2[k])-firstPermissionTile)
						if self.permissionMap[j][k] < 0:
							self.permissionMap[j][k] = -1
			elif layers[i].attrib["name"] == "Hero":
				self.heroLayer = i
				self.map.append([])
			else:
				self.map.append([])
				for j in range(h):
					self.map[i].append([])
					l2 = l[j].split(",")
					for k in range(w):
						self.map[i][j].append(int(l2[k])-1)

		self.limits = [None]*4
		properties = root.findall("properties")[0].findall("property")
		for i in properties:
			if i.attrib["name"] == "name":
				self.name = i.attrib["value"]
			elif i.attrib["name"] == "northLimit":
				self.limits[0] = i.attrib["value"]
			elif i.attrib["name"] == "southLimit":
				self.limits[1] = i.attrib["value"]
			elif i.attrib["name"] == "westLimit":
				self.limits[2] = i.attrib["value"]
			elif i.attrib["name"] == "eastLimit":
				self.limits[3] = i.attrib["value"]

		self.tileset = Tileset(root.findall("tileset")[0].findall("image")[0].attrib["source"].split("/")[-1])

		objectList = root.findall("objectgroup")[0].findall("object")
		self.instanceList = []
		mapModule = __import__(self.filename[0:-4])
		for i in objectList:
			instance = getattr(mapModule,i.attrib["name"])()
			# Corregimos el bug de posición del Tiled
			if "gid" in i.attrib:
				instance.tilePos = [ int(i.attrib["x"])/16, int(i.attrib["y"])/16-1 ]
			else:
				instance.tilePos = [ int(i.attrib["x"])/16, int(i.attrib["y"])/16 ]
			instance.rect = pygame.Rect(instance.tilePos[0]*16, instance.tilePos[1]*16,16,16)
			if "behavior" in i.attrib:
				instance.behavior = i.attrib["behavior"]
			self.instanceList.append(instance)

		""""
		for i in objectList:
			instType = objects.convertToObject(i.attrib["type"])
			instName = i.attrib["name"]
			instPos = [ int(i.attrib["x"]), int(i.attrib["y"]) ]
			instTile = [ instPos[0]/16, instPos[1]/16 ]
			self.instanceList.append([instType,instName,instPos,instTile])
		"""
	
	def clear(self):
		self.map = []