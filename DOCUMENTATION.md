# PDF Hebrew Text Decoder - Complete Documentation

## Overview

This project provides a comprehensive toolkit for extracting, decoding, and processing Hebrew text from specially encoded PDFs. The system handles PDFs where Hebrew characters are encoded with non-standard mappings, corrects text direction, and processes the output into readable format.

## Installation

### Requirements

- Python 3.6 or higher
- PyMuPDF (fitz)
- python-bidi
- PyPDF2 (optional, for some utilities)

### Setup

```bash
# Install required dependencies
pip install pymupdf python-bidi pypdf2
```

## Files and Components

### Core Components

#### decode_pdf.py
Main module for extracting and decoding PDF text.

- `create_hebrew_mapping()`: Creates a dictionary mapping garbled characters to proper Hebrew.
- `decode_text()`: Applies character mapping to convert text.
- `extract_and_decode_pdf_pages()`: Extracts text from PDF page range and decodes it.
- `extract_text_from_page()`: Handles text extraction with block positioning.

#### process_pdf.py
Comprehensive PDF processing pipeline.

- `extract_text_from_pdf()`: Extracts all text from a PDF.
- `clean_text()`: Removes artifacts like page numbers, hyphenation.
- `correct_text_direction()`: Fixes RTL text rendering.
- `process_pdf()`: Complete pipeline from PDF to processed text.

#### text_processor.py
Processes extracted text files.

- `process_text_files()`: Batch processes extracted text files.
- `clean_text()`: Similar to the one in process_pdf.py but for files.
- `correct_text_direction()`: Applies RTL correction to text.

### Utility Components

#### extract_char_code.py
Utility to analyze character codes in garbled text.

#### remove_linebreaks_quotes.py
Fixes linebreaks around quotes in processed text.

- `remove_linebreaks_around_quotes()`: Processes a directory of files.
- `remove_linebreaks_around_double_quotes()`: Core function for removing breaks.

#### remove_page_numbers.py
Removes page numbers from processed files.

- `remove_page_numbers()`: Removes page numbers based on pattern matching.

#### test.py
Tests PDF decoding functionality on specific pages.

- `extract_text_from_pdf()`: Extracts text from a specific page.
- `print_character_codes()`: Prints character codes and their mappings.

#### pdf_reader.py and pdf.py
Alternative PDF reading implementations.

## Character Mapping

The system uses an extensive mapping table (`create_hebrew_mapping()` function) to convert garbled characters to proper Hebrew. The mapping includes:

- Basic Hebrew letters
- Final Hebrew letters
- Punctuation and special characters
- Numbers

If you encounter unmapped characters, they'll be reported in the console and maintained in the output.

## Workflow

1. **Extraction**: PDF text is extracted page by page with PyMuPDF
2. **Decoding**: Extracted text is decoded using the Hebrew character mapping
3. **Cleaning**: Text artifacts are removed (page numbers, line breaks, etc.)
4. **Direction Correction**: RTL text direction is applied for Hebrew
5. **Processing**: Further text processing (quotes, line breaks)
6. **Output**: Final text is saved as plain text or markdown

## Detailed Usage

### 1. Extracting and Decoding PDF Pages

For basic extraction and decoding of a page range:

```python
# Edit decode_pdf.py
if __name__ == "__main__":
    pdf_path = "your_document.pdf"  # Path to your PDF
    start_page = 0                  # First page (0-indexed)
    end_page = 20                   # Last page (0-indexed)
    output_dir = "extracted_pages"  # Output directory
    
    extract_and_decode_pdf_pages(pdf_path, start_page, end_page, output_dir)
```

Run:
```bash
python decode_pdf.py
```

Output will be saved as timestamped text files in the specified output directory.

### 2. Full PDF Processing

For complete processing of a PDF:

```python
# Edit process_pdf.py
if __name__ == "__main__":
    pdf_path = "your_document.pdf"                      # Path to your PDF
    output_file = "final_text/full_processed_text.txt"  # Output file
    
    process_pdf(pdf_path, output_file)
```

Run:
```bash
python process_pdf.py
```

### 3. Post-Processing Text Files

Process already extracted text files:

```bash
# Clean up text files
python text_processor.py

# Remove linebreaks around quotes
python remove_linebreaks_quotes.py

# Remove page numbers
python remove_page_numbers.py
```

### 4. Testing Specific Pages

To test extraction and mapping on a specific page:

```python
# Edit test.py
if __name__ == "__main__":
    pdf_path = "your_document.pdf"  # Path to your PDF
    page_number = 5                # Page to test (0-indexed)
    
    # Rest of the code remains unchanged
```

Run:
```bash
python test.py
```

## Directory Structure

The project creates the following directory structure:

```
/
├── extracted_pages/     # Raw extracted text
├── extracted_pages/done/  # Processed raw files
├── input_files/         # Processed text files
├── processed_files/     # Files after first processing
├── final_files/         # Final output files
└── final_text/          # Complete processed documents
```

## Advanced Configuration

### Customizing Character Mapping

The mapping is defined in `create_hebrew_mapping()` in decode_pdf.py. You can add or modify mappings:

```python
def create_hebrew_mapping():
    mapping = {
        # Existing mappings...
        
        # Add your custom mappings
        'ñ': 'נ',  # Example: Map 'ñ' to Hebrew letter nun
    }
    return mapping
```

### Customizing Text Cleaning

Text cleaning rules are defined in `clean_text()` in process_pdf.py and text_processor.py:

```python
def clean_text(text):
    # Existing cleaning rules...
    
    # Add custom cleaning rules
    text = re.sub(r'your_pattern', 'replacement', text)
    
    return text
```

## Troubleshooting

### Missing Character Mappings

If you see "Missing mappings for: [characters]" in the output:

1. Note the missing characters
2. Find their Unicode code points using extract_char_code.py
3. Add them to the mapping in create_hebrew_mapping()

### Text Direction Issues

If Hebrew text displays incorrectly:

1. Check that python-bidi is installed
2. Verify the `correct_text_direction()` function is being called
3. Try adding explicit RTL marks: `'\u200F' + your_text`

### Block Ordering Issues

If text blocks appear out of order:

1. Modify the sorting key in `extract_text_from_page()`:
   ```python
   # For RTL documents, try sorting by y-coordinate first, then x-coordinate in reverse
   blocks.sort(key=lambda b: (b[1], -b[0]))
   ```

### Performance Issues with Large PDFs

For large PDFs:

1. Process the PDF in smaller page ranges
2. Use parallel processing for multiple ranges simultaneously
3. Consider memory-efficient options in PyMuPDF

## Command-Line Tools

For batch processing, you can add command-line arguments:

```python
# Example for decode_pdf.py
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and decode PDF pages')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--start', type=int, default=0, help='Starting page (0-indexed)')
    parser.add_argument('--end', type=int, help='Ending page (0-indexed)')
    parser.add_argument('--output', default='extracted_pages', help='Output directory')
    
    args = parser.parse_args()
    
    end_page = args.end if args.end is not None else len(fitz.open(args.pdf_path)) - 1
    extract_and_decode_pdf_pages(args.pdf_path, args.start, end_page, args.output)
```

Then run:
```bash
python decode_pdf.py your_document.pdf --start 5 --end 10 --output my_pages
``` 