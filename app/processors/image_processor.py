# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np

# class ImageProcessor:
#     def __init__(self):
#         pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path
    
#     def extract_text(self, image_path):
#         try:
#             img = cv2.imread(image_path)
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#             image = Image.fromarray(thresh)
#             return pytesseract.image_to_string(image)
#         except Exception as e:
#             raise ValueError(f"Image processing failed: {str(e)}")
import pytesseract
from PIL import Image
import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        # Configure Tesseract path (update if needed)
        self.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
        
        # Configure Tesseract parameters
        self.custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789xk×*.,₹$€'

    def preprocess_image(self, image_path):
        """Enhanced image preprocessing for better OCR"""
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Remove noise
        kernel = np.ones((2, 2), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        return Image.fromarray(processed)

    def extract_text(self, image_path):
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Perform OCR with custom configuration
            text = pytesseract.image_to_string(
                processed_img,
                config=self.custom_config,
                lang='eng'
            )
            
            # Post-process text
            clean_text = ' '.join(text.strip().split())
            return clean_text
        except Exception as e:
            raise ValueError(f"Image processing failed: {str(e)}")