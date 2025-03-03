#!/bin/bash -x
#SBATCH --job-name=trends
#SBATCH --account=jibg31
#SBATCH --ntasks=256
#SBATCH --mem=512000
#SBATCH --time=4:00:00

# Environment
source /p/scratch/cjibg31/jibg3105/projects/venvs/test_crusty/activate.sh

# Data
data=clm5_detect_control
outfile=CLM5_DETECT_production_control_trends.nc
variables=(
    NEE
    GPP
    TLAI
    TOTECOSYSC
    TOTSOMC
    TOTVEGC
    LEAFC
    QFLX_EVAP_TOT
    QFLX_EVAP_VEG
    ZWT
)

# https://pypi.org/project/pymannkendall/
test=seasonal_test

# run parallel
srun -n 256 \
    python calculate_trends.py \
        --data $data \
        --variables ${variables[@]} \
        --outfile $outfile
