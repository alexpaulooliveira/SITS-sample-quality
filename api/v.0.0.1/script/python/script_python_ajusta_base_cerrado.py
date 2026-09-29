#!/usr/bin/env python3
"""
Fallback entre rpy2 e Rscript para carregar RData + achatamento em CSV.
"""

import argparse
import os
import sys
import json
import tempfile
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime

def try_load_with_rpy2(path):
    try:
        import rpy2.robjects as ro
        import rpy2.robjects.pandas2ri as pandas2ri
        pandas2ri.activate()
        ro.r['load'](path)
        sam = pandas2ri.rpy2py(ro.globalenv['cerrados_samples'])
        pts = pandas2ri.rpy2py(ro.globalenv['points'])
        # extrair lista de mini-data.frames de points$time_series
        r_ts = ro.globalenv['points'].rx2('time_series')
        ts_list = [pandas2ri.rpy2py(r_ts[i]) for i in range(len(r_ts))]
        pts = pts.drop(columns=['time_series'])
        return sam, pts, ts_list
    except Exception as e:
        # qualquer falha em rpy2 → fallback
        return None

def load_via_rscript(path):
    # prepara dir temporário
    td = tempfile.TemporaryDirectory()
    tmp = td.name
    samples_csv = os.path.join(tmp, "samples.csv")
    points_csv  = os.path.join(tmp, "points.csv")
    ts_json     = os.path.join(tmp, "time_series.json")

    # comando Rscript (exige jsonlite instalado em R)
    r_cmd = f"""
      load("{path}");
      library(jsonlite);
      write.csv(cerrados_samples, file="{samples_csv}", row.names=FALSE);
      pts2 <- points; pts2$time_series <- NULL;
      write.csv(pts2, file="{points_csv}", row.names=FALSE);
      js <- toJSON(points$time_series, dataframe="columns");
      write(js, file="{ts_json}");
    """
    try:
        subprocess.check_call(["Rscript", "--vanilla", "-e", r_cmd], stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        td.cleanup()
        raise RuntimeError(f"Rscript fallback falhou (stderr na tela).") from e

    # carregar em pandas
    sam = pd.read_csv(samples_csv)
    pts = pd.read_csv(points_csv)
    with open(ts_json, "r") as f:
        # ts_json é um array de length N, cada elemento é dict col->list(26)
        ts_list = json.load(f)
        # converter cada dict em DataFrame
        ts_list = [pd.DataFrame(rec) for rec in ts_list]

    td.cleanup()
    return sam, pts, ts_list

def load_rdata(path):
    # 1) tenta rpy2
    res = try_load_with_rpy2(path)
    if res:
        return res
    # 2) fallback Rscript + jsonlite
    return load_via_rscript(path)

def flatten_and_save(sam, pts, ts_list, output_csv):
    n = ts_list[0].shape[0]    # deve ser 26
    bands = list(ts_list[0].columns)

    records = []
    for i in range(len(sam)):
        rec = {}
        rec.update(sam.iloc[i].to_dict())
        rec.update(pts.iloc[i].to_dict())
        ts = ts_list[i]
        for band in bands:
            vals = ts[band].tolist()
            for j, v in enumerate(vals, start=1):
                rec[f"{band}.{j:02d}"] = v
        for j in range(1, n+1):
            b8a = rec.get(f"B8A.{j:02d}", np.nan)
            b4  = rec.get(f"B04.{j:02d}", np.nan)
            b2  = rec.get(f"B02.{j:02d}", np.nan)
            # EVI
            try:
                rec[f"EVI.{j:02d}"] = 2.5 * ((b8a - b4) / (1 + b8a + 6*b4 - 7.5*b2))
            except:
                rec[f"EVI.{j:02d}"] = np.nan
            # NDVI
            try:
                rec[f"NDVI.{j:02d}"] = (b8a - b4) / (b8a + b4)
            except:
                rec[f"NDVI.{j:02d}"] = np.nan
        records.append(rec)

    df = pd.DataFrame(records)

    # reordena colunas
    order = []
    order += list(sam.columns)
    order += list(pts.columns)
    blocos = ['B02','B03','B04','B05','B06','B07','B8A','B11','B12','EVI','NDVI']
    for band in blocos:
        for j in range(1, n+1):
            nm = f"{band}.{j:02d}"
            if nm in df.columns:
                order.append(nm)
    df = df[order]
    df.to_csv(output_csv, index=False)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rdata",  required=True, help="caminho para cerrado_points.RData")
    p.add_argument("--output", required=True, help="CSV de saída achatado")
    args = p.parse_args()

    sam, pts, ts_list = load_rdata(args.rdata)
    flatten_and_save(sam, pts, ts_list, args.output)
    print("Pronto.")

if __name__ == "__main__":
    main()
