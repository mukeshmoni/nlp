# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# from processors.image_processor import ImageProcessor
# from processors.pdf_processor import PDFProcessor
# from processors.docx_processor import DocxProcessor
# from detectors.numeric_detector import NumericDetector
# from detectors.math_detector import MathDetector
# from utils.file_utils import FileUtils

# app = Flask(__name__)
# app.config["UPLOAD_FOLDER"] = "uploads"
# app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "pdf", "docx"}

# # Initialize processors & detectors
# image_processor = ImageProcessor()
# pdf_processor = PDFProcessor()
# docx_processor = DocxProcessor()
# numeric_detector = NumericDetector()
# math_detector = MathDetector()

# def process_file(file_path):
#     ext = FileUtils.get_file_extension(file_path)
    
#     if ext in {"png", "jpg", "jpeg"}:
#         text = image_processor.extract_text(file_path)
#     elif ext == "pdf":
#         text = pdf_processor.extract_text(file_path)
#     elif ext == "docx":
#         text = docx_processor.extract_text(file_path)
#     else:
#         return {"error": "Unsupported file type"}
    
#     numeric_match = numeric_detector.detect(text)
#     math_match = math_detector.detect(text)
    
#     return {
#         "contains_27000": numeric_match or math_match,
#         "numeric_match": numeric_match,
#         "math_match": math_match,
#         "text": text[:500] + "..." if len(text) > 500 else text
#     }

# @app.route("/detect", methods=["POST"])
# def detect():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "No file selected"}), 400
    
#     if not FileUtils.is_allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]):
#         return jsonify({"error": "File type not allowed"}), 400
    
#     filename = secure_filename(file.filename)
#     os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
#     file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#     file.save(file_path)
    
#     result = process_file(file_path)
#     os.remove(file_path)
    
#     return jsonify(result)

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, request, jsonify, render_template, send_from_directory
# from werkzeug.utils import secure_filename
# import os

# # Initialize Flask app
# app = Flask(__name__, template_folder='templates')
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'docx'}
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# # Ensure upload folder exists
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# @app.route('/')
# def home():
#     """Render the main page"""
#     return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     """Serve favicon"""
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                            'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/api/detect', methods=['POST'])
# def detect_27000():
#     """API endpoint for file processing"""
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if not file.filename.lower().endswith(tuple(app.config['ALLOWED_EXTENSIONS'])):
#         return jsonify({'error': 'File type not allowed'}), 400
    
#     filename = secure_filename(file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(file_path)
    
#     # Here you would add your actual processing logic
#     result = {
#         'filename': filename,
#         'message': 'File uploaded successfully (processing logic would go here)'
#     }
    
#     os.remove(file_path)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from processors.image_processor import ImageProcessor
from processors.pdf_processor import PDFProcessor
from processors.docx_processor import DocxProcessor
from detectors.numeric_detector import NumericDetector
from detectors.math_detector import MathDetector

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'docx'}

# Initialize processors and detectors
image_processor = ImageProcessor()
pdf_processor = PDFProcessor()
docx_processor = DocxProcessor()
numeric_detector = NumericDetector()
math_detector = MathDetector()

def process_file(file_path):
    """Process uploaded file and detect 27000"""
    filename = secure_filename(file_path)
    ext = filename.split('.')[-1].lower()
    
    try:
        # Extract text based on file type
        if ext in {'png', 'jpg', 'jpeg'}:
            text = image_processor.extract_text(file_path)
        elif ext == 'pdf':
            text = pdf_processor.extract_text(file_path)
        elif ext == 'docx':
            text = docx_processor.extract_text(file_path)
        else:
            return {'error': 'Unsupported file type'}
        
        # Detect 27000 in extracted text
        numeric_match = numeric_detector.detect(text)
        math_match = math_detector.detect(text)
        
        return {
            'filename': filename,
            'contains_27000': numeric_match or math_match,
            'numeric_match': numeric_match,
            'math_match': math_match,
            'text': text[:500] + '...' if len(text) > 500 else text
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect_27000():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith(tuple(app.config['ALLOWED_EXTENSIONS'])):
        return jsonify({'error': 'File type not allowed'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(file_path)
    
    result = process_file(file_path)
    
    os.remove(file_path)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)