import pylab as pl
import numpy as np

def first(filename, name='EI-MCMC'):
	result = np.load(filename)

	mean = np.mean(result, axis=0)
	std = np.sqrt(np.var(result, axis=0))
	x_indices = np.arange(mean.shape[0])+1
	pl.fill_between(x_indices, mean-std, mean+std, color='red', alpha=0.2)
	first = pl.plot(x_indices, mean, color='red', \
    	linestyle='-', linewidth='4.0', label=name)

	pl.legend(borderaxespad=0.2)
	pl.ylabel('Log Distance to optimal', fontsize=20)
	pl.xlabel('No. of Iterations ($t$)', fontsize=20)
	pl.axis([1, 150, np.floor(np.min(mean))-0.5, np.ceil(np.max(mean))+0.5])

	pl.show()

if __name__ == '__main__':
	first('./result-braninpy-7859558362.mat.npy')

