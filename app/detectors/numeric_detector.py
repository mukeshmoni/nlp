# import re
# from transformers import pipeline
# import joblib
# from sklearn.feature_extraction.text import TfidfVectorizer

# class NumericDetector:
#     def __init__(self):
#         # Rule-based patterns
#         self.patterns = [r'27000', r'27k', r'₹27000', r'\$27000', r'27,000']
        
#         # ML model for contextual detection
#         try:
#             self.model = joblib.load('models/numeric_classifier.pkl')
#             self.vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
#         except:
#             self.model = None
#             self.vectorizer = None
    
#     def detect(self, text):
#         # Rule-based check
#         for pattern in self.patterns:
#             if re.search(pattern, text, re.IGNORECASE):
#                 return True
        
#         # ML-based check (if model exists)
#         if self.model and self.vectorizer:
#             X = self.vectorizer.transform([text])
#             return self.model.predict(X)[0] == 1
        
#         return False
import re

class NumericDetector:
    def __init__(self):
        self.patterns = [
            r'\b27000\b',          # Exact match
            r'\b27\s?k\b',         # 27k
            r'₹\s?27000',          # ₹27000
            r'\$\s?27000',         # $27000
            r'\b27[,.]?000\b',     # 27,000 or 27.000
            r'\b27\s?000\b',       # 27 000
            r'27\s?thousand',      # 27 thousand
            r'27\s?grand'          # 27 grand
        ]

    def detect(self, text):
        """Enhanced detection with fuzzy matching"""
        text = text.lower().replace(',', '').replace(' ', '')
        
        # Check for direct matches
        for pattern in self.patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Check for number proximity (e.g., 26999-27001)
        numbers = re.findall(r'\d+', text)
        for num in numbers:
            try:
                if 26999 <= int(num) <= 27001:
                    return True
            except ValueError:
                continue
                
        return False