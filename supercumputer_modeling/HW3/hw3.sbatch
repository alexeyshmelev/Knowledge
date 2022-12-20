#!/bin/bash
#SBATCH --job-name=hw3
#SBATCH --error=hw3_errors.txt
#SBATCH --output=hw3_results.txt
#SBATCH --time=00:10:00
#SBATCH --ntasks-per-node=16
#SBATCH -N 1
#SBATCH --no-requeue
#SBATCH -A proj_1339

mpicxx -O3 eigenvector_vector.cpp
echo 1000 | srun --mpi=pmix a.out