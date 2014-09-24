import numpy as np
import sys
import math
import time
import logistic_sgd

def logistic(params):
  learning_rate=params['lrate']
  n_epochs=params['n_epochs']
  dataset='mnist.pkl.gz'
  batch_size = params['batchsize']
  l1_reg=0#params['l1_reg']
  l2_reg=params['l2_reg']

  y = logistic_sgd.sgd_optimization_mnist(learning_rate=learning_rate, n_epochs=n_epochs, dataset='mnist.pkl.gz', batch_size = batch_size, l1_reg=l1_reg, l2_reg=l2_reg)
  
  result = y;
  #time.sleep(5)

  return result

# Write a function like this called 'main'
def main(job_id, params):
  print params
  return logistic(params)
