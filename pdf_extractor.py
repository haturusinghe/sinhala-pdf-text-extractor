from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
import logging
from pathlib import Path
import shutil
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required system dependencies are installed"""
    if not shutil.which('pdfinfo'):
        sys.exit("""
Error: poppler-utils is not installed. 
Please install it using:
    Ubuntu/Debian: sudo apt-get install poppler-utils
    MacOS: brew install poppler
""")
    
    if not shutil.which('tesseract'):
        sys.exit("""
Error: tesseract is not installed. 
Please install it using:
    Ubuntu/Debian: sudo apt-get install tesseract-ocr
    MacOS: brew install tesseract
""")

class PDFTextExtractor:
    def __init__(self, languages=['sin', 'eng', 'tam']):
        check_dependencies()
        self.languages = '+'.join(languages)
        self.custom_config = f'--psm 1 --oem 3 -l {self.languages}'

    def preprocess_image(self, image):
        """Apply image preprocessing for better OCR results"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def extract_text(self, pdf_path, output_path):
        """Extract text from PDF using OCR"""
        try:
            pages = convert_from_path(pdf_path)
            full_text = ""
            
            for page_num, page_image in enumerate(pages, 1):
                logger.info(f"Processing page {page_num}")
                
                # Convert PIL image to OpenCV format
                image = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
                
                # Preprocess image
                binary = self.preprocess_image(image)
                
                # Perform OCR
                text = pytesseract.image_to_string(binary, config=self.custom_config)
                full_text += f"\n--- Page {page_num} ---\n{text}\n"
            
            # Save extracted text
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
                
            logger.info(f"Text extraction completed. Saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error during extraction: {str(e)}")
            raise

if __name__ == "__main__":
    import argparse
    
    check_dependencies()
    
    parser = argparse.ArgumentParser(description='Extract text from PDF using OCR')
    parser.add_argument('--input_pdf', help='Path to the input PDF file')
    parser.add_argument('--output', help='Path to save the extracted text')
    parser.add_argument('--languages', nargs='+', default=['sin', 'eng', 'tam'],
                        help='Languages to use for OCR (default: sin eng tam)')
    
    args = parser.parse_args()
    
    extractor = PDFTextExtractor(languages=args.languages)
    extractor.extract_text(args.input_pdf, args.output)
