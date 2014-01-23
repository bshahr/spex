import time
import hyperopt
import logistic_sgd
from hyperopt.ht_dist2 import one_of, normal, rSON2

class logistic_hyperopt(hyperopt.Bandit):
    def __init__(self):
        hyperopt.Bandit.__init__(self,
            template=rSON2(
                    'l1_reg', uniform(0, 1),
                    'lrate', uniform(0, 0.1),
                    'batch_size', one_of(20, 2000),
                    'l2_reg', uniform(0, 1),
                    'n_epochs', one_of(5, 2000),
                    ))

    @classmethod
    def evaluate(cls, argd, ctrl):
        rval = {'start_time': time.time()}
        rval['loss'] = logistic_sgd.sgd_optimization_mnist(
            learning_rate=argd['learning_rate', n_epochs=argd['n_epochs'], 
            dataset='mnist.pkl.gz', batch_size = argd['batch_size'], 
            l1_reg=argd['l1_reg'], l2_reg=argd['l2_reg'])

        rval['end_time'] = time.time()
        rval['status'] = 'ok'
        ctrl.info('done')
        return rval
