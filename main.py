import argparse
from pathlib import Path
from src.extractors.pdf_extractor import PDFExtractor
from src.processors.unicode_handler import UnicodeHandler

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF files with Sinhala support')
    parser.add_argument('input_file', type=str, help='Path to the input PDF file')
    parser.add_argument('--output', type=str, help='Path to the output text file', default=None)
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = PDFExtractor(args.input_file)
        
        # Extract text
        text = extractor.extract_text()
        
        # Process text
        unicode_handler = UnicodeHandler()
        processed_text = unicode_handler.clean_text(text)
        
        # Handle output
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)
            print(f"Text extracted and saved to {args.output}")
        else:
            print(processed_text)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
