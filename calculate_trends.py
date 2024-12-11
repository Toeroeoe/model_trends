import numpy as np
import pymannkendall as pymk
from timeit import default_timer as timer

from blitzcomp.parallel import pixel_wise
import data_config



## Settings
# The data that you specified in data_config.py
data = 'SXI_183D_EU3_8daily' 
variables = ['SXI_SM_r']
outfile = 'out.nc'
units = {'p': 'dimensionless',
         'slope': 'm^3 m^-3 8d^-1'}


if __name__ == '__main__':

    def mannkendall(arrays: dict[str, np.ndarray]):

        dict_out = {}

        for v, array in arrays.items():
        
            if np.isnan(array).any(): 
            
                dict_out[f'{v}_slope'] = np.nan
                dict_out[f'{v}_p'] = np.nan
        
                continue
            
            if array.ndim == 1:
            
                result = pymk.original_test(array)
    
            else: 
            
                NotImplementedError('Input array needs to be one-dimensional.')
    
            dict_out[f'{v}_slope'] = result.slope
            dict_out[f'{v}_p'] = result.p
    
        return dict_out

    start = timer()

    data_dict = getattr(data_config, data)

    vars_out = [f'{v}_slope' for v in variables] + \
               [f'{v}_p' for v in variables]
    
    units_out = {v: units[v.split('_')[-1]] for v in vars_out}

    pixel_wise(mannkendall,
               variables = variables,
               data = data_dict,
               variables_out = vars_out,
               units = units_out,
               file_out = outfile,)

    end = timer()

    print('\nParallel trend calculation done.\n')
    print(f'\nTime elapsed: {end - start} seconds.')




