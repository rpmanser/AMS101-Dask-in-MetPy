# =============================================================================
# benchmark_dask.py
#
# Benchmark metpy functions with dask arrays as arguments.
#
# Author: Russell Manser
# Created: 12/9/15
# =============================================================================

from pathlib import Path
import argparse
import time

import pandas as pd
from dask_jobqueue import SGECluster
from dask.distributed import Client

from benchmark import test

parser = argparse.ArgumentParser(description='Run and benchmark dask jobs')
parser.add_argument('nworkers', type=int, help='Total number of workers')
parser.add_argument('dir_data', type=str, help="Directory to save data to")
args = parser.parse_args()
nworkers = args.nworkers
dir_data = args.dir_data

overhead_start = time.time()

cluster = SGECluster(
    cores=1,
    memory='5 GB',
    project='quanah',
    queue='omni',
    processes=1,
    job_extra=['-pe sm 1'],
    local_directory='/lustre/scratch/rmanser'
)
cluster.scale(nworkers)
client = Client(cluster)

total_wall, total_proc = test('dask')
overhead_end = time.time()

client.close()
cluster.close()

path = Path(dir_data) / f"dask_{nworkers}.csv"
columns = [
    'Total Cores',
    'Wall Time',
    'Processor Time',
    'Overhead Time',
]
index = pd.Index([0])
data = pd.DataFrame(
    data={
        'Total Cores': nworkers,
        'Wall Time': total_wall,
        'Processor Time': total_proc,
        'Overhead Time': overhead_end - overhead_start,
    },
    index=index
)
if path.exists():
    df = pd.read_csv(path).drop("Unnamed: 0", axis=1)
    df = df.append(data, ignore_index=True)
else:
    df = pd.DataFrame(data=data, index=index, columns=columns)


# df.append(data, ignore_index=True)
# df[columns] = nworkers, total_wall, total_proc, overhead_end - overhead_start
df.to_csv(f'{dir_data}/dask_{nworkers}.csv')
