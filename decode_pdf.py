import fitz  # PyMuPDF
import os
from datetime import datetime
import pathlib
import re
from bidi.algorithm import get_display  # Import get_display from python-bidi

def create_hebrew_mapping():
    mapping = {
        # Basic Hebrew letters
        'ô': 'פ',    # U+00F4 to U+05E4
        'ú': 'ת',    # U+00FA to U+05EA
        'ç': 'ח',    # U+00E7 to U+05D7
        'ã': 'ד',    # U+00E3 to U+05D3
        'á': 'ב',    # U+00E1 to U+05D1
        'ø': 'ר',    # U+00F8 to U+05E8
        '˜': 'ק',    # U+02DC to U+05E7
        '˘': 'ש',    # U+02D8 to U+05E9
        'Ú': 'ע',    # U+00DA to U+05E2
        'Ì': 'ם',    # U+00CC to U+05DD
        'È': 'י',    # U+00C8 to U+05D9
        'Â': 'ו',    # U+00C2 to U+05D5
        '‰': 'ה',    # U+2030 to U+05D4
        'ä': 'ה',    # U+00E4 to U+05D4
        'â': 'ג',    # manual by Rayi
        'ı': 'ץ',    # manual by Rayi
        'Z': '—',    # manual by Rayi
        'Û': 'ף',    # manual by Rayi
        'ê': 'ך',    # manual by Rayi
        't': 'ַ',    # manual by Rayi
        'î': 'מ',    # U+00EE to U+05DE
        'ù': 'ש',    # U+00F9 to U+05E9
        'é': 'י',    # U+00E9 to U+05D9
        'è': 'ט',    # U+00E8 to U+05D8
        'ì': 'ל',    # U+00EC to U+05DC
        'ë': 'כ',    # U+00EB to U+05DB
        'à': 'א',    # U+00E0 to U+05D0
        'Ù': 'פ',    # U+00D9 to U+05E4
        '˙': 'ת',    # U+02D9 to U+05EA
        '„': 'ד',    # U+201E to U+05D3
        'Ë': 'ט',
        '‚': 'ג',
        'Ó': 'מ',    # U+00D3 to U+05DE
        'Á': 'ח',    # U+00C1 to U+05D7
        'Î': 'כ',    # U+00CE to U+05DB
        'Ê': 'ז',    # U+00CA to U+05D6
        '¯': 'ר',    # U+00AF to U+05E8
        '‡': 'א',    # U+2021 to U+05D0
        'Ï': 'ל',    # U+00CF to U+05DC
        'Í': 'ך',    # U+00CD to U+05DA
        'Ò': 'ס',    # U+00D2 to U+05E1
        'ˆ': 'צ',    # U+02C6 to U+05E6

        # Additional mappings based on the provided documents
        'Ô': 'ן',    # U+00D4 to U+05E2 edited by Rayi, caps
        '': 'נ',    # U+F8FF to U+05E0
        '·': 'ב',    # U+00B7 to U+05D1
        #'‚': ',',    # U+201A to U+002C removed this, because we want to have comma 44 map to comma, and comma 8218 map to gimmel
        '…': '...',  # U+2026 to '...'
        'æ': 'ז',    # U+00E6 to U+05D6
        'ö': 'ט',    # U+00F6 to U+05D8
        '÷': 'ת',    # U+00F7 to U+05EA
        'û': 'ת',    # U+00FB to U+05EA
        'ü': 'ש',    # U+00FC to U+05E9
        'þ': 'ת',    # U+00FE to U+05EA
        'ÿ': 'ף',    # U+00FF to U+05E3
        'œ': 'פ',    # U+0153 to U+05E4
        'Œ': 'פ',    # U+0152 to U+05E4
        'š': 'ט',    # U+0161 to U+05D8
        'Š': 'ט',    # U+0160 to U+05D8
        'Ÿ': 'ף',    # U+0178 to U+05E3
        'ž': 'צ',    # U+017E to U+05E6
        'Ž': 'צ',    # U+017D to U+05E6
        'Ð': 'ד',    # U+00D0 to U+05D3
        'Ñ': 'נ',    # U+00D1 to U+05E0
        'Õ': 'ץ',    # U+00D5 to U+05E5
        'Ø': '×',    # U+00D8 to U+00D7
        'Ý': 'י',    # U+00DD to U+05D9
        'Þ': 'ת',    # U+00DE to U+05EA
        'ß': 'ס',    # U+00DF to U+05E1
        'ð': 'נ',    # U+00F0 to U+05E0 (corrected from final nun ן to regular nun נ)
        'å': 'ו',    # U+00E5 to U+05D5
        'ì': 'ל',    # U+00EC to U+05DC
        'í': 'ם',    # U+00ED to U+05DD
        'î': 'מ',    # U+00EE to U+05DE
        'ï': 'ן',    # U+00EF to U+05DF
        'ñ': 'ס',    # U+00F1 to U+05E1
        'ò': 'ע',    # U+00F2 to U+05E2
        'ó': 'פ',    # U+00F3 to U+05E4
        'ô': 'פ',    # U+00F4 to U+05E6
        'õ': 'ץ',    # U+00F5 to U+05E5
        'ö': 'צ',    # U+00F6 to U+05E7
        '÷': 'ק',    # U+00F7 to U+05E8
        'ø': 'ר',    # U+00F8 to U+05E9
        'ù': 'ש',    # U+00F9 to U+05E9
        'ú': 'ת',    # U+00FA to U+05EA

        # Punctuation and numbers
        '|': '|',      # U+007C to U+007C
        '-': '-',      # U+002D to U+002D
        '–': '-',      # U+2013 to U+002D
        '—': '-',      # U+2014 to U+002D
        ',': ',',      # U+002C to U+002C
        '.': '.',      # U+002E to U+002E
        '(': '(',      # U+0028 to U+0028
        ')': ')',      # U+0029 to U+0029
        '[': '[',      # U+005B to U+005B
        ']': ']',      # U+005D to U+005D
        '"': '"',      # U+0022 to U+0022
        "'": "'",      # U+0027 to U+0027
        '“': '"',      # U+201C to U+0022
        '”': '"',      # U+201D to U+0022
        '‘': "'",      # U+2018 to U+0027
        '’': "'",      # U+2019 to U+0027
        '«': '"',      # U+00AB to U+0022
        '»': '"',      # U+00BB to U+0022
        '‹': "'",      # U+2039 to U+0027
        '›': "'",      # U+203A to U+0027
        '₪': '₪',     # U+20AA to U+20AA

        # Numbers
        '0': '0',    # U+0030 to U+0030
        '1': '1',    # U+0031 to U+0031
        '2': '2',    # U+0032 to U+0032
        '3': '3',    # U+0033 to U+0033
        '4': '4',    # U+0034 to U+0034
        '5': '5',    # U+0035 to U+0035
        '6': '6',    # U+0036 to U+0036
        '7': '7',    # U+0037 to U+0037
        '8': '8',    # U+0038 to U+0038
        '9': '9',    # U+0039 to U+0039
    }
    return mapping
def decode_text(garbled_text, mapping):
    decoded = ''
    missing_chars = set()
    for char in garbled_text:
        if char in mapping:
            decoded += mapping[char]
        else:
            if char not in ['\n', ' ', '\t', '.', ',', '(', ')', '-', '—']:  # Ignore common punctuation
                missing_chars.add(char)
            decoded += char  # Optionally keep the original char
    if missing_chars:
        print(f"Missing mappings for: {', '.join(missing_chars)}")
    return decoded

def extract_and_decode_pdf_pages(pdf_path, start_page, end_page, output_dir):
    try:
        # Open the PDF using PyMuPDF
        doc = fitz.open(pdf_path)
        num_pages = len(doc)

        # Validate page numbers
        if start_page < 0 or end_page >= num_pages:
            print(f"Error: Page range {start_page + 1} to {end_page + 1} is invalid. PDF has {num_pages} pages.")
            return

        # Get the mapping
        mapping = create_hebrew_mapping()

        for page_num in range(start_page, end_page + 1):
            # Get output filename
            output_path = get_output_filename(pdf_path, page_num, output_dir)

            # Get the specified page
            page = doc[page_num]

            # Extract text from the page using a custom function to handle order
            text = extract_text_from_page(page)

            # Decode the text
            decoded_text = decode_text(text, mapping)

            # Write the decoded text to file for further processing
            with open(output_path, 'w', encoding='utf-8') as out_file:
                out_file.write(decoded_text)

            print(f"Decoded text for page {page_num + 1} has been saved to {output_path}")

        # Close the document
        doc.close()

    except Exception as e:
        print(f"Error processing PDF: {e}")

def extract_text_from_page(page):
    # Extract text blocks with their positions
    blocks = page.get_text("blocks")

    # Sort blocks: adjust the sort key depending on layout
    # For example, sort by vertical position (y0), then horizontal position (x0)
    blocks.sort(key=lambda b: (b[1], b[0]))

    text = ''
    for block in blocks:
        block_text = block[4]
        text += block_text + '\n'

    return text

def get_output_filename(pdf_path, page_num, output_dir):
    pdf_name = pathlib.Path(pdf_path).stem
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{timestamp}_{pdf_name}_page{page_num+1:03d}_raw.txt"
    return os.path.join(output_dir, filename)

if __name__ == "__main__":
    pdf_path = "25tisa1a.pdf"  # Replace with your PDF file path
    start_page = 0        # Starting page number (0-based index)
    end_page = 5         # Ending page number (0-based index)
    output_dir = "extracted_pages"

    # Extract and decode the pages in the specified range
    extract_and_decode_pdf_pages(pdf_path, start_page, end_page, output_dir)