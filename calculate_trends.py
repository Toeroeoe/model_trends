import numpy as np
import pandas as pd
import xarray as xr
import pymannkendall as pymk
from timeit import default_timer as timer

from blitzcomp.parallel import pixel_wise
import data_config
from argparse import ArgumentParser
from datarie.time import index

def anom_trends(arrays: dict[str, np.ndarray],
                baseline_y0: int,
                baseline_y1: int,
                time_index: pd.Series,
                test: str = 'original_test'):
     
        anomalies = baseline_anomalies(arrays = arrays,
                                       baseline_y0 = baseline_y0,
                                       baseline_y1 = baseline_y1,
                                       time_index = time_index)
        
        trends = mannkendall(anomalies,
                             test)
        
        return trends
     



def baseline_anomalies(arrays: dict[str, np.ndarray],
                       baseline_y0: int,
                       baseline_y1: int,
                       time_index: pd.Series):
    
    xarr = xr.Dataset(data_vars = {k: (['time'], v)
                                   for k, v in arrays.items()},
                      coords = {'time': time_index}).convert_calendar('noleap')
    
    xarr.coords['dayofyear'] = xarr['time'].dt.dayofyear

    base_mean = xarr.sel(time=slice(f'{baseline_y0}-01-01', 
                                    f'{baseline_y1}-12-31'))\
                                    .groupby(dayofyear = xr.groupers.UniqueGrouper())\
                                    .mean()
    
    xarr_anom = xarr.groupby(dayofyear = xr.groupers.UniqueGrouper()) - base_mean

    return {k: v.to_numpy() for k, v in xarr_anom.items()}




def mannkendall(arrays: dict[str, np.ndarray],
                test: str = 'original_test'):

        dict_out = {}

        for v, array in arrays.items():
        
            if np.isnan(array).any(): 
            
                dict_out[f'{v}_slope'] = np.nan
                dict_out[f'{v}_p'] = np.nan
        
                continue
            
            if array.ndim == 1:

                func = getattr(pymk, test)
            
                result = func(array)
    
            else: 
            
                NotImplementedError('Input array needs to be one-dimensional.')
    
            dict_out[f'{v}_slope'] = result.slope
            dict_out[f'{v}_p'] = result.p
    
        return dict_out


if __name__ == '__main__':
    
    parser = ArgumentParser()
    
    parser.add_argument('--data', 
                        '-d', 
                        help = 'name of data dictionary', 
                        type = str)

    parser.add_argument('--variables', 
                        '-v', 
                        help = 'list of variable names',
                        nargs = '*', 
                        type = str)
    
    parser.add_argument('--outfile', 
                        '-o', 
                        help = 'path of the output file', 
                        type = str)
    
    parser.add_argument('--test',
                        '-t',
                        help = 'mann kendall test type',
                        type = str,
                        default = 'original_test')
    
    args = parser.parse_args()
    
    units = {'p': 'dimensionless',
             'slope': 'm^3 m^-3 8d^-1'}

    start = timer()

    data_dict = getattr(data_config, args.data)

    vars_out = [f'{v}_slope' for v in args.variables] + \
               [f'{v}_p' for v in args.variables]
    
    units_out = {v: units[v.split('_')[-1]] 
                 for v in vars_out}
    
    time = index(2000,
                 2022,
                 'D',
                 leapday = False)

    pixel_wise(anom_trends,
               variables = args.variables,
               data = data_dict,
               variables_out = vars_out,
               units = units_out,
               file_out = args.outfile,
               return_shape = 0,
               return_dims = [],
               baseline_y0 = 2003,
               baseline_y1 = 2016,
               time_index = time,
               test = args.test)

    end = timer()

    print('\nParallel trend calculation done.\n')
    print(f'\nTime elapsed: {end - start} seconds.')




