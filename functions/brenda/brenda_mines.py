import numpy as np
import re, os

class KrigingBrenda:
    def __init__(self, use_gp=False):
        # Brenda Mines (Old Brenda), porphyry copper/molybdenum deposit
        # 1800           8           1 -1.0000000E+08
        # X_co-ordinate       Y_co-ordinate       Z_co-ordinate       Cu%
        # Mo%                 length_of_core      From                To

        path = re.sub(r'brenda_mines.pyc?', '', \
            os.path.abspath(__file__))
        data = np.loadtxt(path + '/BrendaMines.csv', delimiter=',')

        self.D = 3
        self.custom_grid = data[:, :3]
        self.Y = data[:, 4]
        self.n = self.custom_grid.shape[0]
        self.bounds = np.array([(data[:, 0].min(), data[:, 0].max()),
                                (data[:, 1].min(), data[:, 1].max()),
                                (data[:, 2].min(), data[:, 2].max())])
        self.best = self.Y.max()

        self.use_gp = use_gp
        if self.use_gp:
            hyp = np.log(np.ones(self.D + 1))
            self.gp = GPModel(hyp)
            self.gp.addPoints(self.custom_grid, self.Y)
            self.gp.optHyperParam(preconditioning=True)

    def kriging_brenda(self, x):
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

        title = 'Kriging Brenda'

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        cmap = sns.blend_palette(["mediumseagreen", "ghostwhite", "#4168B7"], as_cmap=True)

        # ax.plot_wireframe(x1, x2, y, rstride=10, cstride=10, color=colors[0])
        #ax.plot_trisurf(self.custom_grid[:,0], self.custom_grid[:,1], self.Y, cmap=cmap, linewidth=0.01)
        ax.plot_trisurf(self.custom_grid[:,0], self.custom_grid[:,1], self.custom_grid[:,2], cmap=cmap, linewidth=0.01)

        # ax.view_init(elev=30., azim=180 + 45 + 10)

        plt.title(title, fontsize=20)

        plt.savefig('{}.pdf'.format(title), bbox_inches='tight', dpi=200)


def main(job_id, params):
    print 'called'
    kb = KrigingBrenda()
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return kb.kriging_brenda(np.array([params['X'], params['Y'], params['Z']]).flatten())


if __name__ == "__main__":
    # KrigingBrenda().plot()
    print KrigingBrenda().kriging_brenda(np.array([ 4301., 5192.9653, 5179.4424]))
    print KrigingBrenda().Y[0]