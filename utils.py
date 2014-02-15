# coding: utf-8

import inspect

def oppositeDirection(d):
	"""
	Devuelve la dirección opuesta a d.
	"""
	dic = {	0:1, 1:0, 2:3, 3:2 }
	return dic[d]

def override(m,n,*args):
	super(m,n).__init__(*args)