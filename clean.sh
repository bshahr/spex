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
#   bash clean.sh experiments/<experiment_directory>
#
# or, to clean all experiments directories:
#
#   bash clean.sh experiments/*
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
    EXE_PY=$EXPT_PATH/execute.py
    EXE_PBS=$EXPT_PATH/execute.pbs

    if [[ -e "$EXE_PY" ]]; then
        rm $EXE_PY
    fi
    if [[ -e "${EXE_PY}c" ]]; then
        rm ${EXE_PY}c
    fi
    if [[ -e "$EXE_PBS" ]]; then
        rm $EXE_PBS
    fi
done

# unset environment variables
unset EXPT_PATH
unset LIST_PATH
unset EXE_PY
unset EXE_PBS
