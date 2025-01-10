import argparse
from src.extractors.pdf_extractor import PDFTextExtractor
import logging

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF with Sinhala support')
    parser.add_argument('--input_pdf', help='Path to input PDF file')
    parser.add_argument('--output', '-o', help='Path to output text file')
    parser.add_argument('--sinhala-only', '-s', action='store_true', 
                       help='Extract only Sinhala text')
    args = parser.parse_args()

    try:
        extractor = PDFTextExtractor()
        
        # Extract all text
        full_text = extractor.extract_text_from_pdf(args.input_pdf, args.output)
        
        # If sinhala-only flag is set, extract and save only Sinhala text
        if args.sinhala_only:
            sinhala_text = extractor.extract_sinhala_text(full_text)
            sinhala_output = args.output.replace('.txt', '_sinhala.txt') if args.output else 'sinhala_output.txt'
            with open(sinhala_output, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sinhala_text))
            logging.info(f"Sinhala text saved to {sinhala_output}")

    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
