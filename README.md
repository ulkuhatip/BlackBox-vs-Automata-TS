# BlackBox-vs-Automata-TS

This project compares two different approaches for time-series anomaly detection:

- black-box deep learning models
- interpretable probabilistic automata models

The project uses two datasets:

- `SKAB`
- `BATADAL`

The goal is not only to find the best score, but to analyze how different model families behave under different data conditions:

- original data
- noisy data
- unseen pattern data

This README is written as an onboarding guide for a teammate who is new to the project.

## Getting Started

These steps are intended for Windows users working in PowerShell.

### 1. Clone the repository

```powershell
git clone <repo-url>
cd BlackBox-vs-Automata-TS
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

If `python` does not work on your machine, try:

```powershell
py -3 -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Verify the dataset layout

Make sure the raw data is placed exactly like this:

```text
data/raw/skab/valve1/*.csv
data/raw/skab/valve2/*.csv
data/raw/batadal/BATADAL_dataset04.csv
```

### 6. Review configuration files

Check:

- `configs/skab.yaml`
- `configs/batadal.yaml`

These files define:

- dataset paths
- preprocessing options
- model settings
- automata parameters
- experiment seeds

### 7. Run the entry point

Current scaffold command:

```powershell
python -m src.main
```

If needed:

```powershell
py -3 -m src.main
```

### 8. Run tests

```powershell
pytest
```

At the current scaffold stage, tests are basic sanity checks. Later they should validate real project behavior.

## Project Goal

We want to answer these questions:

- How do deep learning and automata-based models behave on time-series anomaly detection?
- How stable are they across datasets, seeds, and scenarios?
- How do they react to noise and unseen symbolic patterns?
- Can the automata model explain its decisions through transition probabilities?

## Datasets

### SKAB

We use only:

- `valve1`
- `valve2`

All CSV files inside these folders are concatenated into one combined dataset.

During the merge we add:

- `source_group`: whether the record comes from `valve1` or `valve2`
- `source_file`: the original CSV filename

Target column:

- `anomaly`

Columns that must not be used as model input:

- `datetime`
- `changepoint`
- `source_group`
- `source_file`

### BATADAL

We use only:

- `Training Dataset 2`

In the current local project this file is:

- `data/raw/batadal/BATADAL_dataset04.csv`

Target column:

- `ATT_FLAG`

The time column must not be used directly as a model feature. It is used only for:

- keeping chronological order
- time-based splitting
- temporal interpretation of results

## High-Level Workflow

This is the order in which the project should be built and executed.

1. Organize raw data in `data/raw/`
2. Load and validate SKAB and BATADAL files
3. Build processed datasets in `data/processed/`
4. Split data correctly without leakage
5. Apply preprocessing using train-only fitting
6. Train deep learning models
7. Build the symbolic automata pipeline
8. Handle unseen patterns with Levenshtein mapping
9. Evaluate all models
10. Generate explainability outputs for the automata model
11. Save metrics, logs, figures, and JSON outputs
12. Summarize everything in the final report

## Directory Guide

Below is the intended role of each folder and when it gets populated.

```text
BlackBox-vs-Automata-TS/
|
|-- data/
|   |-- raw/
|   |   |-- skab/
|   |   |   |-- valve1/
|   |   |   `-- valve2/
|   |   `-- batadal/
|   |       `-- BATADAL_dataset04.csv
|   `-- processed/
|       |-- skab/
|       `-- batadal/
|
|-- configs/
|   |-- skab.yaml
|   `-- batadal.yaml
|
|-- src/
|   |-- data/
|   |-- features/
|   |-- models/
|   |   |-- deep_learning/
|   |   `-- automata/
|   |-- explainability/
|   |-- evaluation/
|   |-- experiments/
|   |-- utils/
|   `-- main.py
|
|-- tests/
|-- outputs/
|   |-- logs/
|   |-- metrics/
|   |-- explainability/
|   `-- figures/
|-- notebooks/
|   `-- eda.ipynb
|-- requirements.txt
|-- README.md
`-- .gitignore
```

### `data/`

This folder contains all dataset files.

### `data/raw/`

This is where original, untouched source data lives.

What goes here:

- original SKAB CSV files
- original BATADAL CSV file

When it is filled:

- at the very beginning of the project

Important rule:

- files in `raw/` should stay unchanged

### `data/processed/`

This folder stores datasets after loading, merging, cleaning, splitting, or transformation.

What goes here:

- merged SKAB dataset
- SKAB fold-specific train/test files
- BATADAL train/validation/test files
- optionally normalized or PCA-ready intermediate outputs

When it is filled:

- after dataset loading and preprocessing scripts are run

Typical examples:

- `data/processed/skab/combined.csv`
- `data/processed/skab/fold_1_train.csv`
- `data/processed/skab/fold_1_test.csv`
- `data/processed/batadal/train.csv`
- `data/processed/batadal/validation.csv`
- `data/processed/batadal/test.csv`

### `configs/`

This folder contains central configuration files for each dataset.

What goes here:

- dataset paths
- split strategy
- preprocessing settings
- model parameters
- automata parameters
- experiment seeds

When it is filled:

- before running experiments
- updated whenever we change hyperparameters or experiment settings

Why it matters:

- no hard-coded parameters should be scattered inside the codebase

### `src/`

This is the main source code folder.

### `src/data/`

This package handles reading, validating, preparing, and splitting data.

Files:

- `loaders.py`: shared loading helpers and shared path abstractions
- `skab_loader.py`: reads all SKAB files, concatenates them, adds `source_group` and `source_file`
- `batadal_loader.py`: reads BATADAL and validates its columns
- `preprocess.py`: central preprocessing pipeline
- `scaling.py`: normalization logic; must fit only on train data
- `pca.py`: PCA logic; must fit only on train data and transform validation/test with the same PCA

When this folder is used:

- immediately after project setup
- before any training starts

### `src/features/`

This package contains feature engineering and symbolic representation logic.

Files:

- `windowing.py`: sliding window creation
- `paa.py`: Piecewise Aggregate Approximation
- `sax.py`: Symbolic Aggregate approXimation
- `noise.py`: Gaussian noise injection for the noise scenario

When this folder is used:

- during automata pipeline construction
- during noisy scenario experiments

### `src/models/`

This package contains all model implementations.

### `src/models/deep_learning/`

This folder contains black-box models.

Files:

- `lstm.py`
- `gru.py`
- `cnn1d.py`

What they should do:

- receive preprocessed sequences
- train with fixed experiment settings
- save predictions for evaluation

When this folder is used:

- after preprocessing and sequence preparation

### `src/models/automata/`

This folder contains the interpretable symbolic model.

Files:

- `automaton.py`: main probabilistic automata class
- `transitions.py`: transition counts and probabilities
- `unseen_handler.py`: maps unseen patterns to the nearest known pattern using Levenshtein distance

What this part must support:

- PAA
- SAX
- sliding window patterns
- state extraction
- transition probability estimation
- unseen pattern handling

When this folder is used:

- after PCA reduces multivariate data to one dimension
- during automata training and inference

### `src/explainability/`

This package generates interpretable outputs for the automata model.

Files:

- `probabilistic_explainer.py`: computes path probability and confidence
- `decision_formatter.py`: formats results into required JSON or table output

What it should produce:

- current state
- current pattern
- seen/unseen status
- mapped pattern for unseen cases
- transition sequence
- transition probabilities
- total path probability
- final decision
- confidence score

When this folder is used:

- after automata inference
- during result export and reporting

### `src/evaluation/`

This package contains evaluation and statistical analysis logic.

Files:

- `metrics.py`: accuracy, precision, recall, F1-score
- `statistical_tests.py`: Wilcoxon or McNemar tests
- `validators.py`: split validation and experiment sanity checks

When this folder is used:

- after each experiment run
- before report generation

### `src/experiments/`

This package orchestrates experiment execution.

Files:

- `runner.py`: top-level experiment loop
- `skab_experiment.py`: SKAB-specific experiment flow
- `batadal_experiment.py`: BATADAL-specific experiment flow

What it should control:

- seed loop
- scenario loop
- model loop
- parameter variation loop
- saving outputs

When this folder is used:

- once loaders, preprocessing, and models are ready

### `src/utils/`

This package contains shared utilities.

Files:

- `config.py`: safe loading of YAML configuration files
- `logger.py`: logging into `outputs/logs/`
- `reproducibility.py`: random seed control

When this folder is used:

- across the whole project

### `src/main.py`

This is the project entry point.

What it should eventually do:

- load config
- choose dataset
- trigger loading and preprocessing
- run experiments
- save results

## `tests/`

This folder contains unit tests and validation tests.

What goes here:

- unseen pattern tests
- Levenshtein tests
- transition probability tests
- data loader tests
- PAA/SAX tests
- pipeline sanity tests

When it is filled:

- throughout development
- especially before final experiments

Most important required test:

- verify that unseen pattern mapping works correctly

## `outputs/`

This folder stores generated experiment outputs. It should not contain hand-written source code.

### `outputs/logs/`

Stores:

- run logs
- debug information
- execution traces

Filled when:

- experiments are executed

### `outputs/metrics/`

Stores:

- per-seed results
- per-fold results
- aggregated means and standard deviations
- comparison tables in CSV or JSON

Filled when:

- evaluation is completed

### `outputs/explainability/`

Stores:

- JSON outputs for automata decisions
- case-by-case explanation files

Filled when:

- explainability module is run

### `outputs/figures/`

Stores:

- confusion matrices
- PR or ROC curves
- automata state diagrams
- transition heatmaps
- parameter sensitivity plots

Filled when:

- visualization scripts are executed

## `notebooks/`

This folder is for exploratory work only.

What goes here:

- quick EDA
- plots for inspection
- temporary analysis

Important rule:

- final project logic should live in `src/`, not only in notebooks

## `requirements.txt`

Lists Python dependencies needed to run the project.

Expected examples:

- `pandas`
- `numpy`
- `scikit-learn`
- `tensorflow`
- `pytest`
- `pyyaml`

## `.gitignore`

Specifies which generated files should not be committed.

Usually ignored:

- cache files
- local virtual environments
- generated outputs
- optionally processed data

## Development Order

This is the recommended implementation order for the team.

### Phase 1: Data foundation

1. Finish `skab_loader.py`
2. Finish `batadal_loader.py`
3. Save merged and processed raw-ready files into `data/processed/`

### Phase 2: Safe preprocessing

1. Implement split logic
2. Implement normalization using train-only fit
3. Implement PCA using train-only fit
4. Validate that no leakage happens

### Phase 3: Deep learning baseline

1. Prepare sequence windows
2. Implement at least two deep learning models
3. Train with fixed seeds and early stopping
4. Save predictions and metrics

### Phase 4: Automata pipeline

1. Convert data to one dimension with PCA
2. Apply sliding window
3. Apply PAA
4. Apply SAX
5. Build patterns and states
6. Estimate transition probabilities
7. Run anomaly decisions

### Phase 5: Unseen pattern handling

1. Build SAX vocabulary from training data
2. Detect unseen patterns in test data
3. Map them using Levenshtein distance
4. test this behavior in `tests/`

### Phase 6: Explainability

1. Compute transition path probabilities
2. Assign confidence scores
3. Export JSON explanation outputs

### Phase 7: Evaluation and reporting

1. Run original scenario
2. Run Gaussian noise scenario
3. Run unseen scenario
4. Run parameter variation experiments
5. Aggregate results over seeds
6. Create figures
7. Write final report in Markdown

## Execution Plan

Once implementation is complete, the expected execution flow should be:

1. Prepare raw data in `data/raw/`
2. Update `configs/skab.yaml` or `configs/batadal.yaml`
3. Run the project entry point
4. Save processed data
5. Train models
6. Evaluate outputs
7. Export logs, metrics, figures, and explainability JSON files

In a mature version of the project, a teammate should be able to run something like:

```bash
python -m src.main
```

or later:

```bash
python -m src.main --dataset skab
python -m src.main --dataset batadal
```

## Data Leakage Rules

These rules are mandatory.

- Never do random row-based splitting for time series
- Fit normalization only on training data
- Apply the fitted scaler to validation and test
- Fit PCA only on training data
- Apply the fitted PCA to validation and test
- Build the SAX vocabulary only from training data
- Build automata transition probabilities only from training data

## Experiment Rules

### SKAB

- split by file groups
- use `source_file` as the grouping variable
- the same file must not appear in both train and test in the same fold

### BATADAL

- preserve time order
- split with `60% train / 20% validation / 20% test`
- do not use random row shuffling

### Fixed seeds

- `42`
- `123`
- `2026`
- `7`
- `999`

## What Is Already Present

The repository already contains:

- the full directory scaffold
- initial config files
- starter code files
- basic placeholder tests
- raw dataset files in the correct `data/raw/` structure

## What Still Needs To Be Implemented

The current codebase is a scaffold, not the final scientific implementation.

Still needed:

- full preprocessing logic
- full split logic
- actual LSTM/GRU/CNN implementations
- actual PAA/SAX implementation details
- automata training and inference logic
- explainability export logic
- real experiment runner
- complete visualizations
- final report content

## Team Handover Summary

If a teammate opens this repository for the first time, they should understand the project like this:

- `data/raw/` contains original source datasets
- `data/processed/` contains generated train/test-ready data
- `configs/` defines what experiment to run
- `src/` contains all code
- `tests/` verifies critical behavior
- `outputs/` stores generated results
- `notebooks/` is only for exploration
- `README.md` explains the plan, structure, and execution flow

This repository is organized to support a modular, reproducible, and report-friendly implementation of the course project.
