#!/usr/bin/python

from point import Point
from getpoly import getpoly
from getKeyFromPoly import getKeyFromPoly
from getpoints import getpoints
from genpoly import genpoly
from Crypto.Cipher import AES

import sys
import pickle
import re

def usage():
	print """
USAGE: pcrypt.py [OPTIONS] file
     -m <number>           Minimum number of keys required to decrypt file
     -n <number>           Number of keys to generate
     -d <filelist>         Decrypt the file
                           <filelist> is a list of semicolon seperated
                           point files, such as file.p1;file.p2;file.p3
     -o <file>             The file to output to
                           By default, the file will be output to file.pcrypt
                           if encrpyting, and file.pdecrypt if decrypting
     -k <keylength>        The length of the key, must be 16, 24, or 32.
                           Default is 16
     --help                Display this help message
"""

def clerror():
	usage()
	sys.exit(2)

if (len(sys.argv) < 2):
	clerror()

i = 1

file = ""
outfile = ""
minKeys = 2
numKeys = 2
keylength = 16
decrypting = False

try:
	while (i < len(sys.argv)):
		if (sys.argv[i][0] != '-'):
			if (file != ""):
				clerror()
			else:
				file = sys.argv[i]
		else:
			if (sys.argv[i] == '-m'):
				minKeys = int(sys.argv[i+1])
				i += 1
			elif (sys.argv[i] == '-n'):
				numKeys = int(sys.argv[i+1])
				i += 1
			elif (sys.argv[i] == '-d'):
				decrypting = True
				pointFileString = sys.argv[i+1]
				i += 1
			elif (sys.argv[i] == '-o'):
				outfile = sys.argv[i+1]
				i += 1
			elif (sys.argv[i] == '-k'):
				keylength = int(sys.argv[i+1])
				i += 1
			elif(sys.argv[i] == '--help'):
				raise
			else:
				clerror()
		i+=1
except:
	clerror()

if (file == ""):
	clerror()
if (numKeys < minKeys):
	print "Error: Number of keys generated is less than the \
	\nminimum number of keys required to decrypt"
	sys.exit(2)
if(decrypting):
	pointFileList = pointFileString.split(';')
if(outfile == ""):
	if(not decrypting):
		outfile = file + ".pcrypt"
	else:
		outfile = file + ".pdecrypt"
if(keylength != 16 and keylength != 24 and keylength != 32):
	print keylength
	print "Error: Keylength must be 16, 24 or 32"
	sys.exit(2)

#Done with command line analysis, now on to the actual work:

if(not decrypting):
	#generate a polynomial
	polynomial = genpoly(minKeys - 1, keylength * 8)
	
	#generate points from the polynomial, and save them to files:
	i = 1
	points = getpoints(polynomial, numKeys)
	for point in points:
		f = open(file + '.p' + str(i), 'w')
		pickle.dump(point, f)
		i += 1;
		f.close()
	
	#encrypt the file using the polynomial's key
	key = str(getKeyFromPoly(polynomial))
	try:
		f = open(file, 'r')
	except IOError:
		print "Cannot open file: " + file
		sys.exit(1)
	plaintext = f.read()
	f.close()
	obj = AES.new(key)
	#make the plaintext a multiple of the encryption algorithm's blocksize:
	while(len(plaintext) % obj.block_size != 0):
		plaintext = plaintext + " "
	ciphertext = obj.encrypt(plaintext)

	#write the ciphertext to file:
	f = open(outfile, 'w')
	f.write(ciphertext)
	f.close()
else:
	#we are decrypting
	#load the points:
	pointList = []
	try:
		for pointFile in pointFileList:
			f = open(pointFile, 'r')
			pointList.append(pickle.load(f))
			f.close()
	except:
		print "Error loading point file"
		sys.exit(1)
	
	#get the polynomial:
	polynomial = getpoly(pointList)
	
	key = str(getKeyFromPoly(polynomial))

	try:
		f = open(file, 'r')
	except IOError:
		print "Cannot open file: " + file
		sys.exit(1)
	ciphertext = f.read()
	f.close()
	
	obj = AES.new(key)
	plaintext = obj.decrypt(ciphertext)

	#remove the padding from the end of the plaintext:
	p = re.compile(r"^ +\Z", re.MULTILINE)
	plaintextF = p.sub('', plaintext)

	#output the plaintext to file:
	f = open(outfile, 'w')
	f.write(plaintextF)
	f.close()
