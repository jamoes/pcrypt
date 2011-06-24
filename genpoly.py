#!/usr/bin/python
import os

def genpoly(order, bits = 128):
	"""Generates a random polynomial of specified order.
	   The polynomial generated will contain exactly as many 
		 bits as the specified number of bits, unless the order
		 is larger than bits, in which case the polynomial will
		 possibly contain more bits than specified.
		 The bits argument should be a multiple of 8.
	   Returns a list in the form [a,b,c,...] where a, b, and c
		 are the coeficiants of the polynomial. For example,
		 the list [5,3,-4,6] represents the 3rd order polynomial 
		 5x^3 + 3x^2 - 4x + 6
	   Uses python's os.urandom function, which is suitable
		 for cryptographic use.
		 Python version >=2.4 must be used"""
	
	#the number of bytes that each coeficiant must have in order
	#to garantee that the entire polynomial contains enough bits:
	coefBytes = (bits / (order + 1)) / 8
	#some coeficiants must contain an extra byte though, in order
	#to garantee that enough bits are generated
	#the first coeficiant not to contain an extra byte:
	first = (bits/8) % (order + 1)
	
	rands = []
	polynomial = []
	for i in range(order+1):
		if(i < first):
			rands.append(os.urandom(coefBytes + 1))
		else:
			rands.append(os.urandom(coefBytes))
	
	for s in rands:
		a = 0
		for byte in s:
			a = a * 256 + ord(byte)
		polynomial.append(a)
	return polynomial

