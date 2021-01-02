#!/bin/sh
#$ -V
#$ -cwd
#$ -S /bin/bash
#$ -N metpy_dask
#$ -o $JOB_NAME.$JOB_ID.out
#$ -e $JOB_NAME.$JOB_ID.error
#$ -q omni
#$ -pe sm 1
#$ -P quanah

# =============================================================================
# sub_benchmark_dask.py
#
# Run benchmark tests for dask arrays in metpy.
#
# Iterates over running tests on clusters with a number of cores in the range
# ncores_min to ncores_max. In this case, the number of cores is equal to the
# number of workers -- the Python script requests a number of workers equal to
# the number of cores, and each worker uses 1 core.
#
# Parameters
# ----------
# ncores : int
#   Number of cores to use
# nruns : int
#   The number of times to run calculations
# config : path
#   Absolute path to the config.bash file in this directory (change its
#   settings before running this script)
#
# Data is written to dask_{ncores}.csv in the directory dir_data specified
# in config.bash
#
# Author: Russell Manser
# Created: 12/9/15
# =============================================================================

ncores=$1
nruns=$2
config=$3

source $config

# for ncores in `seq $ncores_min 1 $ncores_max`; do
#   $pyenv ${dir_scripts}/benchmark_dask.py $ncores $nruns $dir_data
#   rm ./dask-worker.*
# done

for run in `seq 1 $nruns`; do
  $pyenv ${dir_scripts}/benchmark_dask.py $ncores $dir_data
  rm ./dask-worker.*
done
