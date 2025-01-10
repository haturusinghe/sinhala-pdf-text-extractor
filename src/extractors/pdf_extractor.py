import fitz
import re
import logging
from typing import List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFTextExtractor:
    def __init__(self):
        # Sinhala Unicode range pattern
        self.sinhala_pattern = re.compile(r'[\u0D80-\u0DFF]+')
    
    def extract_text_from_pdf(self, pdf_path: str, output_txt_path: Optional[str] = None) -> str:
        """
        Extract text from PDF while preserving structure
        """
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            
            for page_num, page in enumerate(doc, 1):
                logger.info(f"Processing page {page_num}/{doc.page_count}")
                blocks = page.get_text("blocks")
                # Sort blocks by vertical then horizontal position
                blocks.sort(key=lambda b: (b[1], b[0]))
                
                for block in blocks:
                    full_text += block[4] + "\n"
            
            doc.close()
            
            if output_txt_path:
                self._save_text(full_text, output_txt_path)
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    def extract_sinhala_text(self, text: str) -> List[str]:
        """
        Extract only Sinhala text portions from the input text
        """
        try:
            matches = self.sinhala_pattern.finditer(text)
            return [match.group() for match in matches]
        except Exception as e:
            logger.error(f"Error extracting Sinhala text: {str(e)}")
            raise
    
    def _save_text(self, text: str, output_path: str):
        """
        Save text to file with UTF-8 encoding
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            logger.info(f"Text saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving text to file: {str(e)}")
            raise
