# Sinhala PDF Text Extractor

A tool for extracting text from PDF documents containing Sinhala text using OCR technology.

## Prerequisites

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y poppler-utils
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-sin
sudo apt-get install tesseract-ocr-tam

# MacOS
brew install poppler
brew install tesseract
brew install tesseract-lang
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
python pdf_extractor.py input.pdf output.txt
```

Optional: Specify languages for OCR:
```bash
python pdf_extractor.py input.pdf output.txt --languages sin eng tam
```

### Python API

```python
from pdf_extractor import PDFTextExtractor

extractor = PDFTextExtractor(languages=['sin', 'eng', 'tam'])
extractor.extract_text('input.pdf', 'output.txt')
```

## Features

- Multi-column layout support
- Automatic page segmentation
- Support for Sinhala, English, and Tamil text
- Image preprocessing for improved OCR accuracy
- Progress logging
- Error handling