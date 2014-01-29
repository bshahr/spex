import pylab as pl
import numpy as np
import seaborn as sns
from bo.demos.testFuncs import computeBest
import pandas as pd
from scipy.stats.mstats import mquantiles

def lineplot(title, results, logscale=False, y_minmax=None):
	fig = pl.figure()
	if not logscale:
		ylabel = 'Min Function Value'
	else:
		ylabel = 'Performance Gap'

	minval = np.inf; maxval = -np.inf
	for key in results.keys():
		result = results[key][0]
		maxx = result.shape[1]
		mean = np.mean(result, axis=0)
		std = np.sqrt(np.var(result, axis=0))
		minvali = np.min(mean-std); maxvali = np.max(mean+std);
		if minvali < minval:
			minval = minvali
		if maxvali > maxval:
			maxval = maxvali


		quants = mquantiles(result, prob=[0.2, 0.5, 0.8], axis=0)
		x_indices = np.arange(mean.shape[0])+1

		pl.fill_between(x_indices, quants[0, :], quants[2, :], \
			facecolor=results[key][1], alpha=0.2)
		a = pl.plot(x_indices, quants[1, :], color=results[key][1], \
			linestyle='-', linewidth=4.0, label=key)

		# for i in xrange(result.shape[0]):
		# 	pl.plot(x_indices, result[i, :], color=results[key][1], \
		# 		linestyle='-', linewidth=.4)

		# a = sns.tsplot(result, err_style="boot_traces", \
		# 	n_boot=5*result.shape[0], label=key, color=results[key][1])
		# pl.fill_between(x_indices, mean-std, mean+std, \
		# 	facecolor=results[key][1], alpha=0.2)
		# a = pl.plot(x_indices, mean, color=results[key][1], \
		# 	linestyle='-', linewidth=4.0, label=key)

	pl.legend(borderaxespad=0.2, fontsize=16)
	pl.ylabel(ylabel, fontsize=16)
	if logscale:
		pl.yscale('log')
		pl.grid(False, which='minor', axis='y')

	pl.xlabel('No. of Fct. Evaluations ($t$)', fontsize=16)
	if y_minmax is not None:
		pl.axis([1, maxx, y_minmax[0], y_minmax[1]])

	pl.title(title, fontsize=20)

	pl.savefig('{}.pdf'.format(title), bbox_inches='tight', dpi=200)
	fig.clf()

if __name__ == '__main__':
	############################################################################
	# Branin
	resultBrEI = np.load('./results/result-braninpy-7859558362.npy')[:, :100]
	resultBrT = np.load('./results/result-Th-braninpy-7196187393.npy')[:, :100]

	resultBrEI = np.exp(resultBrEI * np.log(10))
	resultBrT = resultBrT + computeBest('branin')/10.

	results = {'EI-MCMC':(resultBrEI, 'blue'), \
			   'Thompson-MCMC':(resultBrT, 'green')}
	title = 'Branin'
	lineplot(title, results, logscale=True)
	############################################################################


	############################################################################
	# Hartman 3
	resultBrEI = np.load('./results/result-hart3py-7277509593.npy')[:, :100]
	resultBrT = np.load('./results/result-Th-hart3py-5136959805.npy')[:, :100]


	resultBrEI = np.vstack([resultBrEI[:12, :], resultBrEI[13:, :]])
	resultBrEI = np.exp(resultBrEI * np.log(10))
	resultBrT = resultBrT + computeBest('hart3')
	results = {'EI-MCMC':(resultBrEI, 'blue'), \
			   'Thompson-MCMC':(resultBrT, 'green')}
	title = 'Hartmann 3'
	lineplot(title, results, logscale=True)
	############################################################################




	############################################################################
	# LDA
	# resultLADT = np.load('./results/result-Th-lda_grid-4469183616.npy')[:, :50]
	# resultLADEI = np.load('./results/result-EI-lda_grid-9417714409.npy')[:, :50]

	# resultLADT = np.load('./results/result-Th-lda_grid-7135130493.npy')[:, :50]
	# resultLADT = np.load('./results/result-Th-lda_grid-8162842191.npy')[:, :50]
	# resultLADEI = np.load('./results/result-EI-lda_grid-9209722279.npy')[:, :50]
	# resultLADT = resultLADT[1:, :]
	# resultLADEI = np.vstack([resultLADEI[:-2, :], resultLADEI[-1, :]])
	



	resultLADT = np.load('./results/result-Th-lda_grid-8741739500.npy')[:, :50]
	resultLADEI = np.load('./results/result-EI-lda_grid-9515508804.npy')[:, :50]
	results = {'Thompson-MCMC':(resultLADT, 'green'), \
			   'EI-MCMC':(resultLADEI, 'blue')}
	title = 'LDA'
	lineplot(title, results, y_minmax=(1264, 1350))
	############################################################################




	############################################################################
	# SVM
	# resultSVMEI = np.load('./results/result-EI-svm_grid-6855126410.npy')[:, :100]
	# resultSVMTh = np.load('./results/result-Th-svm_grid-7951017795.npy')[:, :100]

	# resultSVMEI = np.load('./results/result-EI-svm_grid-5165881950.npy')[:, :100]
	# resultSVMTh = np.load('./results/result-Th-svm_grid-2661913354.npy')[:, :100]
	
	# resultSVMEI = np.vstack([resultSVMEI[:-7, :], resultSVMEI[-6:, :]])
	# resultSVMTh = resultSVMTh[:-1, :]

	resultSVMEI = np.load('./results/result-EI-svm_grid-7518851186.npy')[:, :100]
	resultSVMTh = np.load('./results/result-Th-svm_grid-7254250177.npy')[:, :100]

	results = {'EI-MCMC':(resultSVMEI, 'blue'), \
			   'Thompson-MCMC':(resultSVMTh, 'green')}
	title = 'SVM'
	lineplot(title, results, y_minmax=(0.24, 0.28))
	############################################################################


	############################################################################
	# Logistic
	resultLogEI = np.load('./results/result-EI-logistic_hpolib-7792985020.npy')[:, :100]
	resultLogTh = np.load('./results/result-Th-logistic_hpolib-8917306460.npy')[:, :100]
	
	results = {'EI-MCMC':(resultLogEI, 'blue'), \
			   'Thompson-MCMC':(resultLogTh, 'green')}
	title = 'Logistic'
	lineplot(title, results, y_minmax=(0.065, 0.1))

