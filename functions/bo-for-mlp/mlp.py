from __future__ import division
import numpy as np
import os, re

# network params
ninput = 1
nhidden = 5
noutput = 1
non_linearity = lambda x: 1. / (1. + np.exp(-x))

dim = (ninput + noutput + 1) * nhidden + noutput

def mlp(weights, X):
    # unpack weights
    nlayerin = nhidden * (ninput + 1)
    V = weights[:nlayerin].reshape((nhidden, ninput+1))
    W = weights[nlayerin:].reshape((noutput, nhidden+1))
    # forward pass
    hidden = non_linearity(np.dot(V, X.T))
    hidden = np.vstack((np.ones(len(X)), hidden))
    
    return np.dot(W, hidden).T


def evaluate(weights, X, y):
    yhat = mlp(weights, X)
    return np.sum((yhat - y) ** 2) / len(X)

def generate_data(weights):
    X = np.array(10*np.random.rand(200) - 5, ndmin=2).T
    X = np.hstack((np.ones((len(X), 1)), X))
    y = mlp(weights, X) + 0.001 * np.random.randn(len(X), noutput)

    return X, y

def main(job_id, params):
    lpath = re.sub(r'mlp.pyc?', 'mlp_data.npz', \
        os.path.abspath(__file__))
    data = np.load(lpath)
    return evaluate(params['X'], data['X'], data['y'])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', '-c', default='run',
                        help='generate to regenerate data')
    args = parser.parse_args()

    if args.command == 'run':
        main()
    elif args.command == 'generate':
	    # select random MLP weights and generate data
        weights = np.random.rand(dim)
        print weights
        X, y = generate_data(weights)
        np.savez('mlp_data.npz', X=X, y=y, weights=weights)
