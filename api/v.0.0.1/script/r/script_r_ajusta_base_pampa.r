# Necessita destes pacotes:
# install.packages(c("dplyr","purrr","tibble","readr","sf"))

library(dplyr)
library(purrr)
library(tibble)
library(readr)
library(sf)

# 1) carregar o .RData
load("/home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_r/pampa_points.RData")

# 2) converter qualquer coluna sf::sfc em WKT
if("geometry" %in% names(pampa_samples)) {
  pampa_samples <- pampa_samples %>%
    mutate(geometry = st_as_text(geometry))
}

# checar consistência de linhas
stopifnot(nrow(pampa_samples) == nrow(points))

# quantas datas em cada time_series?
ts0 <- as.data.frame(points$time_series[[1]])
if("Index" %in% colnames(ts0)) ts0 <- ts0 %>% select(-Index)
n_ts <- nrow(ts0)

# definir bandas e sufixos
bandas   <- c("B02","B03","B04","B08","B11","B12")
prefixos <- c(bandas, "EVI", "NDVI")
sufo     <- sprintf(".%02d", seq_len(n_ts))

# função que achata uma linha
achata_linha <- function(i) {
  ps <- pampa_samples[i, ]
  pt <- points[i, setdiff(names(points),"time_series")]
  ts_df <- as.data.frame(points$time_series[[i]])
  if("Index" %in% names(ts_df)) ts_df <- ts_df %>% select(-Index)
  
  # montar colunas de cada banda
  bandas_list <- map(bandas, function(b) {
    set_names(ts_df[[b]], paste0(b, sufo))
  }) %>% flatten()
  
  # calcular EVI e NDVI
  B04 <- ts_df$B04; B08 <- ts_df$B08; B02 <- ts_df$B02
  evi  <- 2.5 * ((B08 - B04) / (B08 + 6*B04 - 7.5*B02 + 1))
  ndvi <- (B08 - B04) / (B08 + B04)
  names(evi)  <- paste0("EVI",  sufo)
  names(ndvi) <- paste0("NDVI", sufo)
  
  # juntar tudo
  c(
    as.list(ps),
    as.list(pt),
    bandas_list,
    as.list(evi),
    as.list(ndvi)
  )
}

# 3) achatar todas as linhas
flattened <- map_dfr(seq_len(nrow(points)), achata_linha)

# 4) reordenar colunas
ord1   <- names(pampa_samples)
ord2   <- setdiff(names(points),"time_series")
ord_ts <- unlist(map(prefixos, ~ paste0(.x, sufo)))
flattened <- flattened %>% select(all_of(c(ord1, ord2, ord_ts)))

# 5) salvar CSV final
write_csv(flattened, "/home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_r/pampa_points_flattened.csv")
