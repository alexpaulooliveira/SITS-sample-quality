# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# '''
# script_python_importa_rdata_com_dataframe_em_coluna
# ----------------------------------------------------
# Gera um CSV a partir de um .RData contendo um objeto (parametrizado), onde uma coluna
# (list-column) armazena, por linha, um data frame com séries (esperado: 6 linhas).

# Parâmetros (obrigatórios, nesta ordem):
# a) Caminho do arquivo .RData;
# b) NOME DO OBJETO dentro do RData (ex.: points_1000_reg);
# c) Nome da coluna que aloca um data frame (list-column) — ex.: time_series;
# d) Lista (separada por vírgulas) com os nomes das colunas a importar do data frame interno — ex.: Index,B02,B03,...;
# e) Nome do arquivo CSV final (será salvo no MESMO diretório do .RData).

# Regras principais:
# - Para cada linha i=1..6 do data frame interno, cria colunas <NOME>.0i para cada nome informado em (d).
# - Cria também NDVI.0i e EVI.0i, calculadas somente se as bandas requeridas estiverem presentes em (d):
#     NDVI = (B08 - B04) / (B08 + B04)            (requer B08 e B04)
#     EVI  = 2.5*(B08 - B04)/(B08 + 6*B04 - 7.5*B02 + 1)  (requer B08, B04 e B02)
# - Remove a list-column original do CSV final.
# - O CSV final é salvo SEMPRE no mesmo diretório do .RData, com o nome (e) exatamente como informado.

# EXEMPLO DE USO:

# python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
#     /home/alex/Downloads/SSF3/ssf_points.RData \
#     points_2000_reg \
#     time_series \
#     "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
#     points_2000_reg.csv
    
# python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
#     /home/alex/Downloads/SSF3/ssf_points.RData \
#     points_3000_reg \
#     time_series \
#     "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
#     points_3000_reg.csv    
    
# python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
#     /home/alex/Downloads/SSF3/ssf_points.RData \
#     points_3000 \
#     time_series \
#     "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
#     points_3000.csv        
# '''

# import os
# import argparse
# import tempfile
# import subprocess
# from shutil import which


# def _rscript_available():
#     return which("Rscript") is not None


# def _run_r_fallback(rdata_path: str, obj_name: str, nested_col: str, bands_csv: str, out_path: str) -> str:
#     # Bloco R em raw-string; usa trimws() e trata datas + nomes case-insensitive
#     r_code = r'''
# args <- commandArgs(trailingOnly = TRUE)
# if (length(args) < 5) {
#   stop("Uso: Rscript temp.R <rdata_path> <obj_name> <nested_col> <bands_csv> <out_path>")
# }
# rdata_path <- args[1]
# obj_name   <- args[2]
# nested_col <- args[3]
# bands_csv  <- args[4]
# out_path   <- args[5]

# # Parse das colunas internas (split por vírgula + trim)
# bands <- trimws(unlist(strsplit(bands_csv, ",")))
# bands <- bands[nchar(bands) > 0]

# # nomes considerados "data" (case-insensitive)
# date_names <- c("index","date","data","dt","dia")

# suppressMessages({
#   tryCatch({
#     obj_names <- load(rdata_path)
#     loaded <- TRUE
#   }, error=function(e) {
#     loaded <- FALSE
#   })
#   if (!loaded) {
#     obj <- tryCatch(readRDS(rdata_path), error=function(e) NULL)
#     if (is.null(obj)) stop("Não foi possível carregar via load() nem readRDS().")
#     assign(obj_name, obj, envir=.GlobalEnv)
#     obj_names <- obj_name
#   }
# })

# # Localiza objeto solicitado (case-insensitive)
# name_candidates <- obj_names
# if (!(obj_name %in% name_candidates)) {
#   lc <- tolower(name_candidates)
#   if (tolower(obj_name) %in% lc) {
#     idx <- which(lc == tolower(obj_name))[1]
#     obj_name <- name_candidates[idx]  # usa o nome real carregado
#   } else {
#     stop(paste0("Objeto '", obj_name, "' não encontrado. Objetos no RData: ", paste(name_candidates, collapse=", ")))
#   }
# }

# df <- get(obj_name, envir=.GlobalEnv)

# if (!(nested_col %in% names(df))) {
#   stop(paste0("A coluna '", nested_col, "' não existe em '", obj_name, "'."))
# }

# # Helpers
# coerce_df <- function(x) {
#   if (is.null(x)) return(NULL)
#   if (inherits(x, "data.frame")) return(as.data.frame(x))
#   y <- tryCatch(as.data.frame(x), error=function(e) NULL)
#   return(y)
# }
# to_num <- function(v) suppressWarnings(as.numeric(v))
# make_suffix <- function(i) sprintf(".%02d", i)

# # --- util: mapeamento case-insensitive de nomes de colunas do ts ---
# # retorna o nome real no ts dado um nome pedido (qualquer case)
# resolve_name <- function(ts_names, requested) {
#   map <- setNames(ts_names, tolower(ts_names))
#   nm <- map[[tolower(requested)]]
#   if (is.null(nm)) return(NA_character_) else return(nm)
# }

# expected_rows <- 6L

# # Pré-cria colunas: se o nome da banda indicar "data", cria como character; caso contrário, numérica
# for (i in seq_len(expected_rows)) {
#   suf <- make_suffix(i)
#   for (b in bands) {
#     if (tolower(b) %in% date_names) {
#       df[[paste0(b, suf)]] <- as.character(NA)  # colunas de data como texto
#     } else {
#       df[[paste0(b, suf)]] <- NA_real_          # numéricas por padrão
#     }
#   }
#   df[[paste0("EVI",  suf)]] <- NA_real_
#   df[[paste0("NDVI", suf)]] <- NA_real_
# }

# # presença de bandas (case-insensitive) para NDVI/EVI
# lbands <- tolower(bands)
# hasB08 <- "b08" %in% lbands
# hasB04 <- "b04" %in% lbands
# hasB02 <- "b02" %in% lbands

# n <- nrow(df)
# for (row in seq_len(n)) {
#   ts <- coerce_df(df[[nested_col]][[row]])
#   if (is.null(ts) || nrow(ts) == 0) next

#   ts_names <- colnames(ts)

#   nr <- nrow(ts)
#   lim <- min(expected_rows, nr)
#   for (i in seq_len(lim)) {
#     suf <- make_suffix(i)

#     for (b in bands) {
#       real_b <- resolve_name(ts_names, b)   # nome real em ts (case-insensitive)
#       if (is.na(real_b)) {
#         # coluna pedida não existe no ts -> deixa NA
#         next
#       }

#       val <- ts[i, real_b][[1]]

#       if (tolower(b) %in% date_names || inherits(ts[[real_b]], "Date") || inherits(ts[[real_b]], c("POSIXct","POSIXt"))) {
#         # DATA: formata como texto
#         if (inherits(val, "Date")) {
#           val <- format(val, "%Y-%m-%d")
#         } else if (inherits(val, c("POSIXct","POSIXt"))) {
#           val <- format(as.POSIXct(val), "%Y-%m-%d %H:%M:%S")
#         } else if (is.numeric(val)) {
#           # número de dias desde 1970
#           val <- format(as.Date(val, origin="1970-01-01"), "%Y-%m-%d")
#         } else {
#           val <- as.character(val)
#         }
#         df[row, paste0(b, suf)] <- val  # preserva o NOME pedido (com o case que veio do usuário)
#       } else {
#         # numérico padrão
#         vnum <- to_num(val)
#         df[row, paste0(b, suf)] <- if (length(vnum)==1) vnum else NA_real_
#       }
#     }

#     # NDVI/EVI quando possível (usando nomes reais do ts)
#     if (hasB08 && hasB04) {
#       nmB08 <- resolve_name(ts_names, "B08")
#       nmB04 <- resolve_name(ts_names, "B04")
#       if (!is.na(nmB08) && !is.na(nmB04)) {
#         B08 <- to_num(ts[i, nmB08][[1]]); B04 <- to_num(ts[i, nmB04][[1]])
#         denom_ndvi <- B08 + B04
#         ndvi <- ifelse(!is.na(denom_ndvi) & denom_ndvi != 0, (B08 - B04) / denom_ndvi, NA_real_)
#         df[row, paste0("NDVI", suf)] <- ndvi
#       }
#     }
#     if (hasB08 && hasB04 && hasB02) {
#       nmB08 <- resolve_name(ts_names, "B08")
#       nmB04 <- resolve_name(ts_names, "B04")
#       nmB02 <- resolve_name(ts_names, "B02")
#       if (!is.na(nmB08) && !is.na(nmB04) && !is.na(nmB02)) {
#         B08 <- to_num(ts[i, nmB08][[1]]); B04 <- to_num(ts[i, nmB04][[1]]); B02 <- to_num(ts[i, nmB02][[1]])
#         denom_evi <- B08 + 6*B04 - 7.5*B02 + 1
#         evi <- ifelse(!is.na(denom_evi) & denom_evi != 0, 2.5 * ((B08 - B04) / denom_evi), NA_real_)
#         df[row, paste0("EVI",  suf)] <- evi
#       }
#     }
#   }
# }

# # Remove a coluna original
# df[[nested_col]] <- NULL

# # Conversão pós-processamento de datas:
# # 1) Se o prefixo antes de .NN for um dos date_names -> força texto
# date_like <- function(nm) tolower(sub("\\.\\d+$","", nm)) %in% date_names
# cols <- names(df)
# for (nm in cols) {
#   if (date_like(nm)) {
#     v <- df[[nm]]
#     if (inherits(v, "Date")) {
#       df[[nm]] <- format(v, "%Y-%m-%d")
#     } else if (inherits(v, c("POSIXct","POSIXt"))) {
#       df[[nm]] <- format(as.POSIXct(v), "%Y-%m-%d %H:%M:%S")
#     } else if (is.numeric(v)) {
#       rng <- suppressWarnings(range(v, na.rm=TRUE))
#       if (is.finite(rng[1]) && is.finite(rng[2]) && rng[1] > 10000 && rng[2] < 50000) {
#         df[[nm]] <- format(as.Date(v, origin="1970-01-01"), "%Y-%m-%d")
#       } else {
#         df[[nm]] <- ifelse(is.na(v), NA, as.character(v))
#       }
#     } else {
#       df[[nm]] <- as.character(v)
#     }
#   }
# }

# # Escreve CSV no caminho exato parametrizado
# dir.create(dirname(out_path), showWarnings = FALSE, recursive = TRUE)
# utils::write.csv(df, file=out_path, row.names=FALSE, na="")
# cat(out_path)
# '''
#     with tempfile.TemporaryDirectory() as tmpd:
#         rfile = os.path.join(tmpd, "ajusta_param_temp.R")
#         with open(rfile, "w", encoding="utf-8") as f:
#             f.write(r_code)
#         proc = subprocess.run(
#             ["Rscript", rfile, rdata_path, obj_name, nested_col, bands_csv, out_path],
#             capture_output=True, text=True
#         )
#         if proc.returncode != 0:
#             raise RuntimeError(f"Rscript falhou:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
#         out_path_rt = proc.stdout.strip().splitlines()[-1].strip()
#         return out_path_rt


# def script_python_importa_rdata_com_dataframe_em_coluna(
#     rdata_path: str, obj_name: str, nested_col: str, inner_cols_csv: str, out_filename: str
# ) -> str:
#     '''
#     Executa a transformação e salva o CSV com nome parametrizado
#     no mesmo diretório do RData.
#     '''
#     if not os.path.isfile(rdata_path):
#         raise FileNotFoundError(f"Arquivo não encontrado: {rdata_path}")
#     if not out_filename or os.path.basename(out_filename) != out_filename:
#         raise ValueError("Forneça apenas o NOME do arquivo de saída (sem diretórios).")
#     if not nested_col or any(c in nested_col for c in ('/', '\\')):
#         raise ValueError("Informe apenas o nome da coluna (sem barras).")
#     if not inner_cols_csv or len(inner_cols_csv.strip()) == 0:
#         raise ValueError("Informe a lista de colunas internas separadas por vírgulas.")
#     if not obj_name or any(c in obj_name for c in ('/', '\\')):
#         raise ValueError("Informe apenas o nome do objeto dentro do RData (sem barras).")

#     out_dir = os.path.dirname(os.path.abspath(rdata_path)) or "."
#     out_path = os.path.join(out_dir, out_filename)

#     if not _rscript_available():
#         raise EnvironmentError("Rscript não encontrado no PATH. Instale R e garanta que 'Rscript' esteja acessível.")

#     out_csv = _run_r_fallback(rdata_path, obj_name, nested_col, inner_cols_csv, out_path)
#     return out_csv


# def main():
#     parser = argparse.ArgumentParser(
#         description="Gera CSV a partir de um .RData parametrizando NOME DO OBJETO, coluna list-column e colunas internas (bands)."
#     )
#     parser.add_argument("rdata_path", help="Caminho para o arquivo .RData")
#     parser.add_argument("obj_name", help="NOME do objeto dentro do RData (ex.: points_1000_reg)")
#     parser.add_argument("nested_col", help="Nome da coluna que aloca um data frame (ex.: time_series)")
#     parser.add_argument("inner_cols_csv", help="Nomes das colunas do data frame interno, separados por vírgula (ex.: Index,B02,B04,B08,...)")
#     parser.add_argument("out_filename", help="NOME do CSV a ser gerado (ex.: saida.csv)")
#     args = parser.parse_args()

#     out_csv = script_python_importa_rdata_com_dataframe_em_coluna(
#         args.rdata_path, args.obj_name, args.nested_col, args.inner_cols_csv, args.out_filename
#     )
#     print(out_csv)


# if __name__ == "__main__":
#     main()





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
script_python_importa_rdata_com_dataframe_em_coluna
----------------------------------------------------
Gera um CSV a partir de um .RData contendo um objeto (parametrizado), onde uma coluna
(list-column) armazena, por linha, um data frame com séries (agora com quantidade de
linhas variável e validada).

Parâmetros (obrigatórios, nesta ordem):
a) Caminho do arquivo .RData;
b) NOME DO OBJETO dentro do RData (ex.: points_1000_reg);
c) Nome da coluna que aloca um data frame (list-column) — ex.: time_series;
d) Lista (separada por vírgulas) com os nomes das colunas a importar do data frame interno — ex.: Index,B02,B03,...;
e) Nome do arquivo CSV final (será salvo no MESMO diretório do .RData).

Regras principais:
- Para cada linha i=1..M do data frame interno (M detectado automaticamente),
  cria colunas <NOME>.0i para cada nome informado em (d).
- Cria também NDVI.0i e EVI.0i, calculadas somente se as bandas requeridas estiverem presentes em (d):
    NDVI = (B08 - B04) / (B08 + B04)            (requer B08 e B04)
    EVI  = 2.5*(B08 - B04)/(B08 + 6*B04 - 7.5*B02 + 1)  (requer B08, B04 e B02)
- **Validação**: todos os data frames da list-column devem ter a MESMA quantidade de linhas.
  Caso contrário, o processo é interrompido com uma mensagem descritiva.
- Remove a list-column original do CSV final.
- O CSV final é salvo SEMPRE no mesmo diretório do .RData, com o nome (e) exatamente como informado.

EXEMPLOS DE USO:

python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
    /home/alex/Downloads/SSF3/ssf_points.RData \
    points_2000_reg \
    time_series \
    "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
    points_2000_reg.csv
    
python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
    /home/alex/Downloads/SSF3/ssf_points.RData \
    points_3000_reg \
    time_series \
    "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
    points_3000_reg.csv    
    
python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
    /home/alex/Downloads/SSF3/ssf_points.RData \
    points_3000 \
    time_series \
    "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
    points_3000.csv        
    
    
python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
    /home/alex/Downloads/SSF10/ssf_points_10000.RData \
    points_10000_reg \
    time_series \
    "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
    points_10000_reg.csv            
    

python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
    /home/alex/Downloads/SSF10/ssf_points_10000.RData \
    points_10000 \
    time_series \
    "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
    points_10000.csv            
        
        
        
python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
    /home/alex/Downloads/SSF50/ssf_points_50000.RData \
    points_50000_reg \
    time_series \
    "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
    points_50000_reg.csv            
        
       
python /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/script_python_importa_rdata_com_dataframe_em_coluna.py \
    /home/alex/Downloads/SSF50/ssf_points_50000.RData \
    points_50000 \
    time_series \
    "Index,B02,B03,B04,B05,B06,B07,B08,B11,B12,B8A" \
    points_50000.csv            
        

        
'''

import os
import argparse
import tempfile
import subprocess
from shutil import which


def _rscript_available():
    return which("Rscript") is not None


def _run_r_fallback(rdata_path: str, obj_name: str, nested_col: str, bands_csv: str, out_path: str) -> str:
    # Bloco R em raw-string; nomes case-insensitive e tratamento de datas
    r_code = r'''
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 5) {
  stop("Uso: Rscript temp.R <rdata_path> <obj_name> <nested_col> <bands_csv> <out_path>")
}
rdata_path <- args[1]
obj_name   <- args[2]
nested_col <- args[3]
bands_csv  <- args[4]
out_path   <- args[5]

# Parse das colunas internas (split por vírgula + trim)
bands <- trimws(unlist(strsplit(bands_csv, ",")))
bands <- bands[nchar(bands) > 0]

# nomes considerados "data" (case-insensitive)
date_names <- c("index","date","data","dt","dia")

suppressMessages({
  tryCatch({
    obj_names <- load(rdata_path)
    loaded <- TRUE
  }, error=function(e) {
    loaded <- FALSE
  })
  if (!loaded) {
    obj <- tryCatch(readRDS(rdata_path), error=function(e) NULL)
    if (is.null(obj)) stop("Não foi possível carregar via load() nem readRDS().")
    assign(obj_name, obj, envir=.GlobalEnv)
    obj_names <- obj_name
  }
})

# Localiza objeto solicitado (case-insensitive)
name_candidates <- obj_names
if (!(obj_name %in% name_candidates)) {
  lc <- tolower(name_candidates)
  if (tolower(obj_name) %in% lc) {
    idx <- which(lc == tolower(obj_name))[1]
    obj_name <- name_candidates[idx]  # usa o nome real carregado
  } else {
    stop(paste0("Objeto '", obj_name, "' não encontrado. Objetos no RData: ", paste(name_candidates, collapse=", ")))
  }
}

df <- get(obj_name, envir=.GlobalEnv)

if (!(nested_col %in% names(df))) {
  stop(paste0("A coluna '", nested_col, "' não existe em '", obj_name, "'."))
}

# Helpers
coerce_df <- function(x) {
  if (is.null(x)) return(NULL)
  if (inherits(x, "data.frame")) return(as.data.frame(x))
  y <- tryCatch(as.data.frame(x), error=function(e) NULL)
  return(y)
}
to_num <- function(v) suppressWarnings(as.numeric(v))
make_suffix <- function(i) sprintf(".%02d", i)

# --- util: mapeamento case-insensitive de nomes de colunas do ts ---
# retorna o nome real no ts dado um nome pedido (qualquer case)
resolve_name <- function(ts_names, requested) {
  map <- setNames(ts_names, tolower(ts_names))
  nm <- map[[tolower(requested)]]
  if (is.null(nm)) return(NA_character_) else return(nm)
}

# ----------------------------
# 1) Descobrir M (nº de linhas) do df interno e validar uniformidade
# ----------------------------
get_rows <- function(obj) {
  x <- coerce_df(obj)
  if (is.null(x)) return(NA_integer_)
  nrow(x)
}

rows_vec <- sapply(df[[nested_col]], get_rows)
rows_vec <- rows_vec[!is.na(rows_vec) & rows_vec > 0]

if (length(rows_vec) == 0) {
  stop(paste0("Nenhum data frame válido encontrado na coluna '", nested_col, "'."))
}

expected_rows <- rows_vec[1]
mismatch_idx <- which(rows_vec != expected_rows)
if (length(mismatch_idx) > 0) {
  bad <- mismatch_idx[1]
  stop(paste0(
    "Todos os data frames da coluna '", nested_col,
    "' devem ter o MESMO número de linhas. Encontrado primeiro conflito na linha ",
    bad, ": esperado ", expected_rows, ", obtido ", rows_vec[bad], "."
  ))
}

# ----------------------------
# 2) Pré-criar colunas de saída para M linhas
# ----------------------------
for (i in seq_len(expected_rows)) {
  suf <- make_suffix(i)
  for (b in bands) {
    if (tolower(b) %in% date_names) {
      df[[paste0(b, suf)]] <- as.character(NA)  # colunas de data como texto
    } else {
      df[[paste0(b, suf)]] <- NA_real_          # numéricas por padrão
    }
  }
  df[[paste0("EVI",  suf)]] <- NA_real_
  df[[paste0("NDVI", suf)]] <- NA_real_
}

# presença de bandas (case-insensitive) para NDVI/EVI
lbands <- tolower(bands)
hasB08 <- "b08" %in% lbands
hasB04 <- "b04" %in% lbands
hasB02 <- "b02" %in% lbands

# ----------------------------
# 3) Preencher valores linha a linha
# ----------------------------
n <- nrow(df)
for (row in seq_len(n)) {
  ts <- coerce_df(df[[nested_col]][[row]])
  if (is.null(ts) || nrow(ts) == 0) next

  ts_names <- colnames(ts)
  nr <- nrow(ts)
  lim <- min(expected_rows, nr)  # por segurança; em tese nr == expected_rows

  for (i in seq_len(lim)) {
    suf <- make_suffix(i)

    for (b in bands) {
      real_b <- resolve_name(ts_names, b)   # nome real em ts (case-insensitive)
      if (is.na(real_b)) next

      val <- ts[i, real_b][[1]]

      if (tolower(b) %in% date_names || inherits(ts[[real_b]], "Date") || inherits(ts[[real_b]], c("POSIXct","POSIXt"))) {
        # DATA: formata como texto
        if (inherits(val, "Date")) {
          val <- format(val, "%Y-%m-%d")
        } else if (inherits(val, c("POSIXct","POSIXt"))) {
          val <- format(as.POSIXct(val), "%Y-%m-%d %H:%M:%S")
        } else if (is.numeric(val)) {
          # número de dias desde 1970
          val <- format(as.Date(val, origin="1970-01-01"), "%Y-%m-%d")
        } else {
          val <- as.character(val)
        }
        df[row, paste0(b, suf)] <- val  # preserva o case solicitado
      } else {
        # numérico padrão
        vnum <- to_num(val)
        df[row, paste0(b, suf)] <- if (length(vnum)==1) vnum else NA_real_
      }
    }

    # NDVI/EVI quando possível (usando nomes reais do ts)
    if (hasB08 && hasB04) {
      nmB08 <- resolve_name(ts_names, "B08")
      nmB04 <- resolve_name(ts_names, "B04")
      if (!is.na(nmB08) && !is.na(nmB04)) {
        B08 <- to_num(ts[i, nmB08][[1]]); B04 <- to_num(ts[i, nmB04][[1]])
        denom_ndvi <- B08 + B04
        ndvi <- ifelse(!is.na(denom_ndvi) & denom_ndvi != 0, (B08 - B04) / denom_ndvi, NA_real_)
        df[row, paste0("NDVI", suf)] <- ndvi
      }
    }
    if (hasB08 && hasB04 && hasB02) {
      nmB08 <- resolve_name(ts_names, "B08")
      nmB04 <- resolve_name(ts_names, "B04")
      nmB02 <- resolve_name(ts_names, "B02")
      if (!is.na(nmB08) && !is.na(nmB04) && !is.na(nmB02)) {
        B08 <- to_num(ts[i, nmB08][[1]]); B04 <- to_num(ts[i, nmB04][[1]]); B02 <- to_num(ts[i, nmB02][[1]])
        denom_evi <- B08 + 6*B04 - 7.5*B02 + 1
        evi <- ifelse(!is.na(denom_evi) & denom_evi != 0, 2.5 * ((B08 - B04) / denom_evi), NA_real_)
        df[row, paste0("EVI",  suf)] <- evi
      }
    }
  }
}

# Remove a coluna original (list-column)
df[[nested_col]] <- NULL

# Conversão pós-processamento de datas:
date_like <- function(nm) tolower(sub("\\.\\d+$","", nm)) %in% date_names
cols <- names(df)
for (nm in cols) {
  if (date_like(nm)) {
    v <- df[[nm]]
    if (inherits(v, "Date")) {
      df[[nm]] <- format(v, "%Y-%m-%d")
    } else if (inherits(v, c("POSIXct","POSIXt"))) {
      df[[nm]] <- format(as.POSIXct(v), "%Y-%m-%d %H:%M:%S")
    } else if (is.numeric(v)) {
      rng <- suppressWarnings(range(v, na.rm=TRUE))
      if (is.finite(rng[1]) && is.finite(rng[2]) && rng[1] > 10000 && rng[2] < 50000) {
        df[[nm]] <- format(as.Date(v, origin="1970-01-01"), "%Y-%m-%d")
      } else {
        df[[nm]] <- ifelse(is.na(v), NA, as.character(v))
      }
    } else {
      df[[nm]] <- as.character(v)
    }
  }
}

# Escreve CSV no caminho exato parametrizado
dir.create(dirname(out_path), showWarnings = FALSE, recursive = TRUE)
utils::write.csv(df, file=out_path, row.names=FALSE, na="")
cat(out_path)
'''
    with tempfile.TemporaryDirectory() as tmpd:
        rfile = os.path.join(tmpd, "ajusta_param_temp.R")
        with open(rfile, "w", encoding="utf-8") as f:
            f.write(r_code)
        proc = subprocess.run(
            ["Rscript", rfile, rdata_path, obj_name, nested_col, bands_csv, out_path],
            capture_output=True, text=True
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Rscript falhou:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        out_path_rt = proc.stdout.strip().splitlines()[-1].strip()
        return out_path_rt


def script_python_importa_rdata_com_dataframe_em_coluna(
    rdata_path: str, obj_name: str, nested_col: str, inner_cols_csv: str, out_filename: str
) -> str:
    '''
    Executa a transformação e salva o CSV com nome parametrizado
    no mesmo diretório do RData.
    '''
    if not os.path.isfile(rdata_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {rdata_path}")
    if not out_filename or os.path.basename(out_filename) != out_filename:
        raise ValueError("Forneça apenas o NOME do arquivo de saída (sem diretórios).")
    if not nested_col or any(c in nested_col for c in ('/', '\\')):
        raise ValueError("Informe apenas o nome da coluna (sem barras).")
    if not inner_cols_csv or len(inner_cols_csv.strip()) == 0:
        raise ValueError("Informe a lista de colunas internas separadas por vírgulas.")
    if not obj_name or any(c in obj_name for c in ('/', '\\')):
        raise ValueError("Informe apenas o nome do objeto dentro do RData (sem barras).")

    out_dir = os.path.dirname(os.path.abspath(rdata_path)) or "."
    out_path = os.path.join(out_dir, out_filename)

    if not _rscript_available():
        raise EnvironmentError("Rscript não encontrado no PATH. Instale R e garanta que 'Rscript' esteja acessível.")

    out_csv = _run_r_fallback(rdata_path, obj_name, nested_col, inner_cols_csv, out_path)
    return out_csv


def main():
    parser = argparse.ArgumentParser(
        description="Gera CSV a partir de um .RData parametrizando NOME DO OBJETO, coluna list-column e colunas internas (bands)."
    )
    parser.add_argument("rdata_path", help="Caminho para o arquivo .RData")
    parser.add_argument("obj_name", help="NOME do objeto dentro do RData (ex.: points_1000_reg)")
    parser.add_argument("nested_col", help="Nome da coluna que aloca um data frame (ex.: time_series)")
    parser.add_argument("inner_cols_csv", help="Nomes das colunas do data frame interno, separados por vírgula (ex.: Index,B02,B04,B08,...)")
    parser.add_argument("out_filename", help="NOME do CSV a ser gerado (ex.: saida.csv)")
    args = parser.parse_args()

    out_csv = script_python_importa_rdata_com_dataframe_em_coluna(
        args.rdata_path, args.obj_name, args.nested_col, args.inner_cols_csv, args.out_filename
    )
    print(out_csv)


if __name__ == "__main__":
    main()







