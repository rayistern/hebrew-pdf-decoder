def analyze_file(filename):
    try:
        # Try UTF-8 first
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback to latin-1 which can read any byte
        with open(filename, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Create a dictionary to store character counts
    char_counts = {}
    
    # Process each character
    for char in content:
        if char not in [' ', '\n', '\r', '\t']:
            if char not in char_counts:
                char_counts[char] = 0
            char_counts[char] += 1
    
    # Print character codes and frequencies
    print(f"Character analysis for {filename}:")
    print("Unicode | Character | Hex | Count")
    print("--------|-----------|-----|------")
    
    for char, count in sorted(char_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{ord(char):8d} | {repr(char):11s} | {hex(ord(char)):6s} | {count:6d}")

if __name__ == "__main__":
    filename = "extracted_pages/t1.txt"
    analyze_file(filename) 