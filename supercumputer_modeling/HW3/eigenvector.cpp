#include <iostream>
#include <memory>
#include <cstdint>
#include <iomanip>
#include <random>
#include <math.h>
#include "vectors_and_matrices/array_types.hpp"
#include "mpi.h"


using ptrdiff_t = std::ptrdiff_t;
using size_t = std::size_t;

void fill_random(vec<double> x, double xmin, double xmax, size_t seed)
{
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> dist(xmin, xmax);
    for (ptrdiff_t i = 0; i < x.length(); i++)
    {
        x(i) = dist(rng);
    }
}

void fill_random(matrix<double> x, double dispersion, size_t seed)
{
    std::mt19937_64 rng(seed);
    std::normal_distribution<double> dist(0, dispersion);
    for (ptrdiff_t i = 0; i < x.length(); i++)
    {
        x(i) = dist(rng);
    }
}

void symmetrize(matrix<double> a)
{
    ptrdiff_t n = a.nrows();
    for (ptrdiff_t i = 0; i < n; i++)
    {
        for (ptrdiff_t j = 0; j < i; j++)
        {
            double sym_elt = (a(i, j) + a(j, i)) / 2;
            a(i, j) = sym_elt;
            a(j, i) = sym_elt;
        }
    }
}

double eigenvalue(matrix<double> A, MPI_Comm comm, int* sendcounts, int* displs)
{
    int n = A.ncols(), m = A.nrows();
    vec<double> v0(n);
    vec<double> v1(n);

    int myrank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank); //номер процесса
    MPI_Comm_size(MPI_COMM_WORLD, &world_size); //количество процессов

    // generate a random vector on rank 0 and broadcast it
    if (myrank == 0)
    {
        fill_random(v0, -10.0, 10.0, 24680);
    }

    MPI_Bcast(v0.raw_ptr(), n, MPI_DOUBLE, 0, comm);

    ptrdiff_t iter;
    ptrdiff_t i, j;

    ptrdiff_t ilocal_start = displs[myrank] / n;

    double rq, diff = 1.0;
    int niter = 0;


    while (std::abs(diff) > 1e-15)
    {
        // normalize v0
        double norm2 = 0;
        for (i=0; i < n; i++)
        {
            norm2 += v0(i) * v0(i);
        }

        for (i=0; i < n; i++)
        {
            v0(i) /= sqrt(norm2);
        }

        // v1 = A * v0
        for (i=0; i<m; i++)
        {
            v1(ilocal_start+i) = 0;
            for (j=0; j<n; j++)
            {
                v1(ilocal_start+i) += v0(j) * A(i, j);
            }
        }

        int recvcounts_new[world_size], displs_new[world_size];

        for (int i = 0; i < world_size; i++){
            recvcounts_new[i] = sendcounts[i] / n;
            displs_new[i] = displs[i] / n;
        }

        MPI_Allgatherv(v1.raw_ptr() + ilocal_start, m, MPI_DOUBLE, v1.raw_ptr(), recvcounts_new, displs_new, MPI_DOUBLE, comm);

        // Rayleigh quotient = (x' A x) / (x' x) = dot(v0, v1)
        rq = 0;
        for (j=0; j<n; j++)
        {
            rq += v1(j) * v0(j);
        }
        diff = 0;
        for (j=0; j<n; j++)
        {
            double d = v1(j) / rq - v0(j);
            if (std::abs(d) > diff)
            {
                diff = d;
            }
        }
        // swap v1 and v0
        vec<double> tmp = v0;
        v0 = v1;
        v1 = tmp;
        niter += 1;
    }

    return rq;
}

// read an integer number from stdin into `n`
void read_integer(int* n, int rank, MPI_Comm comm)
{
    if (rank==0)
    {
        std::cin >> *n;
    }

    MPI_Bcast(n, 1, MPI_INT, 0, comm);//передали значение переменной n на все остальные процессы, 1 т.к. это просто число
}

// scatter matrix `source` over processes in communicator `comm` from `root`
void scatter_matrix(matrix<double> source, matrix<double> dest, int root, MPI_Comm comm, int* sendcounts, int* displs)
{

    int myrank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank); //номер процесса
    MPI_Comm_size(MPI_COMM_WORLD, &world_size); //количество процессов

    int n = dest.ncols(), m_each = dest.nrows();

    double *src_ptr = source.raw_ptr(), *dest_ptr = dest.raw_ptr();
    MPI_Scatterv(src_ptr, sendcounts, displs, MPI_DOUBLE, dest_ptr, m_each * n, MPI_DOUBLE, root, comm);
}

int main(int argc, char* argv[])
{
    int n;

    int myrank, world_size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank); //номер процесса
    MPI_Comm_size(MPI_COMM_WORLD, &world_size); //количество процессов

    read_integer(&n, myrank, MPI_COMM_WORLD);

    int whole_part = n / world_size;
    int remainder = n % world_size;

    int sendcounts[world_size], displs[world_size];

    for (int i = 0; i < world_size; i++) sendcounts[i] = whole_part;
    int i = 0;
    while (remainder != 0){
        sendcounts[i]++;
        remainder--;
        i++;
    }
    for (int i = 0; i < world_size; i++) sendcounts[i] *= n;
    for (int i = 0; i < world_size; i++){
        if (i == 0) displs[i] = 0;
        else displs[i] = displs[i-1] + sendcounts[i-1];
    }

    
    matrix<double> A(1, 1);

    // assuming n is multiple of world_size
    if ((n % world_size) == 0) A = matrix<double>(n / world_size, n);
    else A = matrix<double>(sendcounts[myrank] / n, n);

    // generate matrix on rank 0 (for simplicity)
    if (myrank == 0)
    {
        matrix<double> A_all(n, n);
        fill_random(A_all, 1.0, 9876);
        symmetrize(A_all);

        scatter_matrix(A_all, A, 0, MPI_COMM_WORLD, sendcounts, displs);

    }
    else
    {
        scatter_matrix(A, A, 0, MPI_COMM_WORLD, sendcounts, displs);
    }

    double t0 = MPI_Wtime();

    double q = eigenvalue(A, MPI_COMM_WORLD, sendcounts, displs);

    double t1 = MPI_Wtime();

    if (myrank == 0)
    {
        std::cout << std::setprecision(std::numeric_limits<double>::digits10 + 1)
                << "Timing: " << t1 - t0 << " sec\n"
                << "Answer = " << q
                << std::endl;
    }

    MPI_Finalize();
    return 0;
}
