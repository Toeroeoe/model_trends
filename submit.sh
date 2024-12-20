#!/bin/bash -x
#SBATCH --job-name=trends
#SBATCH --account=jibg31
#SBATCH --ntasks=256
#SBATCH --mem=512000
#SBATCH --time=10:00

source /p/scratch/cjibg31/jibg3105/projects/venvs/crusty/activate.sh

srun -n 256 python calculate_trends.py
