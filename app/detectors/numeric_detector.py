import re
from transformers import pipeline
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

class NumericDetector:
    def __init__(self):
        # Rule-based patterns
        self.patterns = [r'27000', r'27k', r'₹27000', r'\$27000', r'27,000']
        
        # ML model for contextual detection
        try:
            self.model = joblib.load('models/numeric_classifier.pkl')
            self.vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
        except:
            self.model = None
            self.vectorizer = None
    
    def detect(self, text):
        # Rule-based check
        for pattern in self.patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # ML-based check (if model exists)
        if self.model and self.vectorizer:
            X = self.vectorizer.transform([text])
            return self.model.predict(X)[0] == 1
        
        return False