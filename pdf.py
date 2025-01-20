import fitz  # pymupdf

def read_specific_page(pdf_path, page_num):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    if page_num < 0 or page_num >= len(doc):
        print(f"Error: Page {page_num} does not exist. PDF has {len(doc)} pages.")
        return
    
    try:
        page = doc[page_num]
        # Get text with specific parameters for better RTL/Hebrew support
        text = page.get_text("text", flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE)
        print(f"Page {page_num + 1}")
        try:
            # Try to properly encode/decode the text
            print(text.encode('utf-8').decode('utf-8'))
        except UnicodeError:
            # Fallback if encoding fails
            print("Original text (possibly encoded):", text)
    finally:
        doc.close()

if __name__ == "__main__":
    pdf_path = './lh1.pdf'
    page_to_read = 24  # Specify the page number here (0-based index for page 25)
    read_specific_page(pdf_path, page_to_read)
