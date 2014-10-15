"""
Script used to plot results that were run by jug.

Matt Hoffman
Edited by Bobak Shahriari
26 September 2014
"""

import matplotlib
matplotlib.use('pdf')

import numpy as np
import matplotlib.pyplot as pl
try: import seaborn
except: pass

import argparse
import yaml
import os.path
import imp
from jug import set_jugdir, value

# parse the path of the experiment to plot
parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('--median', action='store_true', default=False,
                    help='whether to plot the median and quantiles; ' +
                    'defaults to False (i.e. mean and standard error).')
args = parser.parse_args()

# set where the data is stored
path = os.path.realpath(args.path)
jugdata = os.path.join(path, 'execute.jugdata')
set_jugdir(jugdata)

# import data place holder
execute_path = os.path.join(path, 'execute.py')
data = imp.load_source('execute', execute_path).data

# import plotting configurations
with open(os.path.join(path, 'config.yaml')) as f:
    config = yaml.safe_load(f)

for function in data.keys():
    ax = pl.figure(1).gca()
    ax.cla()

    # sort keys in order requested by config file
    keys = sorted(config.keys(), key=lambda k: config[k].get('order', -np.inf))

    for method in keys:
        c = config[method]

        # load in plotting configurations
        color = c.get('color', None)
        linestyle = c.get('linestyle', '-')
        label = c.get('label', method)
        ymin = c.get('ymin', None)
        log = False if (ymin is None) else c.get('log', False)

        # manipulate data
        runs = np.array(value(data[function][method]))
        N = runs.shape[0]
        T = runs.shape[1]
        x = np.arange(1, T+1)
        if args.median:
            y = np.median(runs, axis=0)
            ylo = np.percentile(runs, 25, axis=0)
            yhi = np.percentile(runs, 75, axis=0)
        else:
            y = runs.mean(axis=0)
            e = runs.std(axis=0) / np.sqrt(N)
            ylo = y - e
            yhi = y + e

        # plotting
        if log:
            if color is None:
                ax.semilogy(x, np.clip(y-ymin, 1e-8, np.inf),
                            lw=2, ls=linestyle, label=label)
            else:
                ax.semilogy(x, np.clip(y-ymin, 1e-8, np.inf),
                            lw=2, color=color, ls=linestyle, label=label)
            ax.fill_between(x, np.clip(ylo-ymin, 1e-8, np.inf), yhi-ymin,
                            color=ax.lines[-1].get_color(), alpha=0.1)
        else:
            if color is None:
                ax.plot(x, y, lw=2, ls=linestyle, label=label)
            else:
                ax.plot(x, y, lw=2, color=color, ls=linestyle, label=label)
            ax.fill_between(x, ylo, yhi,
                            color=ax.lines[-1].get_color(), alpha=0.1)

    ax.axis('tight')
    ax.axis(xmin=0, xmax=T)
    ax.set_xlabel('iterations')
    ax.set_ylabel('absolute error' if log else 'function value')
    ax.legend(loc='best')
    ax.set_title(function)
    ax.figure.canvas.draw()

    # save figure
    figpath = os.path.dirname(os.path.realpath(__file__))
    figpath = os.path.join(figpath, 'figures')
    if not os.path.isdir(figpath):
        os.mkdir(figpath)
    figpath = os.path.join(figpath, '{}.pdf'.format(function))
    ax.figure.savefig(figpath, bbox_inches='tight')
    print 'Plot saved in {}'.format(figpath)

