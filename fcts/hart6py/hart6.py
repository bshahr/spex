import numpy as np
import sys
import math
import time
from bo.demos.testFuncs import hart6


# Write a function like this called 'main'
def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return hart6(params['X'])
