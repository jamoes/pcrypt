#!/usr/bin/python
from point import Point
import os

def getpoints(polynomial, num):
	"""returns a list of num points from polynomial
  """	
  	#the number of bytes that a x value can have:
  	domain = 4
	
	xvals = set()
	while (len(xvals) != num):
		r = os.urandom(domain)
		a = 0
		for byte in r:
			a = a * 256 + ord(byte) - 128
		xvals.add(a)
	
	points = []
	for x in xvals:
		y = 0
		for i in range(len(polynomial)):
			y += polynomial[i] * pow(x,len(polynomial) - i - 1)
		points.append(Point(x,y))
	return points
