from __future__ import annotations

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def compute_classification_metrics(y_true, y_pred) -> dict[str, float]:
    y_true_list = list(y_true)
    y_pred_list = list(y_pred)

    if len(y_true_list) == 0:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
        }

    return {
        "accuracy": float(accuracy_score(y_true_list, y_pred_list)),
        "precision": float(precision_score(y_true_list, y_pred_list, zero_division=0)),
        "recall": float(recall_score(y_true_list, y_pred_list, zero_division=0)),
        "f1": float(f1_score(y_true_list, y_pred_list, zero_division=0)),
    }
