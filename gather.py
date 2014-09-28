"""
Script used to gather results that were run by jug.

Bobak Shahriari
26 September 2014
"""

import cPickle as pkl
import argparse
import os.path
import imp
from jug import set_jugdir, value

# parse the path of the experiment to plot
parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()

# set where the data is stored
path = os.path.realpath(args.path.rstrip('/'))
jugdata = os.path.join(path, 'execute.jugdata')
set_jugdir(jugdata)

# import data place holder and fill in values
execute_path = os.path.join(path, 'execute.py')
data = imp.load_source('execute', execute_path).data
data = value(data)

# save to results directory
root_path = os.path.dirname(os.path.realpath(__file__))
expt_name = os.path.basename(path)
results_path = os.path.join(root_path, 'results')
if not os.path.isdir(results_path):
    os.mkdir(results_path)
pkl_file = os.path.join(results_path, expt_name)
with open(pkl_file + '.pkl', 'wb') as f:
    pkl.dump(data, f)
