import numpy as np
import sys
import math
import time

def hart6(x):
	""" 
		Hartmann function 
		The number of variables n = 6.
	"""

	a = np.array([[10.0, 3.0, 17.0, 3.5, 1.7, 8.0], \
				  [0.05, 10.0, 17.0, 0.1, 8.0, 14.0], \
				  [3.0, 3.5, 1.7, 10.0, 17.0, 8.0], \
				  [17.0, 8.0, 0.05, 10.0, 0.1, 14.0]])

	c = np.array([1.0, 1.2, 3.0, 3.2])
	p = np.array([[0.1312, 0.1696, 0.5569, 0.0124, 0.8283, 0.5886], \
				  [0.2329, 0.4135, 0.8307, 0.3736, 0.1004, 0.9991], \
				  [0.2348, 0.1451, 0.3522, 0.2883, 0.3047, 0.6650], \
				  [0.4047, 0.8828, 0.8732, 0.5743, 0.1091, 0.0381]])

	s = 0.
	for i in range(4):
	   sm = 0.
	   for j in range(6):
	      sm = sm + a[i,j]*(x[j]-p[i,j])**2.
	   s = s + c[i]*np.exp(-sm)

	return s

# Write a function like this called 'main'
def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return -hart6(params['X'])
