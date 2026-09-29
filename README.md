# SITS Sample Quality

**Fully automated training-data refinement for satellite image time series using automatically tuned self-organizing maps, cluster-constrained neighbourhoods, and a novel Bayes-inspired heuristic**

## Overview

This repository contains the source code, datasets, and computational outputs associated with a fully automated framework for refining labelled training data in satellite image time series (SITS).

The framework is designed to identify and remove samples that are inconsistent with their local spectro-temporal context. It builds on Self-Organizing Maps (SOMs) and introduces three main methodological components:

1. **Automated SOM hyperparameter tuning**, in which candidate SOM configurations are systematically evaluated using complementary quantization-error and neural-grid-occupancy criteria.

2. **Cluster-constrained neighbourhoods**, in which neighbourhood evidence is restricted to neurons belonging to the same cluster as the focal neuron, providing spectro-temporally coherent local support.

3. **A novel Bayes-inspired count-based heuristic**, which combines empirical neighbourhood support and focal-neuron evidence using variance-weighted aggregation without requiring formal posterior estimation.

The complete workflow is designed to support reproducible and fully automated training-data refinement. In the four real-world datasets evaluated in the associated study, no expert intervention was required to resolve final cases.

## Repository structure

```text
SITS-sample-quality/
├── api/
│   └── v.0.0.1/
│       ├── app.py
│       └── img/
│           └── alg.png
├── datasets/
├── results/
├── README.md
└── requirements.txt
```

The main implementation is provided in:

```text
api/v.0.0.1/app.py
```

The `datasets/` directory contains or indexes the datasets used by the workflow, subject to their respective access conditions.

The `results/` directory contains machine-readable computational outputs associated with the experiments.

## Computational workflow

The main computational workflow comprises the following stages:

1. preparation and standardization of labelled satellite image time-series samples;
2. optional Local Outlier Factor (LOF) analysis;
3. systematic evaluation of SOM hyperparameter configurations;
4. selection of the SOM configuration using complementary quantization-error and neural-grid-occupancy criteria;
5. SOM training;
6. clustering of SOM weight vectors;
7. definition of cluster-constrained neighbourhoods;
8. assessment of sample-label consistency using neighbourhood and focal-neuron evidence;
9. application of the Bayes-inspired count-based heuristic;
10. generation of the exclusion map and refined dataset;
11. quantitative evaluation of the resulting training data.

The implementation exposes the workflow through a REST-based interface.

## Automated SOM hyperparameter tuning

For each dataset, the SOM hyperparameter search evaluates combinations of:

- 11 candidate neural-grid dimensions;
- 5 candidate neighbourhood-width (`sigma`) values;
- 10 candidate learning-rate values.

This results in **550 candidate SOM configurations per dataset**.

Candidate configurations are evaluated using two complementary criteria:

- quantization error; and
- neural-grid occupancy.

This procedure systematically selects the SOM configuration instead of relying on a manually chosen network configuration.

## Cluster-constrained neighbourhoods

After SOM training, neuron weight vectors are grouped using clustering methods.

The implementation supports clustering approaches including:

- DBSCAN;
- HDBSCAN;
- k-Means; and
- hierarchical agglomerative clustering.

Clustering quality can be evaluated using measures including Accuracy (ACC), Normalized Mutual Information (NMI), and Adjusted Rand Index (ARI).

For sample-consistency assessment, local neighbourhood evidence is restricted to neurons belonging to the **same cluster as the focal neuron**. This prevents spatially adjacent SOM neurons representing different spectro-temporal regimes from contributing indiscriminately to the same local assessment.

## Bayes-inspired count-based heuristic

The framework includes a Bayes-inspired heuristic for assessing sample-label consistency.

The heuristic does **not** estimate a formal Bayesian posterior probability. Instead, it combines empirical evidence derived from:

- the focal neuron; and
- its cluster-constrained neighbourhood.

The aggregation procedure uses local variability to weight the available evidence, so that more internally consistent neighbourhood evidence receives greater influence than highly heterogeneous evidence.

The framework supports sample statuses including kept, removed, and flagged cases. In the four datasets evaluated in the associated study, the final refined datasets contained only kept and removed samples; no expert intervention was required to resolve final cases.

## Datasets

The associated study evaluates the framework using four real-world Brazilian satellite image time-series datasets acquired from MODIS and Sentinel-2.

| Dataset | Sensor | Region / biome | Access |
| --- | --- | --- | --- |
| Cerrado I | MODIS | Cerrado | Public |
| Cerrado II | Sentinel-2 MSI | Cerrado | Subject to third-party data-access conditions |
| Pampa | Sentinel-2 MSI | Pampa | Subject to third-party data-access conditions |
| Santana | Sentinel-2 MSI | Santana do São Francisco, Sergipe, Brazil | Public |

### Cerrado I

The Cerrado I dataset is publicly available through Zenodo:

https://doi.org/10.5281/zenodo.3941278

### Cerrado II

The Cerrado II dataset is subject to third-party data-access conditions. Access should follow the conditions established by the original data providers.

### Pampa

The Pampa dataset is subject to third-party data-access conditions. Access should follow the conditions established by the original data providers.

### Santana

The Santana dataset is publicly available through Zenodo:

https://doi.org/10.5281/zenodo.22674760

The `datasets/` directory provides the repository-level organization associated with the datasets used in the study.

## Software environment

The software was developed and validated using **Python 3.12.7**.

The direct Python dependencies used by the implementation are:

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

All direct Python dependencies and their validated versions are specified in `requirements.txt`.

## Installation

A clean Python environment is recommended.

Using Python's built-in virtual-environment support:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The dependency set specified in `requirements.txt` was validated in a clean Python 3.12 environment using:

```bash
python -m pip check
```

with no broken requirements reported.

## Reproducibility

The repository is intended to provide the source code, dataset references, dependency specification, and machine-readable computational outputs required to reproduce and verify the computational workflow described in the associated study.

For reproducible execution, users should:

1. use Python 3.12;
2. create a clean virtual environment;
3. install the dependencies specified in `requirements.txt`;
4. use the datasets under their respective access conditions; and
5. execute the REST-based workflow implemented in `api/v.0.0.1/app.py`.

The source code version associated with the submitted study will be archived as a versioned software release. The corresponding persistent identifier (DOI) will be added here after archival.

## Results

Machine-readable outputs generated by the computational experiments are organized in the `results/` directory.

These outputs complement the quantitative results reported in the associated manuscript and are provided to facilitate verification and reproducibility.

## Data availability

The datasets, source code, and machine-readable computational outputs required to reproduce and verify the results reported in the associated study are available subject to the following conditions:

- **Cerrado I:** publicly available through Zenodo at https://doi.org/10.5281/zenodo.3941278.
- **Cerrado II:** subject to third-party data-access conditions.
- **Pampa:** subject to third-party data-access conditions.
- **Santana:** publicly available through Zenodo at https://doi.org/10.5281/zenodo.22674760.
- **Source code:** available in this GitHub repository.
- **Computational outputs:** available in the `results/` directory of this repository.

A persistent DOI for the version of the software associated with the submitted study will be provided after archival.

## Citation

A `CITATION.cff` file will be provided with the archived software release to supply machine-readable citation metadata.

The software DOI and recommended citation will be added after creation of the versioned release and archival.

## Related work

The framework builds on previous work on quality control and class-noise reduction in satellite image time series:

Santos et al. (2021). *Quality control and class noise reduction of satellite image time series*. ISPRS Journal of Photogrammetry and Remote Sensing, 177, 75–88.

https://doi.org/10.1016/j.isprsjprs.2021.04.014

## License

Licensing information will be provided before the versioned software release.

## Authors

Authorship and contributor information for the software will be formally specified in the `CITATION.cff` file accompanying the versioned release.

## Associated publication

This repository accompanies the manuscript:

**Fully automated training-data refinement for satellite image time series using automatically tuned self-organizing maps, cluster-constrained neighbourhoods, and a novel Bayes-inspired heuristic**

Publication metadata, including the article DOI, will be added after publication.
