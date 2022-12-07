#!/bin/bash
#SBATCH --job-name=hw2
#SBATCH --constraint="[type_a|type_b]"
#SBATCH --error=hw2_errors.txt
#SBATCH --output=hw2_results.txt
#SBATCH --time=00:10:00
#SBATCH -N  1
#SBATCH -n 1
#SBATCH  -c 4 
export OMP_NUM_THREADS=4; 
srun  ./a.out 
