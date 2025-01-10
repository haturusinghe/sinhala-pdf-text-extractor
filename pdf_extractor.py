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
            
            logger.info(f"Processing {pdf_path}")
            
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

    def process_directory(self, input_dir, output_dir):
        """Process all PDF files in the input directory"""
        output_dir = input_dir.split('/')[-1]
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.is_dir():
            raise ValueError(f"Input path {input_dir} is not a directory")
        
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        pdf_files = list(input_path.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {input_dir}")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            output_file = output_path / f"{pdf_file.stem}.txt"
            try:
                self.extract_text(pdf_file, output_file)
            except Exception as e:
                logger.error(f"Failed to process {pdf_file}: {str(e)}")
                continue

if __name__ == "__main__":
    import argparse
    
    check_dependencies()
    
    parser = argparse.ArgumentParser(description='Extract text from PDF files using OCR')
    parser.add_argument('--input_dir', required=True, help='Directory containing PDF files')
    parser.add_argument('--output_dir', required=True, help='Directory to save the extracted text files')
    parser.add_argument('--languages', nargs='+', default=['sin', 'eng', 'tam'],
                        help='Languages to use for OCR (default: sin eng tam)')
    
    args = parser.parse_args()
    
    extractor = PDFTextExtractor(languages=args.languages)
    extractor.process_directory(args.input_dir, args.output_dir)
