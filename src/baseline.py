# src/baseline.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import sys

PATH = "../data/raw.csv"

df = pd.read_csv(PATH)
X = df['text'].astype(str)
y = df['label'].astype(str)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
vec = TfidfVectorizer(ngram_range=(1,2), max_features=20000)
Xtr_t = vec.fit_transform(Xtr)
Xte_t = vec.transform(Xte)
clf = LogisticRegression(max_iter=1000, class_weight='balanced')
clf.fit(Xtr_t, ytr)
pred = clf.predict(Xte_t)
print(classification_report(yte, pred))
