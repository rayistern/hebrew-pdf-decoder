import os
import re
import fitz  # PyMuPDF
import pathlib
from datetime import datetime
from bidi.algorithm import get_display

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

def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF using PyMuPDF
        doc = fitz.open(pdf_path)
        num_pages = len(doc)
        print(f"Total pages in PDF: {num_pages}")

        # Extract text from all pages and concatenate
        all_text = ''
        for page_num in range(num_pages):
            page = doc[page_num]
            # Extract text from the page using a custom function
            text = extract_text_from_page(page)
            all_text += text + '\n'  # Add a newline between pages

        # Close the document
        doc.close()

        return all_text

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ''

def extract_text_from_page(page):
    # Extract text blocks with their positions
    blocks = page.get_text("blocks")

    # Sort blocks: adjust the sort key depending on layout
    # For example, sort by vertical position (y0), then horizontal position (x0)
    # For RTL languages, you might need to adjust the sorting to fit the text flow
    blocks.sort(key=lambda b: (b[1], b[0]))

    text = ''
    for block in blocks:
        block_text = block[4]
        text += block_text + '\n'

    return text

def clean_text(text):
    # Remove sequences of numbers (footnote markers), possibly with punctuation, surrounded by newlines
    text = re.sub(r'\n\s*\d+[\s]*[.,]?\s*\n', '\n', text)

    # Remove hyphenation at line breaks
    text = re.sub(r'-\s*\n\s*', '', text)

    # Remove line breaks around double quotes
    double_quotes = r'["״]'
    text = re.sub(fr'({double_quotes})\s*\n\s*', r'\1', text)  # After opening quote
    text = re.sub(fr'\s*\n\s*({double_quotes})', r'\1', text)  # Before closing quote
    text = re.sub(fr'\n\s*({double_quotes})\s*\n', r'\1', text)  # Standalone quotes

    # Normalize multiple newlines to a single newline
    text = re.sub(r'\n\s*\n+', '\n', text)

    # Normalize multiple spaces to a single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Strip leading and trailing whitespace on each line
    text = '\n'.join(line.strip() for line in text.split('\n'))

    return text

def correct_text_direction(text):
    # Correct the text direction using python-bidi
    final_text = get_display(text)

    # Optionally, add Right-to-Left Mark at the beginning
    final_text = '\u200F' + final_text

    return final_text

def process_pdf(pdf_path, output_file):
    # Step 1: Extract text from PDF
    raw_text = extract_text_from_pdf(pdf_path)

    # Step 2: Decode the text
    mapping = create_hebrew_mapping()
    decoded_text = decode_text(raw_text, mapping)

    # Step 3: Clean the text
    cleaned_text = clean_text(decoded_text)

    # Step 4: Correct text direction
    final_text = correct_text_direction(cleaned_text)

    # Write the final processed text to output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(final_text)

    print(f"Final processed text has been saved to {output_file}")

if __name__ == "__main__":
    pdf_path = "25tisa1a.pdf"  # Replace with your PDF file path
    output_file = "final_text/full_processed_text1a.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    process_pdf(pdf_path, output_file) 