#!/usr/bin/python
from point import Point

def getKeyFromPoly(polynomial):
	"""returns a string from the polynomial in a uniform manner"""
	s = ""
	for c in polynomial:
		a = c
		while (a != 0):
			byte = chr(a % 256)
			a = a / 256
			s = s + byte
	return s

