#include <iostream>
#include <memory>
#include <cstdint>
#include <iomanip>
#include "array_types.hpp"
#include <cmath>
#include <functional>
#include <chrono>

using intptr_t = std::intptr_t;

template <class T> struct benchresult {
    T result;
    double btime;
};

template <class T, class input_type>
auto benchmark(std::function<T(input_type)> fn, input_type input, intptr_t nrepeat){
    T result;
    auto start = std::chrono::steady_clock::now();
    for (intptr_t i = 0; i < nrepeat; i++) {
        result = fn(input);
    }
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> duration_s = end - start;
    double ms_per_run = duration_s.count() * 1000 / nrepeat;
    return benchresult<T> {result, ms_per_run};
}

template <class T>
T force(vec<T> m, vec<T> x, vec<T> y, vec<T> z)
{    
    int n = m.length();
    double mforce = 0;
    double cforce = 0;

    for (intptr_t i = 0; i < n-1; i++) {
        for (intptr_t j = i+1; j < n; j++) {
            double den = (x(i) - x(j))*(x(i) - x(j)) + (y(i) - y(j))*(y(i) - y(j)) + (z(i) - z(j))*(z(i) - z(j));
            cforce = (m(i) * m(j)) / den;
            if (cforce > mforce) {
             mforce = cforce;
            }
        }
    }

    return mforce;
}

int main(int argc, char* argv[])
{
    intptr_t n;

    std::cin >> n;
    vec<double> m(n);
    vec<double> x(n);
    vec<double> y(n);
    vec<double> z(n);
    for (intptr_t k = 0; k < n; k++) {
        std::cin >> m(k);
    }
    for (intptr_t k = 0; k < n; k++) {
        std::cin >> x(k);
    }

    for (intptr_t k = 0; k < n; k++) {
        std::cin >> y(k);
    }
    for (intptr_t k = 0; k < n; k++) {
        std::cin >> z(k);
    }
    std::function<double(int)> max_force = [=](int idx) {return force(m,x,y,z);};

    auto benchresult = benchmark(max_force, 0, 1000);

    std::cout << std::setprecision(std::numeric_limits<double>::digits10 + 1)
              << "Timing: " << benchresult.btime << " ms\n"
              << "Answer = " << benchresult.result << "\n"
              << "Giga flops: " << (((n * (n-1) / 2) * 10) / (benchresult.btime / 1e+3)) / 1e+9 // where n * (n-1) / 2 is number of combinations C_n^2
              << std::endl;
        
    return 0;
}
