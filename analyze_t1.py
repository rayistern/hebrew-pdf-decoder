def analyze_t1_file():
    """Directly analyze the content of t1.txt"""
    from pattern_mapping import create_hebrew_pattern_mapping
    
    # Read the file as bytes
    with open("t1.txt", "rb") as f:
        content_bytes = f.read()
    
    # Display the raw bytes
    print("Raw bytes (first 30):")
    print(" ".join(f"{b:02x}" for b in content_bytes[:30]))
    
    # Now decode using latin-1 to preserve all byte values as characters
    content = content_bytes.decode('latin-1')
    
    # Print the Unicode code points
    print("\nUnicode code points (first 15 chars):")
    for i, char in enumerate(content[:15]):
        print(f"{i:2d}: '{char}' -> U+{ord(char):04X}")
    
    # Check our mapping
    char_map, _ = create_hebrew_pattern_mapping()
    
    print("\nMapping of characters:")
    for i, char in enumerate(content):
        if char in char_map:
            print(f"{i:2d}: '{char}' (U+{ord(char):04X}) -> '{char_map[char]}'")
        elif char not in ['\n', '\r', '\t', ' ']:
            print(f"{i:2d}: '{char}' (U+{ord(char):04X}) -> unmapped")
    
    # Try to map the content manually
    result = ""
    for char in content:
        if char in char_map:
            result += char_map[char]
        elif char in ['\n', '\r', '\t', ' ']:
            result += char
        else:
            result += '□'
    
    print("\nManual mapping result:")
    print(result)
    
    return content_bytes

if __name__ == "__main__":
    analyze_t1_file() 