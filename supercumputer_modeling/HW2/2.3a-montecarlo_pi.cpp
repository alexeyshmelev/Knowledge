#include <iomanip>
#include <iostream>
#include <cmath>
#include <cstddef>
#include <random>

#include <omp.h>

#include "vectors_and_matrices/array_types.hpp"

using std::cin;
using std::cout;
using ptrdiff_t = std::ptrdiff_t;
using size_t = std::size_t;

const double PI = 3.141592653589793;

double mc_pi(ptrdiff_t niter, size_t seed)
{
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    ptrdiff_t pi_est = 0;
    double x, y;

#pragma omp parallel private(rng, dist, x, y)
    {
        #pragma omp for reduction(+: pi_est)
        for (ptrdiff_t i = 0; i < niter; ++i)
        {
            x = dist(rng);
            y = dist(rng);
            pi_est += (x * x + y * y <= 1) ;
        }
    }
    return (double) 4.0 * (double) pi_est / (double) niter;
 }

int main(int argc, char** argv)
{
    ptrdiff_t niter;

    cin >> niter;

    double t1 = omp_get_wtime();

    double pi_est = mc_pi(niter, 4321);

    double t2 = omp_get_wtime();
    
    cout << "Computed average: " << std::setprecision(16) << pi_est << std::endl;
    cout << "Exact average: " << std::setprecision(16) << PI << std::endl;
    cout << "Time: " << t2 - t1 << std::endl;

    return 0;
}