#!/bin/bash

# Loop through pages 1 to 10
for i in {1..10}
do
    echo "Processing page $i..."
    python pdf_extractor.py --input_dir "data/scraped_hansards/page_$i" --output_dir data/extracted
done
