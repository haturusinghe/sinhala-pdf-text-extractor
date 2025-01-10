import pdfplumber
from typing import List, Dict

class PDFExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def extract_text(self) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_pages(self) -> List[str]:
        """Extract text page by page."""
        pages = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    pages.append(page.extract_text() or "")
            return pages
        except Exception as e:
            raise Exception(f"Error extracting pages from PDF: {str(e)}")
