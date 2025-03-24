#!/usr/bin/env Rscript
library(future.apply)
library(future)
library(rhdf5)

plan(multicore)

args = commandArgs(trailingOnly=TRUE)
indir <- args[1]
outdir <- args[2]

fast5s <- dir(indir, ".fast5$", full.names = TRUE)
names(fast5s) <- gsub(".+/", "", fast5s)

extract_5mer <- function(fast5, name) {
    events <- h5dump(fast5)$Analyses$RawGenomeCorrected_000$BaseCalled_template$Events
    events$start <- NULL
    T_pos  <- which(events$base == "T")
    if (length(T_pos) >= 1) {
        T_pos <- T_pos[T_pos > 2 & T_pos < nrow(events) -1]
    }
    
    if (length(T_pos) >= 1) {
        T_centered_5mer_features <- lapply(T_pos, function(.x){
            events[(.x -2):(.x+2), ]
        })
        
        T_centered_5mer_features <- do.call("rbind", T_centered_5mer_features)
        
        fname <- paste0(name, ".resquiggle.features.txt")
        write.table(T_centered_5mer_features, 
                    file=file.path(outdir, fname),
                    sep = "\t", quote = FALSE, row.names = FALSE)
    }
    
}

null <- future_mapply(extract_5mer, fast5s, names(fast5s), 
                      SIMPLIFY = FALSE,
                      future.chunk.size = 250)

