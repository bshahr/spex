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
import seaborn

import argparse
import os.path
import imp
from jug import set_jugdir, value

# parse the path of the experiment to plot
parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()

# set where the data is stored
path = os.path.realpath(args.path)
jugdata = os.path.join(path, 'execute.jugdata')
set_jugdir(jugdata)

# import data place holder
execute_path = os.path.join(path, 'execute.py')
data = imp.load_source('execute', execute_path).data

for function in data.keys():
    ax = pl.figure(1).gca()
    ax.cla()
    for method in data[function].keys():
        runs = np.array(value(data[function][method]))
        N = runs.shape[0]
        T = runs.shape[1]
        x = np.arange(1, T+1)
        y = runs.mean(axis=0)
        e = runs.std(axis=0) / np.sqrt(N) * 3

        ax.plot(x, y, lw=2, label=method)
        ax.fill_between(x, y-e, y+e, color=ax.lines[-1].get_color(), alpha=0.1)

    ax.axis('tight')
    ax.axis(xmin=0, xmax=T)
    ax.set_xlabel('iterations')
    ax.set_ylabel('function value')
    ax.legend(loc='best')
    ax.figure.canvas.draw()

    # save figure
    figpath = os.path.dirname(os.path.realpath(__file__))
    figpath = os.path.join(figpath, 'figures')
    if not os.path.isdir(figpath):
        os.mkdir(figpath)
    figpath = os.path.join(figpath, '{}.pdf'.format(function))
    print figpath
    ax.figure.savefig(figpath, bbox_inches='tight')

