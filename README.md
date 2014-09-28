spex
====

This repository is meant to facilitate running experiments with
spearmint. It requires a working
[spearmint repo](http://github.com/JasperSnoek/spearmint "spearmint"),
and [jug](http://luispedro.org/software/jug "jug") which is used to
process batch experiments and can simply be installed using pip, i.e.,

    pip install jug

Once spearmint and jug are properly installed, all you need to do is
write a configuration [yaml](http://www.yaml.org/ "yaml") file that
corresponds to the experiment you wish to run. A sample configuration
file can be found at `spex/experiments/branin/branin.yaml`.

Configuring, running, and visualizing results of this experiment can
be accomplished using the following three commands from the `spex`
home directory:

    python replicate.py experiments/branin

    bash jug-execute.sh experiments/branin -n 8

    python plot.py experiments/branin

where in the second line we have set 8 processes to run (in the
background). Note that, naturally, the last line (plotting the
results) can only be run when the jug tasks are done executing. You
can monitor the progress of said tasks by running:

    jug status experiments/branin/execute.py

If you prefer to plot or manipulate the results yourself, you can
also run:

    python gather.py experiments/branin

which will pickle the results in `results/branin.pkl`.

Alternatively, the `replicate.py` script will give you the exact
command to run on a cluster to submit a job to TORQUE. It will look
something like:

    qsub -l walltime=24:00:00,mem=4gb -t 1-10 path/to/execute.pbs

The experiments can be fully cleaned up (leaving the config file
intact) by running:

    bash clean.sh experiments/branin

or all of them by running `bash cleanup.sh experiments/*`.

