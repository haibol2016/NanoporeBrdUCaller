#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
library(rhdf5)
indir <- args[1]
outdir <- args[2]

fast5 <- dir(indir, "*.fast5", 
	                    recursive = TRUE,
			                 full.names = TRUE)

null <- lapply(fast5, function(.x)
	       {
		   base <- basename(.x)
		   if (!"Fastq" %in%  h5ls(.x)$name){
		        file.rename(from = .x, to = file.path(outdir, base))
	           }
	       })

