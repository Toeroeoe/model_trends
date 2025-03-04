
from simple_slurm import Slurm


# slurm settings
slurm = Slurm(job_name = 'trends',
              account = 'jibg31',
              ntasks = 256,
              mem = 512000,
              time = '5:00:00')

# Data settings
data = 'CLM5_detect_SP'
outfile = 'out/data/CLM5_detect_SP_TWS_trends.nc'
variables = ['TWS']

# function settings
func_name = 'anom_trends'
test = 'seasonal_test'

func_args = {'baseline_y0': 2003,
             'baseline_y1': 2016,
             'test': 'seasonal_test',
             'time_res': 'D'}


if __name__ == '__main__':

    slurm.sbatch("python calculate_trends.py " +\
                    f"--data {data} " +\
                    f"--variables {[f'{v} ' for v in variables]} " +\
                    f"--outfile {outfile} " +\
                    f"--func_name {func_name} " +\
                    f"""--func_args "{func_args}" """)


