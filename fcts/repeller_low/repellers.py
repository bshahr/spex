from __future__ import division
from numpy import *
import numpy as np
import matplotlib.pylab as mpl
import pickle

class RepellersModel:
    def __init__(self, weights, centers, scales):
        # parameters controlling the initial state distribution.
        self.initRangeX = r_[-.5, .5]
        self.initRangeY = r_[-.2, .3]

        # parameters controlling the transition model.
        self.gravity = .03
        self.viscosity = 0.1
        self.sigma = .02

        # parameters controlling the rewards.
        self.weights = array(weights, ndmin=1, copy=True)
        self.centers = array(centers, ndmin=2, copy=True)
        self.scales = array(scales, ndmin=2, copy=True)
        print 'weights =', self.weights
        print 'centers =', self.centers
        print 'scales =', self.scales

    def sampleInit(self, N):
        """Return N samples from the initial state model."""
        return random.uniform(
            low  = r_[self.initRangeX[0], self.initRangeY[0], 0., 0.],
            high = r_[self.initRangeX[1], self.initRangeY[1], 0., 0.],
            size = [N,4])

    def sampleTransition(self, x, u):
        """Sample transitions given N states and actions x[i] and u[i]."""
        xnew = x.copy()
        xnew[:,2:4] *= (1.0 - self.viscosity)
        xnew[:,2:4] += u + r_[0, -self.gravity]
        xnew[:,0:2] += xnew[:,2:4]
        xnew[:,2:4] += random.normal(scale=self.sigma, size=(x.shape[0], 2))
        return xnew

    def samplePolicy(self, theta, x):
        """
        Sample actions u[i] for each of N states x[i], where the policy is
        parameterized by theta. In particular theta is a collection of 3-tuples
        where theta[3n] is the force of the nth repulsor and theta[3n+1:3n+2]
        are the x and y positions.
        """
        u = 0.0
        for (w,xpos,ypos) in asarray(theta).reshape(-1,3):
            d = x[:,0:2] - r_[xpos,ypos] + .001
            d2 = sum(d**2, axis=1).reshape(-1,1)
            u += w * d / (d2**1.5)
        return u

    def sampleReward(self, x):
        """Sample rewards for each given state x[i]."""
        r = 0.0
        for w, center, scale in zip(self.weights, self.centers, self.scales):
            a = (x[:,0:2]-center) / scale
            r += w * exp(-0.5 * sum(a**2, axis=1))
        return r

    def samplePaths(self, theta, N, horizon):
        """Sample paths (position only) under the given policy."""
        paths = []
        x = self.sampleInit(N)
        for t in xrange(horizon):
            paths.append(x[:,0:2])
            u = self.samplePolicy(theta, x)
            x = self.sampleTransition(x,u)
        return swapaxes(paths, 0, 1)

    def getExpectedReward(self, theta, N=10000, horizon=50, gamma=1.0):
        """
        Get the expected reward for the given policy where we use N sample
        paths, each with the given time horizon and use a discount factor of
        gamma.
        """
        x = self.sampleInit(N)
        r = 0.0
        for n in xrange(horizon):
            r += (gamma**n) * sum(self.sampleReward(x)) / N
            u = self.samplePolicy(theta, x)
            x = self.sampleTransition(x, u)
        return r

    def plot(self, ax, theta=None, N=0, horizon=20):
        """
        Make an informative plot of the model. If theta is not None display the
        repellers and if N is also greater than zero then plot some sample paths
        with the given time horizon.
        """
        # import matplotlib.pyplot as pl
        # ax = pl.gca()
        # ax.cla()

        # make contours of the reward.
        X, Y = meshgrid(linspace(-5,5), linspace(-5,2))
        R = self.sampleReward(c_[X.flatten(),Y.flatten()]).reshape(X.shape)
        ax.contour(X, Y, R)

        # draw the initial state distribution.
        ax.add_patch(mpl.Rectangle(
            r_[self.initRangeX[0], self.initRangeY[0]],  # corner of the rect.
            self.initRangeX[1] - self.initRangeX[0],     # width.
            self.initRangeY[1] - self.initRangeY[0],     # height.
            edgecolor=(0.5, 0.5, 0.0),
            facecolor=(1.0, 1.0, 0.8)))

        # draw the repellers if any are given.
        if theta is not None:
            print theta
            print asarray(theta).reshape(-1,3)
            for (w,xpos,ypos) in asarray(theta).reshape(-1,3):
                print xpos, ypos, w
                ax.plot([xpos], [ypos], 'o', ms=max([2,200*w]), alpha=0.3)

        # draw some paths.
        if N>0 and theta is not None:
            paths = self.samplePaths(theta, N, horizon)
            for i in xrange(len(paths)):
                ax.plot(paths[i,:,0], paths[i,:,1], '.-')

        # draw everything
        # ax.draw_if_interactive()
        ax.set_xbound(-10, 10)
        ax.set_ybound(-10, 2)

if __name__ == '__main__':
    # CREATE THE REWARD MODEL.
    params = {}
    params['weights'] = [1, 1, 1, 1]
    params['centers'] = [(0,-2), (-3, -3), (-2, -2), (-2, -4.3)]
    params['scales' ] = [(0.5, 0.5), (0.3, 0.3), (0.5, 0.5), (0.3, 0.3)]

    model = RepellersModel(**params)

    # REASONABLE BOUNDS.
    bounds = [[0., .5], [-8, 0], [-8, 0],
              [0., .5], [0, 8], [-8, 0],
              [0., .5], [-8, 8], [-6, 4]]

    # EVALUATE A PARTICULAR THETA.
    theta = [
        .2,  0.00, -4.50,
        .07, -5, -2,
        .1,  1.99, -3.50]
    theta = [0.192545069468, -2.59824457337, -4.77624027894, 0.450462078346, 
            2.54726731266, -5.78219533407, 0.0520929864638, -6.12032709961, 
            -5.2387726667]


    print model.getExpectedReward(theta)
    model.plot(mpl.gca(), theta, N=10, horizon=100)
    mpl.axis([-6, 5, -8, 1])
    mpl.savefig('repellers.pdf', bbox_inches='tight')

def main(job_id, params):
    # CREATE THE REWARD MODEL.
    mparams = {}
    mparams['weights'] = [1, 1, 1, 1]
    mparams['centers'] = [(0,-2), (-3, -3), (-2, -2), (-2, -4.3)]
    mparams['scales' ] = [(0.5, 0.5), (0.3, 0.3), (0.5, 0.5), (0.3, 0.3)]

    model = RepellersModel(**mparams)
    bounds = np.array([[0., .5], [-8, 8], [-8, 0], \
        [0., .5], [-8, 8], [-8, 0], \
        [0., .5], [-8, 8], [-8, 0]] )


    theta = bounds[:, 0] + params['X']*(bounds[:, 1] - bounds[:, 0])

    print 'theta is:', [str(x) for x in theta]
    return -model.getExpectedReward(theta)

# if __name__ == '__main__':

#     params = {'X': np.array([0.929045393352, 0.687864855499, 0.0, 0.747314133915, 0.395931109638, \
#     0.257882271251, 0.671253438556, 1.0, 0.680440180762])}


#     # params = {'X': np.array([0.342468261719, 0.802307128906, 0.512634277344, \
#     #     0.595275878906, 0.592468261719, 0.312561035156, 0.472473144531, 0.986755371094, 0.602478027344])}
#     # params = {'X': np.array([0.6, 0.6, 0.6, 0.2, .2, .3, .5, .5, .5])}
#     print main(1, params)
