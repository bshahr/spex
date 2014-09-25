#!/bin/bash
 
let MAX_NJOBS=10
let NJOBS=1     # default number of parallel jobs
SCRIPT=$1
OPTIND=2

# fetch number of parallel jobs
while getopts :n: opt; do
  case $opt in
    n)
      let NJOBS=$OPTARG
      ;;
    \?)
      echo "Usage: jug-execute path/to/execute.py [-n NJOBS]"
      ;;
  esac
done

# limit number of parallel jobs to MAX_NJOBS
if (($NJOBS > $MAX_NJOBS)); then
    NJOBS=$MAX_NJOBS
fi

# run NJOBS parallel background jug jobs
let i=0
while (($i < $NJOBS)); do
  let i++
  jug execute $SCRIPT &
done

