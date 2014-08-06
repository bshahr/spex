import numpy as np

from gpbo.model import GPModel


class KrigingBrenda:
    def __init__(self, path="/Users/iassael/code/projects/python/RandomForestGP/", use_gp=False):
        # Brenda Mines (Old Brenda), porphyry copper/molybdenum deposit
        # 1800           8           1 -1.0000000E+08
        # X_co-ordinate       Y_co-ordinate       Z_co-ordinate       Cu%
        # Mo%                 length_of_core      From                To
        data = np.loadtxt(path + 'datasets/BrendaMines.csv', delimiter=',')

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
        # print x
        if self.use_gp:
            x = x.reshape((-1, self.D))
            mean, var = self.gp.meanVar(x)
            return mean
        else:
            for i in xrange(self.n):
                if np.allclose(x, self.custom_grid[i, :]):
                    return self.Y[i]

    def plot(self):
        from matplotlib import rc
        # rc('text', usetex=True)
        from mpl_toolkits.mplot3d import axes3d
        import matplotlib.pyplot as plt
        from matplotlib import cm
        import numpy as np
        import seaborn as sns
        from gpbo.demos.functions.gramacy2d import gramacy2d
        from gpbo.util.sobol_lib import i4_sobol_generate

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



if __name__ == "__main__":
    KrigingBrenda().plot()