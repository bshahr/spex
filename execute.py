"""
This script is meant to be copied into the root directory of each experiment
by the replicate.py script. This script generates a jug task for each run.

Example usage:

    # run replicate.py to create subdirectories and tasks
    python replicate.py experiment-directory/config.yaml

    # use jug to execute tasks
    jug execute experiment-directory/execute.py

    # use the following to track progress
    jug status experiment-directory/execute.py


Bobak Shahriari
24 September 2014
"""

import os
import shutil
import yaml
import jug
import subprocess
from numpy import loadtxt

# get path to spearmint binary
HOME = os.environ['HOME']
SPEARMINT = os.path.join(HOME, 'spearmint/spearmint/bin/spearmint')

@jug.TaskGenerator
def run_spearmint(path, config, seed):

    # unpack configuration
    function = config.get('function')
    method = config.get('method')
    horizon = config.get('horizon')
    noiseless = config.get('noiseless', 0)
    # usegrad = config.get('usegrad')

    # run process
    subprocess.call([
        SPEARMINT,
        '--driver=local',
        '--method={}'.format(method),
        '--max-finished-jobs={}'.format(horizon),
        '--method-args=noiseless={}'.format(noiseless),
        # '--use-gradient={}'.format(usegrad),
        '--grid-seed={}'.format(seed),
        os.path.join(path, '{0:03d}'.format(seed), 'config.pb')
        ])

    # return results if they exist
    result_file = os.path.join(path, '{0:03d}'.format(seed), 'trace.txt')
    try:
        data = loadtxt(result_file)
        return data[:, 1]
    except IOError:
        pass


# fetch path of the experiment config file
path = os.path.dirname(os.path.abspath(__file__))

# subdirectory name for current function/method pair
subdirs = os.listdir(path)

for directory in subdirs:
    current_path = os.path.join(path, directory)

    # make sure current_path is a directory with a config file
    if not os.path.isdir(current_path):
        continue

    config_file = os.path.join(current_path, 'config.yaml')
    if not os.path.isfile(config_file):
        continue

    with open(config_file) as f:
        config = yaml.safe_load(f)

    nreps = config.get('nreps')
    for seed in range(nreps):
        run_spearmint(current_path, config, seed)

