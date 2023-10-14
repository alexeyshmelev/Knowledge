install.packages('comprehenr') # run it if you don't have this package installed (for list comprehension in R)

library(comprehenr)

# task 1
num_dots = 100

x = runif(num_dots**2, -1, 1)
y = runif(num_dots**2, -1, 1)

is_inside = as.integer(sqrt(x**2 + y**2) <= 1) + 1

plot(x, y, col=c('blue', 'red')[is_inside], main='Visualization of selected dots')

prob = length(is_inside[is_inside==2]) / length(is_inside) # the probability equals ~ 0.7866 (slightly depends on the seed)

# task 2
pi_approx = (2 * 2) * prob # here is approxamation of pi

# task 3
array_of_squares = c()
for (i in 1:8) {
    x = runif(10**i, -1, 1)
    y = runif(10**i, -1, 1)
    is_inside = as.integer(sqrt(x**2 + y**2) <= 1) + 1
    array_of_squares = append(array_of_squares, 4 * length(is_inside[is_inside==2]) / length(is_inside))
}

plot(log10(to_vec(for(i in 1:8) 10**i)), array_of_squares, xlab='number of throws (log10 scale)', ylab='approximation of pi', type="b", col='red', main='Dependance of approximation of pi on number of throws')
abline(h=pi, col="blue")
legend('topright', legend=c("Approximation", "Ground truth"), col=c("red", "blue"), lty=c(1, 1))

# difference
plot(log10(to_vec(for(i in 1:8) 10**i)), abs(pi - array_of_squares), xlab='number of throws (log10 scale)', ylab='absolute difference', type="b", col='red', main='Dependance of difference between approximation of pi and \n real value on number of throws')

