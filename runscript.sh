#!/bin/bash

# path to spearmint and experiment directory
SPEARMINT=$HOME/spearmint
EXPERIMENT=`pwd`

# path to spearmint's main script
SCRIPT=$SPEARMINT/spearmint/spearmint/main.py

# arguments to pass
FUNCTION=$1
SERIAL=$2
SEED=$3
METHOD=$4
HORIZON=$5
NOISELESS=$6
USEGRAD=$7

# path to config file
CONFIG=$EXPERIMENT/$FUNCTION-$METHOD-$SERIAL/$SEED/config.pb

# run python script
python $SCRIPT \
    --driver=local \
    --method=$METHOD \
    --max-finished-jobs=$HORIZON \
    --method-args=noiseless=$NOISELESS \
    --use-gradient=$USEGRAD \
    --grid-seed=$SEED \
    $CONFIG
    
