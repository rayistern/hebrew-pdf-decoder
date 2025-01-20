from PyPDF2 import PdfReader
import zlib  # for FlateDecode

def try_decrypt(reader, password=None):
    if password:
        try:
            reader.decrypt(password)
            print(f"Successfully decrypted with password: {password}")
            return True
        except:
            return False
    return False

def extract_stream_data(pdf_content):
    # Find stream markers
    stream_start = pdf_content.find(b'stream\n')
    stream_end = pdf_content.find(b'endstream')
    if stream_start != -1 and stream_end != -1:
        # Extract the compressed data between stream and endstream
        compressed_data = pdf_content[stream_start + 7:stream_end]
        try:
            # Decompress using zlib (FlateDecode)
            decompressed = zlib.decompress(compressed_data)
            return decompressed
        except zlib.error as e:
            print(f"Decompression error: {e}")
    return None

pdf_path = './lh1.pdf'
reader = PdfReader(pdf_path)

print("PDF Information:")
print(f"Encrypted: {reader.is_encrypted}")
if reader.is_encrypted:
    # Try some common passwords
    passwords = ["", "password", "1234", "admin"]
    for password in passwords:
        if try_decrypt(reader, password):
            break
    else:
        print("Could not decrypt with common passwords")

# Try to read pages regardless
for page_num, page in enumerate(reader.pages, 1):
    print(f"\nPage {page_num}:")
    try:
        text = page.extract_text()
        print(text)
    except Exception as e:
        print(f"Error extracting text: {e}")
        # Try to get raw content
        try:
            print("Raw content:")
            print(page.get_contents())
        except:
            print("Could not get raw content")

# Read the PDF file in binary mode
with open('./lh1.pdf', 'rb') as f:
    pdf_content = f.read()

# Find and decode all streams
pos = 0
while True:
    stream_pos = pdf_content.find(b'stream\n', pos)
    if stream_pos == -1:
        break
    
    # Find corresponding endstream
    end_pos = pdf_content.find(b'endstream', stream_pos)
    if end_pos == -1:
        break
        
    # Extract and decode this stream
    stream_data = extract_stream_data(pdf_content[stream_pos:end_pos+9])
    if stream_data:
        print("\nDecoded stream content:")
        print(stream_data)
    
    pos = end_pos + 9

def create_hebrew_mapping():
    mapping = {
        # Basic Hebrew letters
        'ô': 'פ',
        'ú': 'ת',
        'ç': 'ח',
        'ã': 'ד',
        'á': 'ב',
        'ø': 'ר',
        '˜': 'ק',
        '˘': 'ש',
        'Ú': 'ע',
        'Ì': 'ם',
        'È': 'י',
        'Â': 'ו',
        '‰': 'ה',
        'ä': 'ה',
        'î': 'מ',
        'ù': 'ש',
        'é': 'י',
        'è': 'ט',
        'ì': 'ל',
        'ë': 'כ',
        'à': 'א',
        'Ù': 'פ',
        '˙': 'ת',
        '„': 'ד',
        'Ó': 'מ',
        'Á': 'ח',
        'Î': 'כ',
        'Ê': 'ז',
        '¯': 'ר',
        '‡': 'א',
        'Ï': 'ל',
        
        # Fixed/new mappings
        'å': 'ו',
        'æ': 'ז',
        'ö': 'צ',
        '‚': 'ג',
        '·': 'ב',
        'ñ': 'ס',
        'ò': 'ע',
        'ð': 'נ',  # Added missing נ
        'Ë': 'ט',  # Added missing ט
        
        # Final letters
        'í': 'ם',  # Final mem
        'ê': 'ך',  # Final kaf
        'ï': 'ן',  # Final nun
        'ó': 'ף',  # Final pe
        'õ': 'ץ',  # Final tzadi
        
        # Special combinations
        "‰'": "ה'",
        '„"': 'ד"',
        'Î"': 'כ"',
        '˘"': 'ש"',
        'Ù"': 'פ"',
        '‡"': 'א"',
        
        # Punctuation and special characters
        '"': '"',
        "'": "'",
        '(': '(',
        ')': ')',
        ',': ',',
        '.': '.',
        ' ': ' ',
        '-': '-',
        '!': '!',
        '[': '[',
        ']': ']',
        '❁': '❁',
        'Z': 'Z',
        ':': ':',
        ';': ';',
        '\n': '\n'
    }
    return mapping

def decode_text(garbled_text):
    mapping = create_hebrew_mapping()
    decoded = ''
    for char in garbled_text:
        decoded += mapping.get(char, char)
    return decoded

# Test with first few lines
sample = """äë (à) ä"îùú'ä ,èáù à"é ,çìùá ô"ù
ÌÈ˜¯Ù‰ ÌÈ¯˘Ú ˙‡ Â„ÓÏ˘ È¯Á‡Ï ,ÈÎ ,ÂÊ ‰˘Ï ÍÈÈ˘‰ ˜¯Ù‰ ‡Â‰˘"""

print("Original:", sample)
print("Decoded:", decode_text(sample))

def clean_hebrew_text(text):
    """
    Clean and normalize Hebrew/Aramaic text that has been incorrectly encoded.
    
    Args:
        text (str): The raw text input
        
    Returns:
        str: Cleaned and normalized text
    """
    # Remove line numbers and other artifacts
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip line numbers at start (e.g. "1| ", "2| ")
        if '|' in line:
            line = line.split('|', 1)[1].strip()
            
        # Skip purely numeric lines
        if line.strip().isdigit():
            continue
            
        # Skip empty lines
        if not line.strip():
            continue
            
        cleaned_lines.append(line)
    
    # Rejoin cleaned lines
    cleaned_text = '\n'.join(cleaned_lines)
    
    # TODO: Add Hebrew character normalization
    # This will require determining the original encoding and properly decoding
    
    return cleaned_text

# Read and process the entire file
try:
    with open('lh1.pdf', 'r', encoding='utf-8') as file:
        content = file.read()
        print("Decoded content:")
        cleaned = clean_hebrew_text(content)
        print(cleaned)
except Exception as e:
    print(f"Error reading file: {e}")

def read_specific_page(pdf_path, page_num):
    reader = PdfReader(pdf_path)
    
    if page_num < 0 or page_num >= len(reader.pages):
        print(f"Error: Page {page_num} does not exist. PDF has {len(reader.pages)} pages.")
        return
    
    print(f"\nReading Page {page_num}:")
    try:
        page = reader.pages[page_num]
        text = page.extract_text()
        decoded_text = decode_text(text)
        print("Decoded text:")
        print(decoded_text)
    except Exception as e:
        print(f"Error extracting text: {e}")
        try:
            print("Attempting to read raw content...")
            raw_content = page.get_contents()
            if raw_content:
                decoded_raw = decode_text(str(raw_content))
                print(decoded_raw)
        except:
            print("Could not get raw content")

if __name__ == "__main__":
    pdf_path = './lh1.pdf'
    page_to_read = 55  # Specify the page number here (0-based index)
    read_specific_page(pdf_path, page_to_read)