# PDF Hebrew Text Decoder

This project provides tools to decode Hebrew text from specially encoded PDFs and process the extracted text for readability.

## Installation

```bash
# Install dependencies
pip install pymupdf python-bidi
```

## Key Components

- **decode_pdf.py**: Main script that extracts and decodes PDF text using character mapping
- **process_pdf.py**: Comprehensive script for PDF processing pipeline
- **text_processor.py**: Processes extracted text files with cleaning and RTL correction

## Usage

### Extracting and Decoding Pages

Edit `decode_pdf.py` to specify your input file and page range:
```python
# At the bottom of decode_pdf.py
if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Change to your PDF file
    start_page = 0              # First page to process (0-based index)
    end_page = 10               # Last page to process (0-based index)
    output_dir = "extracted_pages"

    extract_and_decode_pdf_pages(pdf_path, start_page, end_page, output_dir)
```

Then run:
```bash
python decode_pdf.py
```

### Full Processing Pipeline

Edit `process_pdf.py` to specify your input file:

```python
# At the bottom of process_pdf.py
if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Change to your PDF file
    output_file = "final_text/full_processed_text.txt"
    
    process_pdf(pdf_path, output_file)
```

Then run:
```bash
python process_pdf.py
```

## Workflow

1. **Extract** text from PDF files
2. **Decode** the text using Hebrew character mappings
3. **Clean** and process the text files
4. **Output** as readable text/markdown files
