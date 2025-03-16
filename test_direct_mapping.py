from hebrew_mapping_direct import create_direct_hebrew_mapping
import re

def decode_with_direct_mapping(input_file, output_file):
    # Load the mapping
    mapping = create_direct_hebrew_mapping()
    
    # Read the file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Apply mapping
    result = ""
    missing = set()
    
    for char in content:
        if char in mapping:
            result += mapping[char]
        else:
            if char not in ['\n', '\r', '\t']:
                missing.add(char)
            result += char
    
    # Print missing characters
    if missing:
        print(f"Missing mappings for: {', '.join(repr(c) for c in missing)}")
    
    # Fix RTL display issues and write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    # Preview output
    print(f"\nDecoded content saved to {output_file}")
    print(f"Preview (first 200 chars):")
    print(result[:200])

if __name__ == "__main__":
    decode_with_direct_mapping("extracted_pages/t1.txt", "hebrew_decoded.txt") 