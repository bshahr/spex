import pylab as pl
import numpy as np
import seaborn as sns
import pandas as pd


def lineplot(title, results, logscale=False, y_minmax=None):
	fig = pl.figure()
	if not logscale:
		ylabel = 'Min Function Value'
	else:
		ylabel = 'Log Dis. to Optimal'

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

		x_indices = np.arange(mean.shape[0])+1

		a = sns.tsplot(result, err_style="boot_traces", \
			n_boot=result.shape[0], label=key, color=results[key][1])
		# pl.fill_between(x_indices, mean-std, mean+std, \
		# 	facecolor=results[key][1], alpha=0.2)
		# a = pl.plot(x_indices, mean, color=results[key][1], \
		# 	linestyle='-', linewidth=4.0, label=key)

	pl.legend(borderaxespad=0.2)
	pl.ylabel(ylabel, fontsize=20)
	if logscale:
		pl.yscale('log')
	pl.xlabel('No. of Fct. Evaluations ($t$)', fontsize=20)
	if y_minmax is not None:
		pl.axis([0, maxx, y_minmax[0], y_minmax[1]])

	pl.title(title, fontsize=20)

	pl.savefig('{}.pdf'.format(title), bbox_inches='tight', dpi=200)
	fig.clf()

if __name__ == '__main__':
	############################################################################
	# Branin
	# resultBrEI = np.load('./results/result-braninpy-7859558362.npy')[:, :100]
	# resultBrT = np.load('./results/out-branin-8683685435.npy')[:, :100]

	# resultBrEI = np.exp(resultBrEI * np.log(10))
	# resultBrT = np.exp(resultBrT * np.log(10))

	# results = {'EI-MCMC':(resultBrEI, 'blue'), \
	# 		   'Thompson-MCMC':(resultBrT, 'green')}
	# title = 'Branin'
	# lineplot(title, results, logscale=True)
	############################################################################


	############################################################################
	# Hartman 3
	# resultBrEI = np.load('./results/result-hart3py-7277509593.npy')[:, :100]
	# resultBrT = np.load('./results/out-hart3-2626550518.npy')[:, :100]

	# resultBrEI = np.exp(resultBrEI * np.log(10))
	# resultBrT = np.exp(resultBrT * np.log(10))
	# results = {'EI-MCMC':(resultBrEI, 'blue'), \
	# 		   'Thompson-MCMC':(resultBrT, 'green')}
	# title = 'Hartmann 3'
	# lineplot(title, results, logscale=True)
	############################################################################




	############################################################################
	# LDA
	resultLADT = np.load('./results/result-Th-lda_grid-8362524370.mat.npy')[:, :50]

	print resultLADT
	resultLADEI = np.load('./results/result-EI-lda_grid-6460751781.npy')[:, :50]
	results = {'EI-MCMC':(resultLADEI, 'blue'), \
			   'Thompson-MCMC':(resultLADT, 'green')}
	title = 'LDA'
	lineplot(title, results, y_minmax=(1264, 1272))
	############################################################################




	############################################################################
	# SVM
	resultSVMEI = np.load('./results/result-EI-svm_grid-3536553150.npy')[:, :100]
	resultSVMTh = np.load('./results/result-Th-svm_grid-9116037553.mat.npy')[:, :100]
	
	results = {'EI-MCMC':(resultSVMEI, 'blue'), \
			   'Thompson-MCMC':(resultSVMTh, 'green')}
	title = 'SVM'
	lineplot(title, results, y_minmax=(0.24, 0.3))
	############################################################################


	############################################################################
	# Logistic
	# resultLogEI = np.load('./results/result-EI-logistic-8569332912.npy')[:, :100]
	# resultLogTh = np.load('./results/result-Th-svm_grid-5098544060.npy')[:, :100]
	
	# results = {'EI-MCMC':(resultLogEI, 'blue')}
	# title = 'Logistic'
	# lineplot(title, results)


	# seaborn_plot()
