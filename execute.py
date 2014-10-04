"""
This script is meant to be copied into the root directory of each experiment
by the replicate.py script. This script generates a jug task for each run.

Example usage:

    # run replicate.py to create subdirectories and tasks
    python replicate.py <experiment-directory>

    # use jug to execute tasks
    jug execute <experiment-directory>

    # use the following to track progress
    jug status <experiment-directory>/execute.py


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
SPEARMINT = os.path.abspath(os.path.dirname(os.path.abspath(spearmint.__file__)) + '/../bin/spearmint')

# fetch path of the experiment config file
path = os.path.dirname(os.path.abspath(__file__))

# subdirectory name for current function/method pair
subdirs = os.listdir(path)

data = dict()
for directory in subdirs:
    current_path = os.path.join(path, directory)

    # make sure current_path is a directory with a config file
    if not os.path.isdir(current_path):
        continue

    config_file = os.path.join(current_path, 'config.yaml')
    if not os.path.isfile(config_file):
        continue

    # load config file
    with open(config_file) as f:
        config = yaml.safe_load(f)

    function = config.get('function')
    method = config.get('method')
    if function not in data.keys():
        data[function] = dict()

    def execute(expt_path, config, seed):
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
            os.path.join(expt_path, '{0:03d}'.format(seed), 'config.pb')
            ])

        # return results if they exist
        result_file = os.path.join(expt_path,
                                   '{0:03d}'.format(seed),
                                   'trace.csv')
        try:
            data = loadtxt(result_file, skiprows=1, delimiter=',')
            return data[1:, 1]
        except IOError:
            pass

    # rename task to match config key
    execute.__name__ = directory

    # generate jug task
    jug_task = jug.TaskGenerator(execute)

    data[function][method] = [jug_task(current_path, config, seed)
                              for seed in range(config.get('nreps', 1))]

