# coding: utf-8
import pygame

pygame.display.init()
screen = pygame.display.set_mode((320,240))
surface = pygame.image.load("tilesets/001.png").convert_alpha()
while True:
	screen.blit(surface,(0,0))
	pygame.display.flip()