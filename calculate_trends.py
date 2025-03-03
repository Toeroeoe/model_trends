import numpy as np
import pymannkendall as pymk
from timeit import default_timer as timer

from blitzcomp.parallel import pixel_wise
import data_config
from argparse import ArgumentParser

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
                        nargs ='*', 
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

    pixel_wise(mannkendall,
               variables = args.variables,
               data = data_dict,
               variables_out = vars_out,
               units = units_out,
               file_out = args.outfile,
               return_shape = 0,
               return_dims = [],
               test = args.test)

    end = timer()

    print('\nParallel trend calculation done.\n')
    print(f'\nTime elapsed: {end - start} seconds.')




