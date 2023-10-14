install.packages('simpleboot')

exp_data = read.table('hw1.txt')

param1 = lm(unlist(exp_data[2]) ~ unlist(exp_data[1]))
param2 = lm(unlist(exp_data[3]) ~ unlist(exp_data[1]))
param3 = lm(unlist(exp_data[3]) ~ unlist(exp_data[2]))

par(mfrow=c(1,3))

plot(exp_data[,1], exp_data[,2], xlab='CPY14', ylab='RMD4')
abline(param1, col='red', lwd=3)

plot(exp_data[,1], exp_data[,3], xlab='CPY14', ylab='htVWQ')
abline(param2, col='red', lwd=3)

plot(exp_data[,2], exp_data[,3], xlab='RMD4', ylab='htVWQ')
abline(param3, col='red', lwd=3)

hist(exp_data$CPY14)

hist(exp_data$htVWQ)

hist(exp_data$RMD4)

print(cor.test(exp_data[,2], exp_data[,1], method = "pearson"))
print(cor.test(exp_data[,3], exp_data[,1], method = "pearson"))
print(cor.test(exp_data[,3], exp_data[,2], method = "pearson"))
# значимая зависимость только в паре генов CPY14-RMD4 (т.к. p-value меньше 0.05), в остальных парах значимой зависимости нет

print(t.test(exp_data[,2], exp_data[,1]), var.equal = TRUE)
print(t.test(exp_data[,3], exp_data[,1]), var.equal = TRUE)
print(t.test(exp_data[,3], exp_data[,2]), var.equal = TRUE)
# с одной стороны, если сдеать t-test, то получается, что есть значимого отличия среднего только в паре генов htVWQ - CPY14, т.к. там p-value больше 0.05

library(simpleboot)
library(ggplot2)

bootstrapped <- two.boot(exp_data$RMD4, exp_data$CPY14, mean, 10000)

bootstrapped_mean_diff <- data.frame(bootstrapped$t)
colnames(bootstrapped_mean_diff) <- 'mean_diffs'

ggplot(bootstrapped_mean_diff, aes(x=mean_diffs)) +
  geom_histogram(bins=20, alpha=0.8) +
  geom_vline(xintercept = bootstrapped$t0, size = 1.5) +
  geom_vline(xintercept = quantile(bootstrapped_mean_diff$mean_diffs, 0.05), size = 1, linetype = 'dashed') +
  geom_vline(xintercept = quantile(bootstrapped_mean_diff$mean_diffs, 0.95), size = 1, linetype = 'dashed') +
  xlab('sample mean') + ylab('bootstrapped count')

bootstrapped <- two.boot(exp_data$htVWQ, exp_data$CPY14, mean, 10000)

bootstrapped_mean_diff <- data.frame(bootstrapped$t)
colnames(bootstrapped_mean_diff) <- 'mean_diffs'

ggplot(bootstrapped_mean_diff, aes(x=mean_diffs)) +
  geom_histogram(bins=20, alpha=0.8) +
  geom_vline(xintercept = bootstrapped$t0, size = 1.5) +
  geom_vline(xintercept = quantile(bootstrapped_mean_diff$mean_diffs, 0.05), size = 1, linetype = 'dashed') +
  geom_vline(xintercept = quantile(bootstrapped_mean_diff$mean_diffs, 0.95), size = 1, linetype = 'dashed') +
  xlab('sample mean') + ylab('bootstrapped count')

bootstrapped <- two.boot(exp_data$htVWQ, exp_data$RMD4, mean, 10000)

bootstrapped_mean_diff <- data.frame(bootstrapped$t)
colnames(bootstrapped_mean_diff) <- 'mean_diffs'

ggplot(bootstrapped_mean_diff, aes(x=mean_diffs)) +
  geom_histogram(bins=20, alpha=0.8) +
  geom_vline(xintercept = bootstrapped$t0, size = 1.5) +
  geom_vline(xintercept = quantile(bootstrapped_mean_diff$mean_diffs, 0.05), size = 1, linetype = 'dashed') +
  geom_vline(xintercept = quantile(bootstrapped_mean_diff$mean_diffs, 0.95), size = 1, linetype = 'dashed') +
  xlab('sample mean') + ylab('bootstrapped count')

# с другой стороны, если сдеалать bootstrap анализ, то получается, что среднее отличие средних в экспрессиях всех пар генов всегда далеко от 0.
# Исходя из данных t-test, bootstrap анализа и scatter plot для пар генов, я считаю, что значимого отличия среднего НЕТ только у пары генов (CPY14-RMD4, там и корреляция хорошая получается к тому же, см. первое задание).