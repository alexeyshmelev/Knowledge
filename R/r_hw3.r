mtcars

typeof(mtcars) # type of variable mtcars

typeof(mtcars[,2]) # type of 2nd column of variable mtcars

mtcars['Fiat 128',] # Fiat 128 has 4 cylinders

row.names(mtcars)[mtcars$cyl == mtcars['Fiat 128',]$cyl] # here are all cars with the same number of cylinders as Fiat 128

min(mtcars$cyl) # minimal number of cylinders is 4

row.names(mtcars)[mtcars$cyl == min(mtcars$cyl)] # here are all cars with the minimal number of cylinders

corr_mtcars = cor(mtcars) # calculate correlation between all categories
corr_mtcars

?mtcars

isSymmetric(corr_mtcars) # we get symmetrical matrix (obviously)

typeof(corr_mtcars) # type of matrix with correlation coefficients

rownames(corr_mtcars)[corr_mtcars[,'mpg'] < -0.7] # here are properties that mpg has correlation lower than -0.7 with

rand_norm = rnorm(100, mean=40, sd=10) # random vector with normal distribution (m=40, s=10)

hist(rand_norm)

every_third = rand_norm[c(F, F, T)] # subvector with every third value
excluding_fifth = rand_norm[c(T, T, T, T, F)] # subvector with every fifth value being excluded
whole_part_is_even = rand_norm[as.logical(sapply(rand_norm, as.integer) %% 2)] # subvector with values that have even whole part

tree = list(left=list(left='a', right=list('b', 'c')), right=list('d', 'e')) # tree structure
tree

(unlist(tree)) # names of all leaves with names of columns
unname(unlist(tree)) # pure names of all leaves (it will work only for the tree where only leaves are labeled; it's exactly the case of our task)

tree$left # left subtree

tree$left$right # node with 'b' and 'c'