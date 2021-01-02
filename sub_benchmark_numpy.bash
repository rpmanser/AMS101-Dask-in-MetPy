#!/bin/bash
# =============================================================================
# sub_benchmark_numpy.bash
#
# Write a submission script to run benchmark tests for numpy arrays in metpy.
#
# Parameters
# ----------
# ncores : int
#   Number of cores to use
# nruns : int
#   The number of times to run the calculations
# config : path
#   Absolute path to the config.bash file in this directory (change its
#   settings before running this script)
#
# Data is written to numpy_{ncores}.csv in the directory dir_data specified
# in config.bash
#
# Author: Russell Manser
# Created: 12/15/20
# =============================================================================

ncores=$1
nruns=$2
config=$3

source $config

# Create a phony job ID to make clean up easier
jobid=`date +"%H%M%S%N"`

# Create the submissions script
cat > numpy${ncores}.bash << END_INPUT

#!/bin/sh
#$ -V
#$ -cwd
#$ -S /bin/bash
#$ -N metpy_numpy
#$ -o metpy_numpy.o${jobid}.1
#$ -e metpy_numpy.e${jobid}.1
#$ -q omni
#$ -pe sm ${ncores}
#$ -P quanah

$pyenv ${dir_scripts}/benchmark_numpy.py $ncores $nruns $dir_data

END_INPUT

# Run the script and clean up after ourselves
qsub numpy${ncores}.bash
rm numpy${ncores}.bash
