# src/
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

PATH = "../data/raw.csv"

df = pd.read_csv(PATH)
X = df['text'].astype(str)
y = df['label'].astype(str)

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train vectorizer + model
vec = TfidfVectorizer(ngram_range=(1,2), max_features=20000)
Xtr_t = vec.fit_transform(Xtr)
clf = LogisticRegression(max_iter=1000, class_weight="balanced")
clf.fit(Xtr_t, ytr)

# Save artifacts
joblib.dump(vec, "../models/vectorizer.joblib")
joblib.dump(clf, "../models/model.joblib")

print("✅ Model and vectorizer saved in ../models/")
