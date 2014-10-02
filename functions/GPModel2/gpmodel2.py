import os.path
import pybo
import pygp

_dim = 2

# get seed from directory name if it's an integer
_path = os.path.dirname(__file__)
_seed = os.path.basename(_path.rstrip('/'))
try:
    _seed = int(_seed)
except ValueError:
    _seed = 0

# define the model
def gpmodel2(x):
    sn = 0.1        # noise
    sf = 1.0        # amplitude
    ell = 0.5       # length scale
    bounds = [[0,10]] * _dim

    gp = pygp.BasicGP(sn, sf, ell, ndim=_dim, kernel='se')
    function = pybo.functions.gps.GPModel(bounds, gp, rng=_seed)

    return function(x)

def main(jobid, params):
    return gpmodel2(params['X'])
