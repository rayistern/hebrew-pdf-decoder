import fitz  # PyMuPDF
import os
from datetime import datetime
import pathlib

# Import the mapping function from decode_pdf.py
from decode_pdf import create_hebrew_mapping

def extract_text_from_pdf(pdf_path, page_number):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Check if the page number is valid
    if page_number < 0 or page_number >= len(doc):
        print(f"Error: Page {page_number + 1} does not exist. PDF has {len(doc)} pages.")
        doc.close()
        return None
    
    # Get the specified page
    page = doc[page_number]
    
    # Extract text with options for better Hebrew support
    text = page.get_text("text", flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE)
    
    # Close the document
    doc.close()
    
    return text

def get_output_filename(pdf_path, page_num):
    # Get PDF filename without extension
    pdf_name = pathlib.Path(pdf_path).stem
    
    # Create timestamp with current time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create output directory if it doesn't exist
    output_dir = "decoded_pages"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename: timestamp_pdfname_pageXXX.txt
    filename = f"{timestamp}_{pdf_name}_page{page_num+1:03d}.txt"
    
    return os.path.join(output_dir, filename)

def print_character_codes(text, mapping, output_file):
    # Print each character with its Unicode code point and mapped character
    for idx, char in enumerate(text):
        code_point = ord(char)
        mapped_char = mapping.get(char, char)
        output_file.write(f"{idx + 1}| Character: {repr(char)} | Code: {code_point} | Mapped: {repr(mapped_char)}\n")

# Main execution
if __name__ == "__main__":
    pdf_path = "lh1.pdf"  # Path to your PDF file
    page_number = 27     # Page number (0-based index)
    
    # Extract text from the specified page
    text = extract_text_from_pdf(pdf_path, page_number)
    
    if text is not None:
        # Get the mapping
        mapping = create_hebrew_mapping()
        
        # Get output filename
        output_path = get_output_filename(pdf_path, page_number)
        
        # Write output to file
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(f"--- Page {page_number + 1} ---\n")
            print_character_codes(text, mapping, out_file)
        
        print(f"Character codes and mappings have been saved to {output_path}")
    else:
        print("Failed to extract text from the PDF.")