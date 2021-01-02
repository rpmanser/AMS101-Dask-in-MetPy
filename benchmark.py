# =============================================================================
# benchmark.py
#
# Functions for benchmarking metpy functions with dask and numpy arrays
# as arguments.
#
# Author: Russell Manser
# Created: 12/15/2020
# =============================================================================

import time
from pathlib import Path

import xarray as xr

import metpy.calc as mpcalc
from metpy.units import units


def dewpoint_from_relative_humidity(temperature, relative_humidity):
    """Similar to `metpy.calc.dewpoint_from_relative_humidity`, but without
    a check for values greater than 120%"""
    return mpcalc.dewpoint(
        relative_humidity * mpcalc.saturation_vapor_pressure(temperature)
    )


def test(type):
    """Run a single benchmark test for computation of meteorological fields
    across a forecast ensemble.

    Parameters
    ----------
    type : str
        The type of array to test; either 'numpy' or 'dask'.

    Returns
    -------
    tuple of floats
        The total wall and process times.
    """
    refpath = Path("/lustre/scratch/rmanser/wrfref/wrfoutREFd02")
    mempath = Path("/lustre/scratch/rmanser/test_ens/2016052812/")

    ref = xr.open_dataset(refpath)
    # All members are loaded implicitly as dask arrays, regardless of `type`
    members = xr.open_mfdataset(
        mempath.glob("mem*/wrfout_d02_2016-05-30_12:00:00"),
        concat_dim='members',
        combine='nested',
    )

    # For dask arrays, we select the individual variable dask arrays
    if type == 'dask':
        pressure = (members.P + ref.PB).data * units(ref.PB.units)
        theta = (members.T + ref.T00).data * units(ref.T00.units)
        mixing_ratio = members.QVAPOR.data * units('dimensionless')

    # For numpy arrays, we force variable arrays to be loaded into memory
    elif type == 'numpy':
        pressure = (members.P + ref.PB).values * units(ref.PB.units)
        theta = (members.T + ref.T00).values * units(ref.T00.units)
        mixing_ratio = members.QVAPOR.values * units('dimensionless')

    start_wall = time.time()
    start_proc = time.process_time()

    temperature = mpcalc.temperature_from_potential_temperature(pressure, theta)
    
    relative_humidity = mpcalc.relative_humidity_from_mixing_ratio(
        mixing_ratio,
        temperature,
        pressure
    )

    # We don't call metpy's function here because it implicitly triggers
    # a dask.compute() call
    dewpoint = dewpoint_from_relative_humidity(temperature, relative_humidity)

    if type == 'dask':
        td = dewpoint.compute()

    end_wall = time.time()
    end_proc = time.process_time()

    total_wall = end_wall - start_wall
    total_proc = end_proc - start_proc

    return total_wall, total_proc
