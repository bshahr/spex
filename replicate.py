"""
This script parses a configuration file (yaml) and replicates the requested
function directory according to the repetitions desired.

Example usage:

    # run replicate.py to create subdirectories and tasks
    python replicate.py experiment-directory/config.yaml

    # use jug to execute tasks
    jug execute experiment-directory/execute.py

    # use the following to track progress
    jug status experiment-directory/execute.py


Bobak Shahriari
23 September 2014
"""

import os
import shutil
import yaml
import random

def prepare_spearmint(expt_path, config):

    # unpack configuration
    function = config.get('function')
    method = config.get('method')
    nreps = config.get('nreps')
    methargs = config.get('methargs', None)

    # draw a unique identifier
    serial = str(random.randint(1e9, 1e10))

    # fetch path of the function that is to be optimized
    root_path = os.path.dirname(os.path.realpath(__file__))
    original_path = os.path.join(root_path, 'functions', function)

    # subdirectory name for current function/method pair
    subdir = '-'.join([function, method, serial])
    expt_path = os.path.join(expt_path, subdir)

    for seed in xrange(nreps):
        # generate subdirectory name and path for this repetition
        seeddir = '{0:03d}'.format(seed)
        destination_path = os.path.join(expt_path, seeddir)

        # copy directory tree
        try:
            shutil.copytree(original_path, destination_path)
        except OSError:
            continue

        # write yaml file that configures the method
        fname = os.path.join(destination_path, 'add.yaml')
        with open(fname, 'w') as f:
            f.write(yaml.dump(methargs, default_flow_style=True))

    # dump yaml file for this particular configuration
    with open(os.path.join(expt_path, 'config.yaml'), 'w') as f:
        f.write(yaml.dump(config))


def main(config_file):

    # set random seed for reproducibility
    random.seed(0)

    # parse config file
    with open(config_file) as f:
        configs = yaml.safe_load(f)

    # get root path (where this `replicate.py` script lives)
    root_path = os.path.dirname(os.path.realpath(__file__))
    # get experiment path (where the config file lives)
    expt_path = os.path.dirname(os.path.realpath(config_file))

    # for each requested configuration prepare required directories
    for config in configs.values():
        prepare_spearmint(expt_path, config)

    # copy the execute script that generates/runs jug tasks
    shutil.copy(os.path.join(root_path, 'execute.py'), expt_path)


if __name__ == '__main__':
    import argparse

    # fetch config filename
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file')
    args = parser.parse_args()

    # prepare required subdirectories
    main(args.config_file)

