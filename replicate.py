"""
This script parses a configuration file (yaml) and replicates the requested
function directory according to the repetitions desired.

Example usage:

    # run replicate.py to create subdirectories and tasks
    python replicate.py <experiment-directory>

    # use jug to execute tasks
    jug execute <experiment-directory>

    # use the following to track progress
    jug status <experiment-directory>/execute.py


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

    # fetch path of the function that is to be optimized
    root_path = os.path.dirname(os.path.realpath(__file__))
    original_path = os.path.join(root_path, 'functions', function)

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
        if methargs is not None:
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
    for name, config in configs.items():
        prepare_spearmint(os.path.join(expt_path, name), config)

    # copy the execute script that generates/runs jug tasks
    root_execute_path = os.path.join(root_path, 'execute.py')
    shutil.copy(root_execute_path, expt_path)
    expt_execute_path = os.path.join(expt_path, 'execute.py')

    # write pbs file to run jug task
    with open(os.path.join(expt_path, 'execute.pbs'), 'w') as f:
        f.write('jug execute {}'.format(expt_execute_path))


if __name__ == '__main__':
    import argparse

    # fetch config filename
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment_path')
    args = parser.parse_args()

    # get path and execute filenames
    expt_path = args.experiment_path.rstrip('/')
    pbs_path = os.path.join(expt_path, 'execute.pbs')

    # prepare required subdirectories
    config_file = os.path.join(expt_path, 'config.yaml')
    if not os.path.isfile(pbs_path):
        main(config_file)


    # print jug or qsub command
    print '\n' + '=' * 72
    print 'spearmint-experiments:\n'
    print 'Your experiment is now ready to be executed! Run the following from'
    print 'the command line to process locally\n'
    print '\tbash jug-execute.sh {} -n 8\n'.format(expt_path)
    print 'where we use 8 as a default number of parallel processes, omitting the'
    print '`-n 8` option defaults to a single process. Alternatively, to submit a'
    print 'job to a cluster, run:\n'
    print '\tqsub -l walltime=24:00:00,mem=4gb -t 1-10 {}\n'.format(pbs_path)
    print 'where by default we request a walltime of 24h, 4gb of memory, and 10'
    print 'jobs. Notice however that submitting this identical job twice will'
    print 'simply double the number of workers on this particular experiment\'s'
    print 'task queue.\n'
    print '=' * 72 + '\n'
    
