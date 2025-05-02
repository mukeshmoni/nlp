import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Sample training data (replace with real data)
data = [
    ("This document contains 27000", 1),
    ("The value is 27k", 1),
    ("Total: ₹27000", 1),
    ("Price is 28000", 0),
    ("9x3000 equals 27000", 1),
    ("300x90 is the calculation", 1),
    ("100*270 appears here", 1),
    ("8x3375 is not relevant", 0)
]

df = pd.DataFrame(data, columns=["text", "label"])

# Feature extraction
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save models
joblib.dump(model, "models/numeric_classifier.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")