#!/usr/bin/env python3
"""
Script para transformar um .RData com os data.frames pampa_samples e points
(no qual points tem, por registro, um mini-dataframe 23×7 em points$time_series)
num único CSV achatado, conforme especificado.
"""


# python3 script_python_ajusta_base_pampa.py \
#   --rdata /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/pampa_points.RData \
#   --output /home/alex/Downloads/github/improving_crop_identification__rest/tmp/script_python/pampa_flat.csv


import argparse
import subprocess
import tempfile
import os
import pandas as pd
import json
import sys

def extract_with_rscript(rdata_path, tmpdir):
    """
    Executa um Rscript que:
      - carrega o .RData num ambiente separado
      - retira pampa_samples, points (sem time_series) e a lista de time_series
      - escreve pampa_samples.csv, points.csv e time_series.json em tmpdir
    """
    sam_csv = os.path.join(tmpdir, 'pampa_samples.csv')
    pts_csv = os.path.join(tmpdir, 'points.csv')
    ts_json = os.path.join(tmpdir, 'time_series.json')
    # código R inline
    r_code = f"""
    library(jsonlite)
    env <- new.env()
    load("{rdata_path}", envir=env)
    sam <- env[["pampa_samples"]]
    pts <- env[["points"]]
    ts_list <- lapply(pts$time_series, function(x) as.data.frame(x))
    pts$time_series <- NULL
    write.csv(sam, "{sam_csv}", row.names=FALSE)
    write.csv(pts, "{pts_csv}", row.names=FALSE)
    write(toJSON(ts_list, dataframe="columns", auto_unbox=TRUE), "{ts_json}")
    """
    cmd = ["Rscript", "--vanilla", "-e", r_code]
    subprocess.check_call(cmd)
    return sam_csv, pts_csv, ts_json

def main():
    p = argparse.ArgumentParser(
        description="Achata pampa_points.RData (pampa_samples + points$time_series) em CSV.")
    p.add_argument("--rdata",  required=True, help="Caminho para pampa_points.RData")
    p.add_argument("--output", required=True, help="CSV de saída achatado")
    args = p.parse_args()

    # diretório temporário para CSVs intermediários
    with tempfile.TemporaryDirectory() as tmp:
        try:
            sam_csv, pts_csv, ts_json = extract_with_rscript(args.rdata, tmp)
        except subprocess.CalledProcessError as e:
            print("Erro ao chamar Rscript:", e, file=sys.stderr)
            sys.exit(1)

        # 1) le pandas
        sam = pd.read_csv(sam_csv)
        pts = pd.read_csv(pts_csv)

        # 2) load JSON de time_series: é lista de dicts {B02:[...],B03:[...],...}
        with open(ts_json, "r") as f:
            ts_list = json.load(f)

        # quantas linhas tem cada mini-dataframe (deveria ser sempre 23)
        example = ts_list[0]
        n = len(next(iter(example.values())))

        # 3) constrói registros
        records = []
        for i in range(len(sam)):
            rec = {}
            rec.update(sam.iloc[i].to_dict())
            rec.update(pts.iloc[i].to_dict())

            # achata cada banda do time_series
            ts = ts_list[i]
            for band, vals in ts.items():
                for j, v in enumerate(vals, start=1):
                    rec[f"{band}.{j:02d}"] = v

            # calcula EVI e NDVI para cada sufixo
            for j in range(1, n+1):
                b8 = rec.get(f"B08.{j:02d}", float("nan"))
                b4 = rec.get(f"B04.{j:02d}", float("nan"))
                b2 = rec.get(f"B02.{j:02d}", float("nan"))
                # fórmula de EVI (2.5*(NIR-RED)/(1+NIR+6*RED-7.5*BLUE))
                try:
                    rec[f"EVI.{j:02d}"] = 2.5 * ((b8 - b4) / (1 + b8 + 6 * b4 - 7.5 * b2))
                except:
                    rec[f"EVI.{j:02d}"] = float("nan")
                # fórmula de NDVI ((NIR-RED)/(NIR+RED))
                try:
                    rec[f"NDVI.{j:02d}"] = (b8 - b4) / (b8 + b4)
                except:
                    rec[f"NDVI.{j:02d}"] = float("nan")

            records.append(rec)

        df = pd.DataFrame(records)

        # 4) reordena colunas:
        #   a) todas de pampa_samples
        order = list(sam.columns)
        #   b) depois todas de points (sem a coluna time_series)
        order += [c for c in pts.columns if c != "time_series"]
        #   c) depois as sufixadas por banda e índice
        bands = ["B02","B03","B04","B08","B11","B12","EVI","NDVI"]
        for band in bands:
            for j in range(1, n+1):
                name = f"{band}.{j:02d}"
                if name in df.columns:
                    order.append(name)
        # filtra só colunas existentes
        order = [c for c in order if c in df.columns]

        df = df[order]
        df.to_csv(args.output, index=False)
        print(f"CSV salvo em: {args.output}")

if __name__ == "__main__":
    main()
