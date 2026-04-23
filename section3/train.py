import csv
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DATA_PATH = Path(__file__).parent / "data.csv"
MODEL_PATH = Path(__file__).parent / "model.pkl"


def load_csv(path: Path) -> tuple[list[str], list[str]]:
    texts, labels = [], []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(row["label"])
    return texts, labels


texts, labels = load_csv(DATA_PATH)

# Same train -test split used by evaluate.py
X_train, _, y_train, _ = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=10_000, sublinear_tf=True)),
    ("clf", LogisticRegression(max_iter=1000, C=5.0, solver="lbfgs", multi_class="multinomial")),
])

model.fit(X_train, y_train)
joblib.dump(model, MODEL_PATH)
print(f"Trained on {len(X_train)} samples → {MODEL_PATH}")
