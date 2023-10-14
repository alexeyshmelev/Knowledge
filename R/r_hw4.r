install.packages("ape")

library(ape)

dna = read.dna('sequence.fasta', 'fasta', as.character = T)
rownames(dna)<-NULL

dna_plain = toupper(apply(dna, 1, paste, collapse = ""))

system.time({

# constructing all possible 6-mers (data.frame)
bases=c('A','T','G','C')
kmeres = expand.grid(bases, bases, bases, bases, bases, bases)
kmeres[] = lapply(kmeres, as.character)
kmeres_str = c()

# creating vector with all 6-mers as strings
for (i in 1:nrow(kmeres)){
    kmeres_str = append(kmeres_str, do.call(paste0, args=c(kmeres[i,], sep='')))
}

# making dumb array where all 6-mers from genome will be stored (pre-allocating memory)
all_kmeres = rep(c('N'), nchar(dna_plain) - 6 + 1)

# filling all_kmers vector with real 6-mers from genome
for (i in 1:(nchar(dna_plain) - 6 + 1)){
    km = substr(dna_plain, i, i+5)
    all_kmeres[i] = km
}

# counting unique 6-mers
all_kmeres_table = table(all_kmeres)

# sorting number of entries for each 6-mer and printing results
all_kmeres_table_sorted = all_kmeres_table[order(all_kmeres_table)]
cat('Two rarest kmeres are', names(all_kmeres_table_sorted)[1], paste0('(', all_kmeres_table_sorted[1]), 'entries)', 'and', names(all_kmeres_table_sorted)[2], paste0('(', all_kmeres_table_sorted[2]), 'entries)\n')
cat('Two most frequent kmeres are', names(all_kmeres_table_sorted)[4095], paste0('(', all_kmeres_table_sorted[4095]), 'entries)', 'and', names(all_kmeres_table_sorted)[4096], paste0('(', all_kmeres_table_sorted[4096]), 'entries)')
})

