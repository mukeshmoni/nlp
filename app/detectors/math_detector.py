# import re
# from asteval import Interpreter
# import joblib
# from sklearn.feature_extraction.text import TfidfVectorizer

# class MathDetector:
#     def __init__(self):
#         self.aeval = Interpreter()
#         self.math_expr_pattern = re.compile(r'(\d+[x×*]\d+)')
        
#         # ML model for math expressions
#         try:
#             self.model = joblib.load('models/math_classifier.pkl')
#             self.vectorizer = joblib.load('models/math_vectorizer.pkl')
#         except:
#             self.model = None
#             self.vectorizer = None
    
#     def detect(self, text):
#         # Find all math expressions
#         matches = self.math_expr_pattern.findall(text.lower())
        
#         for expr in matches:
#             # Rule-based evaluation
#             expr_clean = expr.replace('x', '*').replace('×', '*')
#             try:
#                 if self.aeval(expr_clean) == 27000:
#                     return True
#             except:
#                 continue
            
#             # ML-based check (if model exists)
#             if self.model and self.vectorizer:
#                 X = self.vectorizer.transform([expr])
#                 if self.model.predict(X)[0] == 1:
#                     return True
        
#         return False
# # app/detectors/math_detector.py
# import re
# import operator

# class MathDetector:
#     def __init__(self):
#         self.math_expr_pattern = re.compile(r'(\d+[x×*]\d+)')
#         self.allowed_operators = {
#             '*': operator.mul,
#             'x': operator.mul,
#             '×': operator.mul
#         }
    
#     def safe_eval(self, expr):
#         try:
#             # Replace different multiplication symbols
#             expr = expr.lower().replace(' ', '')
#             for symbol, op in self.allowed_operators.items():
#                 expr = expr.replace(symbol, '*')
            
#             # Simple evaluation without using eval()
#             parts = expr.split('*')
#             if len(parts) != 2:
#                 return None
#             a, b = map(float, parts)
#             return a * b
#         except:
#             return None
    
#     def detect(self, text):
#         matches = self.math_expr_pattern.findall(text.lower())
#         for expr in matches:
#             result = self.safe_eval(expr)
#             if result == 27000:
#                 return True
#         return False
import re
import numpy as np
from typing import Optional

class MathDetector:
    def __init__(self):
        self.math_expr_pattern = re.compile(r'(\d+[x×*]\d+)')
        try:
            from asteval import Interpreter
            self.aeval = Interpreter()
            self.use_asteval = True
        except ImportError:
            self.use_asteval = False
    
    def safe_eval(self, expr: str) -> Optional[float]:
        """Safely evaluate mathematical expression"""
        try:
            # Standardize multiplication symbols
            expr = expr.replace('x', '*').replace('×', '*')
            
            if self.use_asteval:
                return self.aeval(expr)
            else:
                # Fallback using numpy
                return float(np.prod([float(x) for x in expr.split('*')]))
        except:
            return None
    
    def detect(self, text: str) -> bool:
        """Check if text contains math expressions that equal 27000"""
        matches = self.math_expr_pattern.findall(text.lower())
        for expr in matches:
            result = self.safe_eval(expr)
            if result == 27000:
                return True
        return False