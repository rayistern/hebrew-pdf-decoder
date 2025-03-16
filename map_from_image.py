def analyze_file_for_mapping(filename):
    """Analyze a file character by character to help with manual mapping"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Create a list of characters with positions
    char_positions = []
    line_num = 1
    col_num = 1
    
    for char in content:
        if char == '\n':
            line_num += 1
            col_num = 1
            continue
        
        char_positions.append((char, line_num, col_num))
        col_num += 1
    
    # Display characters in a grid format for easier mapping
    print(f"File: {filename}")
    print("\nCharacter grid (line:column):")
    print("============================")
    
    for i, (char, line, col) in enumerate(char_positions):
        # Skip display of whitespace characters
        if char.isspace():
            continue
            
        char_code = f"0x{ord(char):04x}"
        print(f"{i+1:3d}. '{char}' ({char_code}) at {line}:{col}")
        
        # Every 5 characters, pause and ask for Hebrew mapping
        if (i + 1) % 500 == 0:
            print("\nEnter the corresponding Hebrew characters for the above (leave blank to skip):")
            mapping_input = input("> ")
            
            if mapping_input:
                chars = mapping_input.split()
                if len(chars) <= 5:
                    # Display the mapping
                    print("\nMapping added:")
                    for j in range(min(5, len(chars))):
                        if j < len(chars) and chars[j]:
                            idx = i - 4 + j
                            if idx < len(char_positions):
                                orig_char = char_positions[idx][0]
                                print(f"'{orig_char}' ({hex(ord(orig_char))}) -> '{chars[j]}'")
    
    print("\nAnalysis complete. Use this information to create your mapping dictionary.")

if __name__ == "__main__":
    filename = "extracted_pages/t1.txt"
    analyze_file_for_mapping(filename) 