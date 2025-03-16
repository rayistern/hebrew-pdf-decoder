def compare_line_by_line(raw_file):
    try:
        with open(raw_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(raw_file, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Break into visible lines for easier comparison
    lines = content.split('\n')
    formatted_output = []
    
    print("RAW TEXT LINES (first 5 lines):")
    print("===============================")
    
    for i, line in enumerate(lines[:5]):
        if line.strip():
            char_codes = ' '.join(f"{c}({hex(ord(c))})" for c in line if not c.isspace())
            print(f"Line {i+1}: {char_codes}")
            
            # Show character count
            non_space_chars = sum(1 for c in line if not c.isspace())
            print(f"  Character count: {non_space_chars}")
            print()
    
    print("\nSample a few Hebrew letters from the image and try to find their pattern:")
    print("1. Look for the first letter א (Alef) in the image")
    print("2. Find the first letter ב (Bet) in the image") 
    print("3. Look for recurring words like של, את, על (common Hebrew words)")

if __name__ == "__main__":
    compare_line_by_line("extracted_pages/t1.txt") 