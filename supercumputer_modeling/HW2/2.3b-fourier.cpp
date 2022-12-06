#include <iostream>
#include <memory>
#include <cstdint>
#include <iomanip>
#include <random>
#include "vectors_and_matrices/array_types.hpp"

#include <omp.h>

using ptrdiff_t = std::ptrdiff_t;
using size_t = std::size_t;
const double PI = 3.141592653589793;

template <class T>
void fill_random(vec<T> x, T xmin, T xmax, size_t seed)
{
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<T> dist(xmin, xmax);
    for (ptrdiff_t i = 0; i < x.length(); i++)
    {
        x(i) = dist(rng);
    }
}

template <class T>
void fill_random_cos(vec<T> x, T ampl_max, size_t seed)
{
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<T> dist(-ampl_max, ampl_max);

    ptrdiff_t n = x.length();
    for (int imode=1; imode<=5; imode++)
    {
        T ampl = dist(rng);
        for (ptrdiff_t i = 0; i < n; i++)
        {
            x(i) += ampl * cos(imode * (2 * PI * i) / n);
        }
    }
}

void cosine_dft(vec<double> f, vec<double> x){
	ptrdiff_t i, k, nf = f.length(), nx = x.length();
	double omega = 0;
	for (k=0; k < nf; k++){
		f(k) = 0;
	}

	#pragma omp parallel private(omega)
	
	for (i=0; i < nx; i++){
		#pragma omp for nowait
		for (k = 0; k < nf; k++){
			omega = 2 * PI * k / nx;
			f(k) += x(i) * cos(omega * i);
		}
	}

}

int main(int argc, char* argv[])
{
    ptrdiff_t n;

    std::cin >> n;
    vec<double> x(n);
    vec<double> f(n);

    fill_random_cos(x, 100.0, 9876);

    double t0 = omp_get_wtime();

    cosine_dft(f, x);

    double t1 = omp_get_wtime();

    // f[1] - f[5] must be non-zero, the rest must be zero
    std::cout << std::setprecision(std::numeric_limits<double>::digits10 + 1)
              << "Timing: " << t1 - t0 << " sec\n";
    for (ptrdiff_t i=0; i<=10; i++){
        std::cout << "f[" << i << "] = " << f(i) << '\n';
    } 
    return 0;
}
