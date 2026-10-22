#!/usr/bin/env Rscript
# Interface interativa opcional do bibliometrix. Na aba de importação, selecione
# data/bibliometria/bibliometrix_records.csv, gerado por scripts/bibliometria.R.
suppressPackageStartupMessages(library(bibliometrix))
biblioshiny()
