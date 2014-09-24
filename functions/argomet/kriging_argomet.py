import numpy as np
import re, os
import scipy

class KrigingArgomet:
    def __init__(self):
        # Simulated values for: production sampling, stope and development
        # 21577 3 0 -99999 -99999 0
        # X co-ordinate       Y co-ordinate       Gold grade

        path = re.sub(r'kriging_argomet.pyc?', '', \
            os.path.abspath(__file__))

        data = np.loadtxt(path + 'krigingArgomet.csv', delimiter=',')
        print data.shape

        self.D = 2
        self.custom_grid = data[:, 1:]
        
        self.Y = data[:, 0]
        self.n = self.custom_grid.shape[0]
        self.bounds = np.array([(data[:, 1].min(), data[:, 1].max()),
                                (data[:, 2].min(), data[:, 2].max())])
        print self.bounds
        self.best = self.Y.max()


    def kriging_argomet(self, x):
        temp = self.custom_grid/100
        x = x/100
        X = x - temp
        return -self.Y[np.argmin(np.sum(X*X, axis=1))]
        
    def plot(self):
        from matplotlib import rc
        # rc('text', usetex=True)
        from mpl_toolkits.mplot3d import axes3d
        import matplotlib.pyplot as plt
        from matplotlib import cm
        import numpy as np
        import seaborn as sns

        sns.set(style="whitegrid")

        title = 'Kriging Argomet'

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        cmap = sns.blend_palette(["mediumseagreen", "ghostwhite", "#4168B7"], as_cmap=True)

        # ax.plot_wireframe(x1, x2, y, rstride=10, cstride=10, color=colors[0])
        ax.plot_trisurf(self.custom_grid[:,0], self.custom_grid[:,1], self.Y, cmap=cmap, linewidth=0.01)

        # ax.view_init(elev=30., azim=180 + 45 + 10)

        plt.title(title, fontsize=20)

        # plt.savefig('{}.pdf'.format(title), bbox_inches='tight', dpi=200)

        plt.show(block=False)


# Write a function like this called 'main'
def main(job_id, params):
    print 'called'
    ka = KrigingArgomet()
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return ka.kriging_argomet(np.array([params['X'], params['Y']]).flatten())

if __name__ == "__main__":
    k = KrigingArgomet()
    # k.plot()
    print k.kriging_argomet(np.array([100,  50600]))
