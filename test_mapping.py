from hebrew_mapping import create_new_hebrew_mapping

def decode_text(text, mapping):
    decoded = ""
    missing_chars = set()
    
    for char in text:
        if char in mapping:
            decoded += mapping[char]
        else:
            decoded += char
            if char not in [' ', '\n', '\r', '\t']:
                missing_chars.add(char)
    
    if missing_chars:
        print(f"Missing mappings for: {', '.join(repr(c) for c in missing_chars)}")
    
    return decoded

def test_mapping(input_file, output_file):
    mapping = create_new_hebrew_mapping()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='latin-1') as f:
            text = f.read()
    
    decoded_text = decode_text(text, mapping)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decoded_text)
    
    print(f"Decoded text saved to {output_file}")

if __name__ == "__main__":
    test_mapping("extracted_pages/t1.txt", "decoded_test.txt") 