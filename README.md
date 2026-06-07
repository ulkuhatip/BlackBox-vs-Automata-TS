# BlackBox-vs-Automata-TS

**Software Development - Project 2**  
**Group 09**  
**Black-Box vs Explainable Time-Series Analysis**

---

## 1. About the Project

This project compares two different modeling paradigms for time-series anomaly detection:

- **Black-box models:** LSTM, GRU, 1D-CNN
- **Explainable model:** Probabilistic Automata

The main goal is not to identify a single universal winner, but to analyze how different model families behave under:

- original data
- Gaussian noise
- unseen pattern conditions
- different automata parameter settings

### Datasets

| Dataset | Source | Data Type | Split Strategy |
|---------|--------|-----------|----------------|
| **SKAB** | `valve1` + `valve2` | Industrial sensor time series | Group-based 5-fold split by `source_file` |
| **BATADAL** | `BATADAL_dataset04.csv` | Water distribution anomaly/attack data | Temporal `60/20/20` split |

---

## 2. Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Dataset Locations

```text
data/raw/skab/valve1/
data/raw/skab/valve2/
data/raw/batadal/BATADAL_dataset04.csv
```

---

## 3. Usage

Run the main project entry point:

```bash
python -m src.main
```

Generate the report figures:

```bash
.\.venv\Scripts\python.exe -m src.generate_report_figures --dataset all --scenario all --window-size 6 --alphabet-size 5 --skab-fold 1
```

Run tests:

```bash
pytest tests/ -v
```

---

## 4. Project Structure

```text
BlackBox-vs-Automata-TS/
├── configs/
├── data/
├── notebooks/
├── outputs/
├── results/
├── src/
│   ├── data/
│   ├── evaluation/
│   ├── experiments/
│   ├── explainability/
│   ├── features/
│   ├── models/
│   │   ├── automata/
│   │   └── deep_learning/
│   └── utils/
└── tests/
```

---

## 5. Experimental Results

### Table 1: Model Performance and Stability (Mean F1-score +- Standard Deviation)

*Final setting: `window_size=6`, `alphabet_size=5`.*  
*SKAB values are averaged over 5 folds. BATADAL values come from a single time-ordered split.*

| Model | SKAB F1 | BATADAL F1 |
|-------|---------|------------|
| LSTM | 0.3892 +- 0.0991 | 0.1567 +- 0.0000 |
| GRU | 0.0000 +- 0.0000 | 0.3265 +- 0.0000 |
| 1D-CNN | 0.3651 +- 0.1584 | 0.1644 +- 0.0000 |
| Automata | 0.3409 +- 0.0736 | 0.0979 +- 0.0000 |

### Table 2: Noise Impact and Unseen Scenario Analysis (SKAB)

| Model | Original F1 | Noisy F1 | Unseen Detection Rate | Unseen Accuracy |
|-------|-------------|----------|-----------------------|-----------------|
| LSTM | 0.3892 | 0.3823 | 0.5190 | 0.5037 |
| GRU | 0.0000 | 0.0231 | 0.0000 | 0.6492 |
| 1D-CNN | 0.3651 | 0.2666 | 0.4766 | 0.5050 |
| Automata | 0.3409 | 0.2954 | 0.5585 | 0.4394 |

### Table 3: Cross-Dataset Performance Comparison

Cross-dataset training/testing experiments were **not executed** in the current project artifacts, so the table can only be marked as not available.

| Train / Test | SKAB | BATADAL |
|--------------|------|---------|
| Train: SKAB | within-dataset only | N/A |
| Train: BATADAL | N/A | within-dataset only |

### Table 4: Automata Parameter Sensitivity Analysis (SKAB Unseen F1-score)

#### 4a. Window Size Effect (`alphabet_size = 5`)

| Window Size | 3 | 4 | 5 | 6 |
|-------------|---|---|---|---|
| **Unseen F1** | 0.3131 | 0.3368 | 0.3771 | 0.4078 |

#### 4b. Alphabet Size Effect (`window_size = 6`)

| Alphabet Size | 3 | 4 | 5 | 6 |
|---------------|---|---|---|---|
| **Unseen F1** | 0.2874 | 0.3719 | 0.4078 | 0.4560 |

### Table 5: Runtime Comparison

Runtime values are **not explicitly logged** in the current saved artifacts.

| Model | Training Time (s) | Inference Time (s) |
|-------|-------------------|--------------------|
| LSTM | N/A | N/A |
| GRU | N/A | N/A |
| 1D-CNN | N/A | N/A |
| Automata | N/A | N/A |

### Summary

- On **SKAB**, `LSTM` is the most balanced model under original and noisy conditions.
- On **SKAB unseen**, `Automata` achieves the strongest recall and the best F1 among meaningful anomaly detectors.
- On **BATADAL**, `GRU` is the strongest overall model according to F1.
- `GRU` on SKAB shows why accuracy alone is misleading in imbalanced anomaly detection.

---

## 6. Required Figures

The figures below were selected as the minimum required visual set for the report.  
For consistency, all four model-behavior figures use the same representative setting:

- dataset: `SKAB`
- scenario: `unseen`
- `window_size = 6`
- `alphabet_size = 5`
- `fold = 1`

### Confusion Matrix

![Confusion Matrix](outputs/figures/report/skab/unseen/skab_unseen_w6_a5_fold1_confusion_matrix.png)

### Precision-Recall Curve

![Precision-Recall Curve](outputs/figures/report/skab/unseen/skab_unseen_w6_a5_fold1_precision_recall_curve.png)

### Automata State Diagram

![Automata State Diagram](outputs/figures/report/skab/unseen/skab_unseen_w6_a5_fold1_state_diagram.png)

### Transition Probability Heatmap

![Transition Probability Heatmap](outputs/figures/report/skab/unseen/skab_unseen_w6_a5_fold1_transition_heatmap.png)

### Parameter Sensitivity Plot

This heatmap shows how automata `F1` in the `unseen` scenario changes with window size and alphabet size.

![Parameter Sensitivity Heatmap](outputs/figures/report/skab/parameter_sensitivity/skab_unseen_automata_f1_heatmap.png)

---

## 7. Explainability Module

For the automata model, the decision process can be explained through:

- current symbolic pattern
- seen/unseen status
- mapped pattern for unseen cases
- transition probability
- full path probability
- anomaly decision

This makes the automata pipeline suitable not only for anomaly detection, but also for interpretable analysis of symbolic temporal behavior.

---

## 8. Statistical and Methodological Notes

- `SKAB` uses a group-based split by `source_file`, which helps reduce leakage across file boundaries.
- `BATADAL` uses a time-ordered split, which is more realistic for temporal anomaly detection.
- `SKAB` results contain fold-level variability, while `BATADAL` results do not include fold-based standard deviation because only one temporal split is used.
- `Cross-dataset` generalization is not available in the current saved project results.

---

## 9. Final Interpretation

This project shows that there is no single model that dominates across all conditions.

- `LSTM` is the most balanced option on `SKAB` under standard conditions.
- `Automata` is especially valuable when unseen symbolic behavior must be detected and interpreted.
- `GRU` is strongest on `BATADAL`, but unreliable on `SKAB` despite its high accuracy.

The main takeaway is therefore not a ranking, but a scientific observation: black-box and explainable models offer different strengths under different data conditions, and meaningful comparison requires scenario-based, metric-based, and parameter-based analysis.
