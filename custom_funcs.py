import numpy as np
import pandas as pd
import xarray as xr
import pymannkendall as pymk

from datarie.time import index

def anom_trends(arrays: dict[str, np.ndarray],
                baseline_y0: int,
                baseline_y1: int,
                time_res: str,
                test: str = 'original_test'):
        
        time_index = index(y0 = baseline_y0,
                           y1 = baseline_y1,
                           t_res = time_res)
     
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

    return {str(k): v.to_numpy() 
            for k, v in xarr_anom.items()}


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
