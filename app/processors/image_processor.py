import pytesseract
from PIL import Image
import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path
    
    def extract_text(self, image_path):
        try:
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            image = Image.fromarray(thresh)
            return pytesseract.image_to_string(image)
        except Exception as e:
            raise ValueError(f"Image processing failed: {str(e)}")