import docx

class DocxProcessor:
    def extract_text(self, docx_path):
        try:
            doc = docx.Document(docx_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"DOCX processing failed: {str(e)}")