nMaxVecElement = function(vec, n){
    if (class(vec)[1] == 'numeric'){
        if (length(vec) != 0) res = unique(sort(vec, decreasing = T))
        else {
            print('length equals 0')
            return(NULL)
        }
        if (length(res) >= n) return(res[n])
        else {
            print('n-th element does not exist, returning NULL')
            return(NULL)
        }
    }
    else {
        print('It is not a vector, or elements inside are not numbers, returning NULL')
        return(NULL)
    }
}

# checking
nMaxVecElement(c(1.564, 5, 5.456, 6, 4.4564, 3, NA , 4, 57, 88, 9, 9, 9, 9), 1)

nMaxVecElement(mtcars, 4)

nMaxVecElement(matrix(rep(seq(1, 2, length.out=2), each=2), ncol=2), 2)

nMaxVecElement(list('a', 'b', 'c'), 10)

nMaxVecElement(c('a', 'b', 'c'), 10)

nMaxVecElement(list(), 10)

nMaxVecElement(c(), 10)

nMaxVecElement(c(1, 2), 10)

mandelbrotPlot = function(x_left_border, x_right_border, y_left_border, y_right_border, N, num_it){

    if (x_left_border == x_right_border |
      y_left_border == y_right_border |
      N <= 1 |
      num_it <= 0){
        # it will work with num_it <= 0 but I don't want negative iterations because num_it = -2 equals 1:-2 and equals c(1, 0, -1, -2) and has length 4 but not 2 (like abs(-2))
        print('Wrong conditions')
        return(NULL)
      }

    else {

        x0 = matrix(rep(seq(x_left_border, x_right_border, length.out=N), each=N), ncol=N)
        y0 = matrix(rep(seq(y_left_border, y_right_border, length.out=N), times=N), ncol=N)

        x = x0
        y = y0

        for (i in 1:num_it) {
            x_old = x
            x = x^2 - y^2 + x0
            y = 2 * x_old * y + y0
        }

        z = t(abs(x^2 + y^2))
        z[!is.na(z)] = rank(z[!is.na(z)])
        if (all(is.na(z^3))) print('Empty picture, select another conditions')
        else {
            image(z^3, col=rev(terrain.colors(1000)), xlab='real', ylab='imaginary')
            title(main = "Mandelbrot plot", font.main = 4)
        }

    }

}

# checking
mandelbrotPlot(-2, 2, -2, 2, 1000, 20)

mandelbrotPlot(-2, 2, -2, 2, 100, 20)

mandelbrotPlot(-2, 2, -2, 2, 1, 20)

mandelbrotPlot(-2, 2, -2, 2, 1000, -20)

mandelbrotPlot(-2, -2, -2, -2, 1000, 20)

mandelbrotPlot(-2, -2, -2, -2, -1000, -20)

mandelbrotPlot(-2, -1, -2, -1, 1000, 20)

