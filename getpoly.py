#!/usr/bin/python
from point import Point

class MatrixException:
	pass

def getpoly(points):
	"""Takes in a set of points
	   Returns a polygon ax^n + bx^(n-1) + ... + cx + d
	   as an ordered list [a, b, ..., c, d]"""
	yVals = []
	xVals = []
	for point in points:
		yVals.append(point.y)
	for c in reversed(range(len(points))):
		vals = []	
		for point in points:
			vals.append(pow(point.x, c))
		xVals.append(vals)
	
	#now we have n equations and n unknowns, 
	#we just have to solve for the unknowns
	#we will solve using Cramer's method:
	xdet = determinant(xVals)
	polynomial = []
	for i in range(len(points)):
		m = []
		for j in range(len(points)):
			if (j == i):
				m.append(yVals)
			else:
				m.append(xVals[j])
		polynomial.append(determinant(m) / xdet)
	return polynomial
	

def determinant(m):
	"Solves determinate of a matrix using Laplacian expansion"
	
	#sanity checks:
	if (len(m) < 1):
		raise MatrixException
	if(len(m) != len(m[0])):
		print "EXCEPTION: Matrix not square"
		raise MatrixException
	
	if (len(m) == 1):
		return m[0][0]
	if (len(m) == 2):
		return m[0][0] * m[1][1] - m[1][0] * m[0][1]
	else:
		det = 0
		for i in range(len(m)):
			smallM = []
			for j in range (len(m)):
				if (j != i):
					a = []
					for k in range(1,len(m)):
						a.append(m[j][k])
					smallM.append(a)
			det += pow(-1,i+2) * m[i][0] * determinant(smallM)
		return det

				
