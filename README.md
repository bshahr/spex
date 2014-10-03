spex
====

This repository is meant to facilitate running experiments with
spearmint.

Installation
--------------

`spex` requires a working
[spearmint repo](http://github.com/JasperSnoek/spearmint "spearmint"),
and [jug](http://luispedro.org/software/jug "jug") which is used to
process batch experiments and can simply be installed using pip, i.e.,

    pip install jug

Running
-----------

Once spearmint and jug are properly installed, all you need to do is
write a configuration [yaml](http://www.yaml.org/ "yaml") file that
corresponds to the experiment you wish to run. A sample configuration
file can be found at `spex/experiments/branin/branin.yaml`.

Configuring and running an experiment can be accomplished using
the following commands from the `spex` home directory:

    python replicate.py experiments/branin

    bash jug-execute.sh experiments/branin -n 8

where in the second line we have set 8 processes to run (in the
background).

Monitoring progress
--------------------------

You can monitor the progress of all tasks in an experiment by running:

    jug status experiments/branin/execute.py


Visualizing results
------------------------

You can plot the average performance with confidence bands (± 3
standard errors) with the following command:

    python plot.py experiments/branin

Naturally, this can only be run when the jug tasks are done executing.
If you prefer to plot or manipulate the results yourself, you can
also run:

    python gather.py experiments/branin

which will pickle the results in `results/branin.pkl`.

Submitting jobs to TORQUE
-------------------------------------

Alternatively, the `replicate.py` script will give you the exact
command to run on a cluster to submit a job to TORQUE. It will look
something like:

    qsub -l walltime=24:00:00,mem=4gb -t 1-10 path/to/execute.pbs

Cleaning up
----------------

The experiments can be fully cleaned up (leaving the config file
intact) by running:

    bash clean.sh experiments/branin

or all of them by running `bash cleanup.sh experiments/*`.