import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input" / "pdfs"
OUTPUT_DIR = DATA_DIR / "output"
RAW_OUTPUT_DIR = OUTPUT_DIR / "raw"
PROCESSED_OUTPUT_DIR = OUTPUT_DIR / "processed"

# Create directories if they don't exist
for dir_path in [INPUT_DIR, RAW_OUTPUT_DIR, PROCESSED_OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# PDF processing settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
SUPPORTED_FORMATS = ['.pdf']

# Language settings
DEFAULT_ENCODING = 'utf-8'
SUPPORTED_LANGUAGES = ['si', 'en']  # si: Sinhala, en: English
