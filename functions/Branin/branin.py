import pybo
import numpy as np


def branin(x):
    sn = 1e-6   # noise
    function = pybo.functions.Branin(sn)

    # transform spearmint x which is in [0,1]
    x *= function.bounds[:, 1] - function.bounds[:, 0]
    x += function.bounds[:, 0]

    return -function(x)

def main(jobid, params):
    return branin(params['X'])
