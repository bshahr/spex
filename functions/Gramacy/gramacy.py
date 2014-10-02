import pybo


def gramacy(x):
    sn = 0.1    # noise
    function = pybo.functions.Gramacy(sn)

    return -function(x)


def main(jobid, params):
    return gramacy(params['X'])
