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

        quants = mquantiles(result, prob=[0.25, 0.5, 0.75], axis=0)
        x_indices = np.arange(mean.shape[0])+1

        pl.fill_between(x_indices, quants[0, :], quants[2, :], \
            facecolor=results[key][1], alpha=0.2)
        a = pl.plot(x_indices, quants[1, :], color=results[key][1], \
            linestyle='-', linewidth=4.0, label=key)

        # for i in xrange(result.shape[0]):
        #   pl.plot(x_indices, result[i, :], color=results[key][1], \
        #       linestyle='-', linewidth=.4)

        # a = sns.tsplot(result, err_style="boot_traces", \
        #   n_boot=5*result.shape[0], label=key, color=results[key][1])
        # pl.fill_between(x_indices, mean-std, mean+std, \
        #   facecolor=results[key][1], alpha=0.2)
        # a = pl.plot(x_indices, mean, color=results[key][1], \
        #   linestyle='-', linewidth=4.0, label=key)

    pl.legend(borderaxespad=0.2, fontsize=16)
    pl.ylabel(ylabel, fontsize=16)
    if logscale:
        pl.yscale('log')
        pl.grid(False, which='minor', axis='y')
    pl.xlabel('No. of Fct. Evaluations ($t$)', fontsize=16)
    if y_minmax is not None:
        pl.axis([1, maxx, y_minmax[0], y_minmax[1]])

    pl.title(title, fontsize=20)

    print 'Plotting for {}.'.format(title)
    pl.savefig('{}.pdf'.format(title), bbox_inches='tight', dpi=200)
    # fig.clf()


def parse_yaml(yaml_file):
    import yaml
    f = open(yaml_file)
    dataMap = yaml.safe_load(f)
    f.close()

    for key in dataMap.keys():
        dictionary = {}
        number = int(dataMap[key]['number'])
        logscale = False
        y_minmax = None
        if 'min' in dataMap[key]:
            min_y = float(dataMap[key]['min'])
            max_y = float(dataMap[key]['max'])
            y_minmax = (min_y, max_y)
        for subkey in dataMap[key]['methods']:
            dataMap[key]['methods'][subkey]
            best = 0
            if 'function' in dataMap[key]['methods'][subkey]:
                best = computeBest(dataMap[key]['methods'][subkey]['function'])
                if key == 'Branin':
                    best = best/10.
                logscale = True

            result = np.load('./results/{}'.format(\
                dataMap[key]['methods'][subkey]['file']))[:, :number] + best
            dictionary[dataMap[key]['methods'][subkey]['name']] = \
                (result, dataMap[key]['methods'][subkey]['color'])

        lineplot(key, dictionary, logscale=logscale, y_minmax=y_minmax)



if __name__ == '__main__':

    parse_yaml('ro_plot_config.yaml')

    # ############################################################################
    # # # Branin
    # resultBrEI = np.load('./results/result-braninpy-7859558362.npy')[:, :100]
    # # resultBrT = np.load('./results/result-Th-braninpy-7196187393.npy')[:, :100]
    # resultBrEI = np.exp(resultBrEI * np.log(10))

    # resultBrEI = np.load('./results/result-EI-braninpy-5010613689.npy')[:, :100]
    # resultBrEIR = np.load('./results/result-EIR-braninpy-7392077481.npy')[:, :100]
    # resultBrT = np.load('./results/result-Th-braninpy-9300183398.npy')[:, :100]
    # resultBrPF = np.load('./results/result-PF-braninpy-8083955903.npy')[:, :100]
    

    # resultBrEIR = resultBrEIR + computeBest('branin')/10.
    # resultBrEI = resultBrEI + computeBest('branin')/10.
    # # resultBrT = resultBrT + computeBest('branin')/10.
    # # resultBrPF = resultBrPF + computeBest('branin')/10.

    # results = {'RO-MCMC':(resultBrEIR, 'green'), \
    #            'EI-MCMC':(resultBrEI, 'blue')}
    # title = 'Branin'
    # lineplot(title, results, logscale=True)
    # ############################################################################




    # ############################################################################
    # # Hartman 3
    # resultBrEI = np.load('./results/result-EI-hart3py-1102589765.npy')[:, :100]
    # # resultBrT = np.load('./results/result-Th-hart3py-1333674245.npy')[:, :100]
    # # resultBrPH = np.load('./results/result-PF-hart3py-7745891638.npy')[:, :100]
    # resultBrRO = np.load('./results/result-EIR-hart3py-3850523492.npy')[:, :100]

    # print resultBrRO
    # print computeBest('hart3')


    # resultBrEI = resultBrEI + computeBest('hart3')
    # # resultBrT = resultBrT + computeBest('hart3')
    # # resultBrPH = resultBrPH + computeBest('hart3')
    # resultBrRO = resultBrRO + computeBest('hart3')


    # results = {'EI-MCMC':(resultBrEI, 'blue'), 
    #          'RO-MCMC':(resultBrRO, 'green')}
    # title = 'Hartmann 3'
    # lineplot(title, results, logscale=True)
    # ############################################################################




    ############################################################################
    # LDA
    # resultLADT = np.load('./results/result-Th-lda_grid-4469183616.npy')[:, :50]
    # resultLADEI = np.load('./results/result-EI-lda_grid-9417714409.npy')[:, :50]

    # resultLADT = np.load('./results/result-Th-lda_grid-7135130493.npy')[:, :50]
    # resultLADT = np.load('./results/result-Th-lda_grid-8162842191.npy')[:, :50]
    # resultLADEI = np.load('./results/result-EI-lda_grid-9209722279.npy')[:, :50]
    # resultLADT = resultLADT[1:, :]
    # resultLADEI = np.vstack([resultLADEI[:-2, :], resultLADEI[-1, :]])
    
    # resultLADT = np.load('./results/result-Th-lda_grid-8741739500.npy')[:, :50]
    # resultLADEI = np.load('./results/result-EI-lda_grid-9515508804.npy')[:, :50]
    # resultLADPF = np.load('./results/result-PF-lda_grid-2753162303.npy')[:, :50]

    # print np.sort(resultLADT[:, 0])
    # print np.sort(resultLADEI[:, 0])
    # print np.sort(resultLADPF[:, 0])
    
    # results = {'Thompson-MCMC':(resultLADT, 'green'), \
    #          'EI-MCMC':(resultLADEI, 'blue'), \
    #          'PF-MCMC':(resultLADPF, 'red')}
    # title = 'LDA'
    # lineplot(title, results, y_minmax=(1264, 1350))
    ############################################################################




    ############################################################################
    # SVM
    # resultSVMEI = np.load('./results/result-EI-svm_grid-6855126410.npy')[:, :100]
    # resultSVMTh = np.load('./results/result-Th-svm_grid-7951017795.npy')[:, :100]

    # resultSVMEI = np.load('./results/result-EI-svm_grid-5165881950.npy')[:, :100]
    # resultSVMTh = np.load('./results/result-Th-svm_grid-2661913354.npy')[:, :100]
    
    # resultSVMEI = np.vstack([resultSVMEI[:-7, :], resultSVMEI[-6:, :]])
    # resultSVMTh = resultSVMTh[:-1, :]

    # resultSVMEI = np.load('./results/result-EI-svm_grid-7518851186.npy')[:, :100]
    # resultSVMTh = np.load('./results/result-Th-svm_grid-7254250177.npy')[:, :100]
    # resultSVMPF = np.load('./results/result-PF-svm_grid-2866798955.npy')[:, :100]

    # print np.sort(resultSVMEI[:, 0])
    # print np.sort(resultSVMTh[:, 0])
    # print np.sort(resultSVMPF[:, 0])

    # results = {'EI-MCMC':(resultSVMEI, 'blue'), \
    #          'Thompson-MCMC':(resultSVMTh, 'green'), \
    #          'PF-MCMC':(resultSVMPF, 'red')}
    # title = 'SVM'
    # lineplot(title, results, y_minmax=(0.24, 0.28))
    ############################################################################




    ############################################################################
    # Logistic
    # resultLogEI = \
    #   np.load('./results/result-EI-logistic_hpolib-7792985020.npy')[:, :100]
    # resultLogTh = \
    #   np.load('./results/result-Th-logistic_hpolib-8917306460.npy')[:, :100]
    # resultLogPf = \
    #   np.load('./results/result-PO-logistic_hpolib-8752363857.npy')[:, :100]

    
    # results = {'EI-MCMC':(resultLogEI, 'blue'), \
    #          'Thompson-MCMC':(resultLogTh, 'green'), \
    #          'PF-MCMC':(resultLogPf, 'red')}
    # title = 'Logistic'
    # lineplot(title, results, y_minmax=(0.065, 0.1))
    ############################################################################




    ############################################################################
    # Random Forest
    # resultLogEI = np.load('./results/result-EI-skrf-1356361364.npy')[:, :100]
    # resultLogTh = np.load('./results/result-Th-skrf-2482106596.npy')[:, :100]
    # resultLogPF = np.load('./results/result-PF-skrf-7499149250.npy')[:, :100]


    # results = {'EI-MCMC':(resultLogEI, 'blue'), \
    #          'Thompson-MCMC':(resultLogTh, 'green'), \
    #          'PF-MCMC':(resultLogPF, 'red')}
    # title = 'Rf'
    # lineplot(title, results, y_minmax=(0.04, 0.1))
    ############################################################################

    ############################################################################
    # Random Forest
    # resultLogEI = np.load('./results/result-EI-repeller-7911680856.npy')[:, :150]
    # resultLogTh = np.load('./results/result-Th-repeller-7900098689.npy')[:, :150]
    # resultLogPF = np.load('./results/result-PF-repeller-9662669862.npy')[:, :150]


    # results = {'EI-MCMC':(resultLogEI, 'blue'), \
    #          'Thompson-MCMC':(resultLogTh, 'green'), \
    #          'PF-MCMC':(resultLogPF, 'red')}
    # title = 'Repeller'
    # lineplot(title, results, y_minmax=(-35., -5.))
    ############################################################################



