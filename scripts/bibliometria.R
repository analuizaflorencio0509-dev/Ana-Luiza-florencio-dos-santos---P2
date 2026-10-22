#!/usr/bin/env Rscript
# Coleta metadados OpenAlex e realiza análise com bibliometrix.
# Uso: Rscript scripts/bibliometria.R [--refresh]

suppressPackageStartupMessages(library(openalexR))
suppressPackageStartupMessages(library(bibliometrix))

args_all <- commandArgs(trailingOnly = FALSE)
script_arg <- grep("^--file=", args_all, value = TRUE)[1]
script_path <- sub("^--file=", "", script_arg)
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
bib_dir <- file.path(root, "data", "bibliometria")
fig_dir <- file.path(root, "figuras")
dir.create(bib_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)

refresh <- "--refresh" %in% commandArgs(trailingOnly = TRUE)
refs_path <- file.path(bib_dir, "referencias_candidatas.csv")
selection_path <- file.path(bib_dir, "dois_selecionados.txt")
cache_path <- file.path(bib_dir, "openalex_records.rds")
if (!file.exists(refs_path)) stop("Arquivo ausente: ", refs_path, ". Execute scripts/consolida_referencias.py.")
refs <- read.csv(refs_path, fileEncoding = "UTF-8-BOM", stringsAsFactors = FALSE, check.names = FALSE)
norm_doi <- function(x) tolower(sub("^https?://(dx\\.)?doi\\.org/", "", trimws(x), ignore.case = TRUE))
if (file.exists(selection_path)) {
  selected <- norm_doi(readLines(selection_path, warn = FALSE, encoding = "UTF-8"))
  selected <- selected[nzchar(selected) & !startsWith(selected, "#")]
  if (anyDuplicated(selected)) stop("A lista de DOI selecionados contém duplicatas.")
  selected_index <- match(selected, norm_doi(refs$doi))
  if (anyNA(selected_index)) stop("Há DOI selecionado ausente da lista consolidada.")
  refs <- refs[selected_index, , drop = FALSE]
  refs$doi <- selected
}
if (length(unique(norm_doi(refs$doi))) < 80) stop("O corpus bibliométrico precisa conter pelo menos 80 DOI selecionados.")
if (!refresh && file.exists(cache_path)) {
  cached <- readRDS(cache_path)
  refresh <- !setequal(norm_doi(refs$doi), norm_doi(cached$doi))
  if (refresh) message("A lista de DOI mudou; o cache OpenAlex será atualizado.")
  else works <- cached
}

if (refresh || !file.exists(cache_path)) {
  dois <- unique(norm_doi(refs$doi))
  dois <- dois[!is.na(dois) & nzchar(dois)]
  if (length(dois) == 0) stop("A lista de DOI está vazia.")
  message("Consultando OpenAlex para ", length(dois), " DOI(s)...")
  works <- oa_fetch(
    entity = "works",
    doi = dois,
    output = "tibble",
    abstract = TRUE,
    timeout = 60,
    verbose = FALSE
  )
  expected_journal <- setNames(tolower(trimws(refs$journal)), norm_doi(refs$doi))
  work_doi <- norm_doi(works$doi)
  source_match <- tolower(trimws(works$source_display_name)) == unname(expected_journal[work_doi])
  source_match[is.na(source_match)] <- FALSE
  ordering <- order(work_doi, -as.integer(source_match))
  works <- works[ordering, , drop = FALSE]
  work_doi <- work_doi[ordering]
  works <- works[!duplicated(work_doi), , drop = FALSE]
  saveRDS(works, cache_path)
  writeLines(paste("Coleta OpenAlex UTC:", format(Sys.time(), tz = "UTC", usetz = TRUE)),
             file.path(bib_dir, "openalex_retrieval.txt"), useBytes = TRUE)
}

if (nrow(works) == 0) stop("OpenAlex não retornou registros.")
message("Registros retornados: ", nrow(works))

# Monta os campos documentados pelo bibliometrix com autoria validada na seleção manual.
# OpenAlex fornece palavras-chave/conceitos; afiliações são omitidas por cobertura irregular.
refs_doi <- norm_doi(refs$doi)
work_doi <- norm_doi(works$doi)
work_index <- match(refs_doi, work_doi)
has_openalex <- !is.na(work_index)
keyword_text <- function(x, threshold = 0.25) {
  if (is.null(x) || nrow(x) == 0 || !all(c("display_name", "score") %in% names(x))) return("")
  paste(x$display_name[is.na(x$score) | x$score >= threshold], collapse = ";")
}
abstracts <- rep("", length(refs_doi))
keyword_values <- rep("", length(refs_doi))
concept_values <- rep("", length(refs_doi))
citation_counts <- rep(NA_real_, length(refs_doi))
if (any(has_openalex)) {
  matched <- work_index[has_openalex]
  if ("abstract" %in% names(works)) abstracts[has_openalex] <- as.character(works$abstract[matched])
  if ("keywords" %in% names(works)) keyword_values[has_openalex] <- vapply(works$keywords[matched], keyword_text, character(1))
  if ("concepts" %in% names(works)) concept_values[has_openalex] <- vapply(works$concepts[matched], keyword_text, character(1), threshold = 0.40)
  if ("cited_by_count" %in% names(works)) citation_counts[has_openalex] <- suppressWarnings(as.numeric(works$cited_by_count[matched]))
}
message("Cobertura de metadados OpenAlex: ", sum(has_openalex), "/", length(refs_doi), " registros.")
writeLines(refs_doi[!has_openalex], file.path(bib_dir, "openalex_missing_dois.txt"), useBytes = TRUE)
M <- data.frame(
  AU = as.character(refs$authors),
  PY = suppressWarnings(as.numeric(refs$year)),
  TI = toupper(as.character(refs$title)),
  SO = toupper(as.character(refs$journal)),
  DI = refs_doi,
  AB = abstracts,
  DE = keyword_values,
  ID = concept_values,
  TC = citation_counts,
  DT = rep("ARTICLE", length(work_index)),
  DB = rep("OPENALEX", length(work_index)),
  stringsAsFactors = FALSE,
  check.names = FALSE
)
M$SR <- make.unique(paste(M$AU, M$PY, M$SO, sep = ", "))
rownames(M) <- M$SR
class(M) <- c("bibliometrixDB", "data.frame")
if (nrow(M) == 0) stop("A preparação para bibliometrix não produziu registros.")

saveRDS(M, file.path(bib_dir, "bibliometrix_records.rds"))
fields <- intersect(c("AU", "PY", "TI", "SO", "DI", "AB", "DE", "ID", "TC", "DT", "SR"), names(M))
write.csv(M[, fields, drop = FALSE], file.path(bib_dir, "bibliometrix_records.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

# Metadados compactos para conferir correspondência com as referências selecionadas.
metadata_fields <- intersect(c("doi", "display_name", "publication_year", "source_display_name", "type", "cited_by_count"), names(works))
metadata <- as.data.frame(works[, metadata_fields, drop = FALSE])
write.csv(metadata, file.path(bib_dir, "openalex_metadata.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

# Executa os métodos principais do bibliometrix e salva o resumo completo.
BA <- biblioAnalysis(M, sep = ";")
summary_obj <- summary(BA, k = 20, pause = FALSE)
summary_path <- file.path(bib_dir, "bibliometrix_summary.txt")
sink(summary_path)
cat("Registros incluídos:", nrow(M), "\n")
cat("Fonte de metadados: OpenAlex, consultada por DOI.\n")
cat("Os termos DE são keywords indexadas pelo OpenAlex, não necessariamente palavras-chave declaradas pelos autores.\n")
cat("Bibliometrix:", as.character(packageVersion("bibliometrix")), "\n")
cat("openalexR:", as.character(packageVersion("openalexR")), "\n\n")
print(summary_obj)
cat("\nNota de interpretação: a métrica de coautoria internacional impressa pelo bibliometrix como zero não é informativa neste conjunto, pois as afiliações foram omitidas por cobertura irregular. Não se deve interpretá-la como ausência de colaboração internacional.\n")
sink()
summary_lines <- readLines(summary_path, warn = FALSE, encoding = "UTF-8")
writeLines(trimws(summary_lines, which = "right"), summary_path, useBytes = TRUE)
saveRDS(summary_obj, file.path(bib_dir, "bibliometrix_summary.rds"))

# Estatísticas para relato e conferência editorial.
years <- seq(min(M$PY, na.rm = TRUE), max(M$PY, na.rm = TRUE))
annual <- data.frame(year = years,
                     articles = as.integer(table(factor(M$PY, levels = years))),
                     stringsAsFactors = FALSE)
write.csv(annual, file.path(bib_dir, "annual_production.csv"), row.names = FALSE, fileEncoding = "UTF-8")

sources <- sort(table(M$SO), decreasing = TRUE)
top_sources <- data.frame(journal = names(sources), articles = as.integer(sources), row.names = NULL)
write.csv(head(top_sources, 20), file.path(bib_dir, "top_sources.csv"), row.names = FALSE, fileEncoding = "UTF-8")

keyword_field <- if ("DE" %in% names(M) && any(!is.na(M$DE) & nzchar(M$DE))) "DE" else "ID"
kw <- trimws(unlist(strsplit(as.character(M[[keyword_field]]), ";", fixed = TRUE)))
kw <- kw[!is.na(kw) & nzchar(kw)]
keyword_counts <- sort(table(kw), decreasing = TRUE)
top_keywords <- data.frame(keyword = names(keyword_counts), articles = as.integer(keyword_counts), row.names = NULL)
write.csv(head(top_keywords, 30), file.path(bib_dir, "top_keywords.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# Gráfico de produção anual com anos sem publicação explicitamente exibidos como zero.
png(file.path(fig_dir, "bibliometria_producao_anual.png"), width = 1800, height = 1000, res = 180)
par(mar = c(5, 5, 3, 1), family = "sans", las = 1)
bp <- barplot(annual$articles, axisnames = FALSE,
              xlab = "Ano de publicação", ylab = "Artigos no corpus",
              main = "Produção anual do corpus bibliométrico",
              col = "#145A75", border = NA, las = 1)
tick_idx <- which(annual$year %% 5 == 0 | annual$year %in% c(min(years), max(years)))
axis(1, at = bp[tick_idx], labels = annual$year[tick_idx], las = 1, cex.axis = 0.85)
abline(h = pretty(c(0, max(annual$articles))), col = "#D8E1E5", lwd = 0.7)
dev.off()

# Principais keywords associadas pelo OpenAlex, sem as confundir com termos autorais.
topk <- head(top_keywords, 10)
png(file.path(fig_dir, "bibliometria_top_keywords.png"), width = 1800, height = 1200, res = 180)
par(mar = c(4, 17, 3, 1), family = "sans")
barplot(rev(topk$articles), names.arg = rev(topk$keyword), horiz = TRUE, las = 1,
        xlab = "Artigos", main = "Keywords indexadas mais frequentes",
        col = "#3A8F77", border = NA)
dev.off()

# Mapa de coocorrência; networkPlot seleciona n nós de maior grau.
net <- tryCatch(
  biblioNetwork(M, analysis = "co-occurrences", network = "author_keywords", sep = ";"),
  error = function(e) NULL
)
if (!is.null(net) && nrow(net) > 1) {
  png(file.path(fig_dir, "bibliometria_rede_palavras.png"), width = 1800, height = 1400, res = 180)
  tryCatch(
    networkPlot(net, n = min(8, nrow(net)), type = "circle",
                normalize = "association", size = TRUE, labelsize = 1.1,
                remove.isolates = TRUE, Title = "Coocorrência de palavras-chave no corpus"),
    error = function(e) message("Rede não renderizada: ", conditionMessage(e))
  )
  dev.off()
}

cat("Bibliometrix executado em ", nrow(M), " registro(s).\n", sep = "")
cat("Saídas: data/bibliometria/ e figuras/bibliometria_*.png\n")
