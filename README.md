# SITS Sample Quality

**Fully automated training-data refinement for satellite image time series using automatically tuned self-organizing maps, cluster-constrained neighbourhoods, and a novel Bayes-inspired heuristic**

This repository contains the source code, dataset access information, and computational outputs associated with a fully automated framework for training-data refinement in Satellite Image Time Series (SITS).

The framework was developed to identify and remove labelled samples that are inconsistent with their local spectro-temporal context. It combines automatically tuned Self-Organizing Maps (SOM), clustering of SOM weight vectors, cluster-constrained neighbourhood analysis, and a Bayes-inspired count-based heuristic for sample-label consistency assessment.

The software accompanies the research article:

> Alex Oliveira, Marcos Silva, and Julio Navoni.  
> **Fully automated training-data refinement for satellite image time series using automatically tuned self-organizing maps, cluster-constrained neighbourhoods, and a novel Bayes-inspired heuristic.**  
> *GIScience & Remote Sensing*.  
> Manuscript under preparation/submission.

---

## Overview

Reliable labelled training data are essential for supervised classification of satellite image time series. However, reference datasets may contain inconsistencies caused by mislabelling, geolocation errors, spectral similarity among classes, temporal inconsistencies, atmospheric effects, and other sources of noise.

This project provides a reproducible and fully automated workflow for refining labelled SITS training datasets.

The proposed framework introduces three main methodological components:

1. **Automated SOM hyperparameter tuning**  
   SOM configurations are systematically evaluated using complementary quantization-error and neural-grid-occupancy criteria. In the experiments reported in the associated study, 550 candidate configurations were evaluated for each dataset.

2. **Cluster-constrained neighbourhoods**  
   SOM weight vectors are clustered, and neighbourhood evidence used to assess a sample is restricted to neurons belonging to the same cluster as the focal neuron. This provides a spectro-temporally coherent neighbourhood for sample-consistency assessment.

3. **Bayes-inspired count-based heuristic**  
   Sample-label consistency is assessed by combining empirical neighbourhood support and focal-neuron evidence through a variance-weighted aggregation mechanism. The resulting score is an empirical support measure and should not be interpreted as a formal Bayesian posterior probability.

The complete procedure is executed iteratively to generate a refined training dataset while maintaining explicit control over sample removal.

---

## Repository structure

```text
SITS-sample-quality/
├── api/
│   └── v.0.0.1/       # REST-based implementation of the processing workflow
├── datasets/          # Dataset access information and/or distributable data
├── results/           # Machine-readable computational outputs
└── README.md
```

The `api/v.0.0.1` directory contains the implementation of the computational workflow.

The `datasets` directory is intended to document the datasets used in the experiments and their corresponding access conditions. Some datasets used in the associated study originate from third-party sources and may therefore be subject to redistribution restrictions.

The `results` directory contains computational outputs associated with the experiments reported in the accompanying article.

---

## Computational workflow

The software implements the methodology as a REST-based processing workflow. The main stages include:

- input-data preparation and cleaning;
- initial classification assessment;
- feature centring;
- systematic SOM hyperparameter evaluation;
- neural-grid occupancy assessment;
- SOM training;
- clustering of SOM weight vectors;
- selection of the clustering solution;
- iterative sample-consistency assessment;
- generation of exclusion maps;
- training-data refinement;
- classification reassessment; and
- generation of statistical summaries and publication-oriented outputs.

The REST architecture makes the experimental sequence explicit and allows processing steps to be reproduced through parameterized HTTP requests.

---

## SOM hyperparameter selection

The experimental parameter space used in the associated study consists of:

- **11 SOM grid dimensions**;
- **5 initial neighbourhood widths (`sigma`)**; and
- **10 learning rates**.

The Cartesian product produces **550 candidate SOM configurations per dataset**.

Quantization error and neural-grid occupancy are used as complementary criteria for automatically selecting an appropriate SOM configuration.

---

## Cluster-constrained neighbourhood analysis

After SOM configuration, clustering algorithms are evaluated on the SOM weight vectors.

The implemented workflow supports:

- DBSCAN;
- HDBSCAN;
- k-Means; and
- hierarchical agglomerative clustering.

Candidate clustering solutions are assessed using:

- clustering accuracy (ACC);
- Normalized Mutual Information (NMI); and
- Adjusted Rand Index (ARI).

During sample-consistency assessment, only neighbouring neurons belonging to the **same cluster as the focal neuron** contribute neighbourhood evidence. This restriction is intended to prevent topologically adjacent but spectro-temporally different regions of the SOM from being treated as equivalent local evidence.

---

## Bayes-inspired sample-consistency heuristic

The framework uses a count-based heuristic inspired by the evidence-updating rationale of Bayesian reasoning.

For each sample, the procedure considers:

- empirical support for the sample label among eligible neighbouring neurons;
- evidence observed at the focal Best Matching Unit (BMU); and
- variability of the neighbourhood evidence.

These components are combined into an updated support score through variance-weighted aggregation.

This procedure **does not estimate prior, likelihood, or posterior probability distributions** and should therefore not be interpreted as a formal implementation or approximation of Bayes' theorem.

Samples can be classified by the implementation as:

- `kept`;
- `removed`; or
- `flagged`.

In the four datasets evaluated in the associated study, no expert intervention was required to resolve final cases.

---

## Experimental datasets

The associated study evaluates the framework using four real-world Brazilian SITS datasets acquired from MODIS and Sentinel-2 and covering different sensors, geographic regions, land-cover settings, and classification problems.

| Dataset | Sensor | Region / Biome | Access |
|---|---|---|---|
| Cerrado I | MODIS | Cerrado, Brazil | Publicly available |
| Cerrado II | Sentinel-2 MSI | Cerrado, Brazil | Subject to source-provider conditions |
| Pampa | Sentinel-2 MSI | Pampa, Brazil | Subject to source-provider conditions |
| Santana | Sentinel-2 MSI | Santana do São Francisco, Sergipe, Brazil | Publicly available |

### Public datasets

**Cerrado I**

Santos et al. (2021), *Quality control and class noise reduction of satellite image time series*.

Zenodo DOI:  
https://doi.org/10.5281/zenodo.3941278

**Santana**

Santos da Silva, Marcos Aurélio (2024).

Zenodo DOI:  
https://doi.org/10.5281/zenodo.22674760

### Restricted or third-party datasets

Cerrado II and Pampa contain data obtained from third-party sources and are not redistributed through this repository when redistribution rights do not permit it.

Access information and provenance for these datasets are documented in the accompanying article and in the `datasets` directory.

Users must comply with the terms and conditions established by the original data providers.

---

## Software environment

The software was developed and validated using Python 3.12.7.

The main direct dependencies are:

- Flask 3.1.0
- pandas 2.2.3
- scikit-learn 1.6.1
- NumPy 1.26.4
- MiniSom 2.3.1
- SciPy 1.13.1
- FastAPI 0.115.12
- Matplotlib 3.10.0
- seaborn 0.13.2
- HDBSCAN 0.8.40
- tabulate 0.9.0
- ReportLab 4.4.1
- pyshp 2.3.1
- pyreadr 0.5.3
- Pillow 11.1.0
- pdfrw 0.4

All direct Python dependencies and their validated versions are specified in
`requirements.txt`.

A reproducible environment can be created with:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Reproducibility

The repository is organized to preserve the computational materials required to reproduce and verify the analyses reported in the associated article.

The processing workflow preserves intermediate and final products associated with each experiment, including, where applicable:

- transformed datasets;
- trained SOM models;
- neural weights;
- clustering products;
- sample-removal decisions;
- classification results; and
- statistical summaries.

The version of the source code associated with the article will be archived through **Zenodo** as a versioned GitHub release and assigned a persistent DOI.

---

## Archived software release and DOI

A permanent Zenodo DOI for the software release associated with the article will be added here after the first archival release is created.

**Software DOI:** *to be added after the Zenodo archival release*

The archived release will provide an immutable snapshot of the software version used to produce the results reported in the article.

---

## Citation

If you use this software, please cite the associated article and the archived software release.

The complete citation and software DOI will be added after publication/archival.

A machine-readable `CITATION.cff` file will also be provided in this repository.

---

## Data availability

Dataset provenance, access conditions, source code, and machine-readable computational outputs are documented in this repository and in the Data Availability Statement of the associated article.

Repository:

https://github.com/alexpaulooliveira/SITS-sample-quality

The availability of individual datasets depends on the licensing and redistribution conditions established by their original providers. Public datasets are referenced through their persistent identifiers rather than unnecessarily duplicated.

---

## Authors

**Alex Oliveira**  
ORCID: https://orcid.org/0000-0002-8346-7954

**Marcos Silva**  
ORCID: https://orcid.org/0000-0002-5367-2869

**Julio Navoni**  
ORCID: https://orcid.org/0000-0001-8715-0527

---

## License

Licensing information for the source code will be specified before the first archived software release.

Dataset licenses and access conditions are independent of the software license and remain governed by the respective data providers.

---

## Acknowledgements

This repository contains the computational implementation and reproducibility materials associated with the research described above.

The proposed framework builds on previous research on quality control and class-noise reduction of satellite image time series, particularly:

Santos, L., Ferreira, K., Camara, G., Picoli, M., & Simoes, R. (2021).  
*Quality control and class noise reduction of satellite image time series.*  
ISPRS Journal of Photogrammetry and Remote Sensing, 177, 75–88.  
https://doi.org/10.1016/j.isprsjprs.2021.04.014
