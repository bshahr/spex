#!/bin/bash
#
# Script for cleaning up experiment directories.
#
# After this script is run, the experiment directory is returned to
# its state before replicate.py was run, i.e., with only a yaml file
# for configuration.
#
# Usage:
#
#   bash cleanup.sh experiments/<experiment_directory>
#
# or, to clean all experiments directories:
#
#   bash cleanup.sh experiments/*
#
#
# Bobak Shahriari
# 25 September 2014
#

for EXPT in $@; do
    # delete experiment subdirectories
    EXPT_PATH=$(pwd)/$EXPT
    LIST_PATH=`find $EXPT_PATH/* -type d`

    # check for empty string (null string)
    if [[ -n "$LIST_PATH" ]]; then
        rm -rf `ls -d $EXPT_PATH/*/`
    fi

    # delete execute.py script if it exists
    EXE_SCRIPT=$EXPT_PATH/execute.py

    if [[ -e "$EXE_SCRIPT" ]]; then
        rm $EXE_SCRIPT
    fi
done

# unset environment variables
unset EXPT_PATH
unset LIST_PATH
unset EXE_SCRIPT
