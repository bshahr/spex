import numpy as np
import numpy.random as nr
import subprocess

def convert(params):
    path = \
        '/home/ziyuw/projects/jointtracking_ziyu/depth_to_bodyparts/'
    
    padding = np.array([500000, 0.001, 100, 0.001, 100])
    params = np.hstack([params[0], padding, params[1:]])

    param_dict = {'key{}'.format(key): value for \
        (key, value) in enumerate(params)}
    param_dict['dataset_name'] = '1000_dataset_1000000'
    param_dict['path'] = path
    
    
    discrete_indices = ['key0', 'key1', 'key3', 'key5', 'key6', 'key7', 'key8']
    for key in discrete_indices:
        param_dict[key] = int(param_dict[key])

    return 'python {path}pipeline/02_train_class_trees.py -i {path}data/{dataset_name}/02_bundled_train/ -v {path}data/{dataset_name}/02_bundled_test/ -o ../data/1000_dataset_1000000/03_tree/ -j 2 -c 5 -n 50 -b {key0} -S {key1} -rs {key2} -ms {key3} -rt {key4} -mt {key5} -g 0 -d {key6} -s {key7} -t {key8} -umeanx {key9} -umeany {key10} -uvarx {key11} -uvary {key12} -uvarxy {key13} -vmeanx {key14} -vmeany {key15} -vvarx {key16} -vvary {key17} --vvarxy {key18}'.format(**param_dict)

def transform(params):
    mean_bound = 50.
    param_bounds = \
        np.array([[0, 1], \
        [np.log(1.), np.log(60.)], \
        [1., 100.], \
        [np.log(1.), np.log(5000.)], \
        [-mean_bound, mean_bound], \
        [-mean_bound, mean_bound], \
        [1.0, 200.0], \
        [1.0, 200.0], \
        [1.0, 200.0], \
        [-mean_bound, mean_bound], \
        [-mean_bound, mean_bound], \
        [1.0, 200.0], \
        [1.0, 200.0], \
        [1.0, 200.0]])
    discrete_indices = [0, 1, 2, 3]
    log_indices = [1, 3]
    
    params = params*(param_bounds[:, 1] - param_bounds[:, 0]) + \
        param_bounds[:, 0]

    
    params[log_indices] = np.exp(params[log_indices])
    params[discrete_indices] = np.round(params[discrete_indices])

    return list(params)


def call(x):
    print float(subprocess.check_output(convert(transform(x)).split()))


# Write a function like this called 'main'
def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return call(params['X'])


if __name__ == '__main__':
    x = nr.rand(14)
    call(x)

    