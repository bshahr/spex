import numpy as np
import sys
import math
import time

def hart3(x):
	""" 
		Hartmann function 
		The number of variables n = 3.
	"""

	a = np.array([[3., 10., 30.], \
				  [0.1, 10., 35.], \
				  [3., 10., 30.], \
				  [0.1, 10., 35.]])

	c = np.array([1., 1.2, 3., 3.2])

	p = np.zeros((4, 3))

	p[0,0]=0.36890;p[0,1]=0.11700;p[0,2]=0.26730
	p[1,0]=0.46990;p[1,1]=0.43870;p[1,2]=0.74700
	p[2,0]=0.10910;p[2,1]=0.87320;p[2,2]=0.55470
	p[3,0]=0.03815;p[3,1]=0.57430;p[3,2]=0.88280
	
	s = 0.

	for i in range(4):
	   sm = 0.
	   for j in range(3):
	      sm = sm + a[i,j]*(x[j]-p[i,j])**2.
	   s = s + c[i]*np.exp(-sm)

	return s

# Write a function like this called 'main'
def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return -hart3(params['X'])
