import csv
import joblib
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).parent / "data.csv"
MODEL_PATH = Path(__file__).parent / "model.pkl"

LABELS = ["billing", "technical_issue", "feature_request", "complaint", "other"]


def load_csv(path: Path) -> tuple[list[str], list[str]]:
    texts, labels = [], []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(row["label"])
    return texts, labels


texts, labels = load_csv(DATA_PATH)

# Same train-test split as in training 
_, X_test, _, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

model = joblib.load(MODEL_PATH)
y_pred = model.predict(X_test)

print(f"Test samples : {len(y_test)}")
print(f"Accuracy     : {accuracy_score(y_test, y_pred):.4f}")
print()
print(classification_report(y_test, y_pred, labels=LABELS, digits=3))
print("Confusion matrix (rows=actual, cols=predicted):")
print(f"{'':20s}", "  ".join(f"{l[:8]:>8}" for l in LABELS))
cm = confusion_matrix(y_test, y_pred, labels=LABELS)
for label, row in zip(LABELS, cm):
    print(f"{label:20s}", "  ".join(f"{v:>8}" for v in row))
