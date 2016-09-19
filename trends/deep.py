"""
this class is really only here as a placeholder, i'm working on integrating a well established machine learning library like
 tensorflow as soon as the rest of the stuff is ready to go.
 
 it doesn't DO anything yet, just creates an empty numpy matrix that would ostensibly hold weights and biases
"""

import numpy as np
import math
import os,sys

#activation function definitions
FN_SIGMOIDAL = lambda x: 1/(1+math.exp(-x))

#default initialization vars
DEFAULT_ARCH = {
		"shape": [3,2,2,1,2,2,3]
								}

DEFAULT_CONSTRAINTS = (0.0,10.0)

DEFAULT_PARAMS = {
		"randomize":(True, (0.0, 10.0)),
		"activation":FN_SIGMOIDAL
									}


class nn(object):
	def __init__(self, arch=DEFAULT_ARCH, params = DEFAULT_PARAMS):
		if arch == DEFAULT_ARCH:
			self.arch = DEFAULT_ARCH
			print "Created neural network with default architecture."
			self._initRandom()
	
	
	#instance layer
	def _initRandom(self, constraints = DEFAULT_CONSTRAINTS):
		""" initialize the network with  random floating point values for weights and biases, within certain constraints """
		self.v = [[0.0 for r in range(self.arch["shape"][i])] for i in range(len(self.arch["shape"]))]
		print self.v
		
	#user layer
	def lin(self):
		""" return linearized neural network for genetic algorithm evolution """
	
	def feed(self, vector):
		""" run data vector through network as input """	
	
	#overloaded operators
	def __getitem__(self, key):
		pass
	

def main():
	net = nn()
	
if __name__ == "__main__":main()