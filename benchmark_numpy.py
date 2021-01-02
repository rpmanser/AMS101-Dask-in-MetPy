# =============================================================================
# benchmark_numpy.py
#
# Benchmark metpy functions with numpy arrays as arguments.
#
# Author: Russell Manser
# Created: 12/9/15
# =============================================================================

import argparse
import time

import pandas as pd

from benchmark import test

parser = argparse.ArgumentParser(description="Run and benchmark numpy jobs")
parser.add_argument('ncores', type=int, help='Number of cores')
parser.add_argument('nruns', type=int, help='Number of iterations to run')
parser.add_argument('dir_data', type=str, help="Directory to save data to")
args = parser.parse_args()
ncores = args.ncores
nruns = args.nruns
dir_data = args.dir_data

index = pd.Index(range(nruns))
columns = [
    'Total Cores',
    'Wall Time',
    'Processor Time',
    'Overhead Time',
]
df = pd.DataFrame(index=index, columns=columns)

for run in range(nruns):
    overhead_start = time.time()
    total_wall, total_proc = test('numpy')
    overhead_end = time.time()

    df.loc[run] = ncores, total_wall, total_proc, overhead_end - overhead_start

df.to_csv(f'{dir_data}/numpy_{ncores}.csv')
