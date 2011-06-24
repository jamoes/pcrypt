#!/usr/bin/python
class Point:
	def __init__(self, xVal, yVal):
		self.x = xVal
		self.y = yVal
	

	def toString(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
