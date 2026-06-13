import pandas as pd


def evaluate_model(predictions, labels_path):
    """
    predictions: list of detected alert user_ids or event ids
    labels_path: path to data_access_labels.csv
    """

    labels = pd.read_csv(labels_path)

    labels.columns = labels.columns.str.strip().str.lower()

    # Assuming label column = is_anomaly (1/0)
    true_labels = labels["is_anomaly"]

    # Convert predictions into binary list
    pred_set = set(predictions)

    y_pred = []
    y_true = []

    for idx, row in labels.iterrows():
        event_id = row.get("access_id", idx)

        y_true.append(1 if row["is_anomaly"] == 1 else 0)

        if event_id in pred_set:
            y_pred.append(1)
        else:
            y_pred.append(0)

    # Calculate metrics
    TP = sum((p == 1 and t == 1) for p, t in zip(y_pred, y_true))
    FP = sum((p == 1 and t == 0) for p, t in zip(y_pred, y_true))
    FN = sum((p == 0 and t == 1) for p, t in zip(y_pred, y_true))

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0
    )

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1, 3),
        "TP": TP,
        "FP": FP,
        "FN": FN
    }