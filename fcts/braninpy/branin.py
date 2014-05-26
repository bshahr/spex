import numpy as np
import sys
import math
import time

def branin(x):
	"""
		Branin function 
		The number of variables n = 2.
	"""
	bound = np.array([[-5., 10.], [0., 15.]])
	x = x*(bound[:, 1] - bound[:, 0]) + bound[:, 0]
	y = (x[1]-(5.1/(4.0*np.pi**2))*x[0]**2.0 + \
		5.0*x[0]/np.pi-6.0)**2.0+10.0*(1.0-1.0/(8.0*np.pi))*np.cos(x[0])+10.0;
	return y

# Write a function like this called 'main'
def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return branin(params['X'])
