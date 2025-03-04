#!/bin/bash -x
#SBATCH --job-name=trends
#SBATCH --account=jibg31
#SBATCH --ntasks=256
#SBATCH --mem=512000
#SBATCH --time=4:00:00

# Environment
source /p/scratch/cjibg31/jibg3105/projects/venvs/test_crusty/activate.sh

# Data
data=CLM5_detect_SP
outfile=out/data/CLM5_detect_SP_TWS_trends.nc
variables=(
    TWS
)

# https://pypi.org/project/pymannkendall/
test=seasonal_test

# run parallel
srun -n 256 \
    python calculate_trends.py \
        --data $data \
        --variables ${variables[@]} \
        --outfile $outfile
