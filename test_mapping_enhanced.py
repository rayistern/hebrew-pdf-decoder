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
    
    # Create a side-by-side view of each character and its mapping
    analysis = []
    for char in text:
        if char in mapping:
            mapped_to = mapping[char]
        else:
            mapped_to = char
        
        if char not in ['\n', '\r', '\t']:
            analysis.append((char, hex(ord(char)), mapped_to))
    
    # Print side-by-side view
    print("Original | Hex Code | Mapped To")
    print("---------|----------|----------")
    for orig, hex_code, mapped in analysis:
        print(f"{repr(orig):10s} | {hex_code:8s} | {mapped}")
    
    # Perform normal decoding
    decoded_text = decode_text(text, mapping)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decoded_text)
    
    print(f"\nDecoded text saved to {output_file}")
    
    # Show a preview of the decoded text
    preview_length = min(100, len(decoded_text))
    print(f"\nPreview of decoded text:")
    print(decoded_text[:preview_length])

if __name__ == "__main__":
    test_mapping("extracted_pages/t1.txt", "decoded_test.txt") 