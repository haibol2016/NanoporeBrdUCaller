#!/usr/bin/env Rscript
library(rhdf5)
library("future.apply")

plan(multicore)

args = commandArgs(trailingOnly=TRUE)

fast5_f <- dir(args[1], full.names = TRUE)

fnames <- gsub(".+/(.+).fast5", "\\1", fast5_f)

acceptor <- "CACAAGAACAGTAAGGA"
terminator <- "TGTATG"

extract_5mer <-  future_mapply(function(f, name){
    resquiggle <- h5dump(f)$Analyses$RawGenomeCorrected_000$BaseCalled_template$Events
    sequence <- paste(resquiggle$base, collapse = "")
    acceptor_pos <- regexpr(paste0(acceptor,".{5}", terminator), sequence)
    if (acceptor_pos != -1)
    {
        match_start <- acceptor_pos + nchar(acceptor)
        five_mer <- resquiggle[match_start:(match_start + 4), c(1,2,4,5)]
        five_mer$readID <- name
        five_mer
    }
}, fast5_f, fnames, SIMPLIFY = FALSE, future.chunk.size = 100)
extract_5mer <- do.call("rbind", extract_5mer)
rownames(extract_5mer) <- NULL

write.table(extract_5mer, file = file.path(args[2], 
					   paste0(gsub(".+?/(batch\\d+)", "\\1", args[1]), ".5mer.info.txt")), 
	    sep = "\t", quote = FALSE, row.names = FALSE)
