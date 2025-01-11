# Sinhala PDF Text Extractor

A tool for extracting Sinhala text from PDF documents with a focus on Hansard parliamentary reports.

## Components

### 1. PDF Text Extractor (`pdf_extractor.py`)

A Python script that extracts text from PDF files containing Sinhala text. It uses various PDF parsing libraries to handle different PDF formats and encoding.

Features:
- Supports multiple PDF text extraction methods
- Handles Sinhala Unicode text properly
- Removes unwanted characters and formatting
- Saves extracted text to output files

Usage:
```bash
python pdf_extractor.py <input_pdf_path> <output_text_path>
```

### 2. Hansard PDF Scraper (`scrape_hansards_pdfs.py`)

A script specifically designed to download Hansard PDFs from the Parliament of Sri Lanka website.

Features:
- Scrapes PDF links from the parliament website
- Downloads Hansard PDFs automatically
- Organizes downloaded files by date
- Handles network errors and retries

Usage:
```bash
python scrape_hansards_pdfs.py
```

## Requirements

- Python 3.x
- pdfplumber
- PyPDF2
- requests
- beautifulsoup4

## Installation

1. Clone this repository:
```bash
git clone https://github.com/haturusinghe/sinhala-pdf-text-extractor.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```
