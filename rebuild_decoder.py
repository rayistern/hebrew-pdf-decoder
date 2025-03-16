def analyze_file(filename):
    """Analyze a file at the byte level without assumptions"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"\nAnalyzing {filename} ({len(data)} bytes)")
    
    # Count byte frequencies
    byte_counts = {}
    for b in data:
        if b not in byte_counts:
            byte_counts[b] = 0
        byte_counts[b] += 1
    
    # Show most common bytes
    print("\nMost common bytes:")
    print("Byte | Hex  | Count")
    print("-----|------|------")
    for b, count in sorted(byte_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"{b:4d} | 0x{b:02x} | {count:5d}")
    
    # Look for patterns: check for byte sequences
    print("\nLooking for patterns...")
    
    # Find repeat sequences (min 2 bytes, max 5 bytes)
    sequences = {}
    for length in range(2, 6):
        for i in range(len(data) - length + 1):
            seq = bytes(data[i:i+length])
            if seq not in sequences:
                sequences[seq] = 0
            sequences[seq] += 1
    
    # Show most common sequences
    print("\nMost common sequences:")
    print("Sequence | Hex | Count")
    print("---------|-----|------")
    for seq, count in sorted(sequences.items(), key=lambda x: x[1], reverse=True)[:10]:
        if count > 1:  # Only show sequences that repeat
            hex_str = ' '.join(f"{b:02x}" for b in seq)
            print(f"{seq!r:10s} | {hex_str} | {count:5d}")
    
    # Look at the beginning of lines (if there are newlines)
    if b'\n' in data:
        print("\nBytes at the beginning of lines:")
        lines = data.split(b'\n')
        line_starts = {}
        for line in lines[1:]:  # Skip first line
            if line:
                first_byte = line[0]
                if first_byte not in line_starts:
                    line_starts[first_byte] = 0
                line_starts[first_byte] += 1
        
        for b, count in sorted(line_starts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"0x{b:02x}: {count} times")
    
    return data

def build_mapping_helper():
    """Build an interactive helper for mapping bytes to Hebrew"""
    print("\nHebrew Mapping Helper")
    print("--------------------")
    print("This tool will help you map byte values to Hebrew characters.")
    
    # Hebrew alphabet in logical order
    hebrew_alphabet = [
        ('א', 'Alef'),
        ('ב', 'Bet'),
        ('ג', 'Gimel'),
        ('ד', 'Dalet'),
        ('ה', 'He'),
        ('ו', 'Vav'),
        ('ז', 'Zayin'),
        ('ח', 'Het'),
        ('ט', 'Tet'),
        ('י', 'Yod'),
        ('כ', 'Kaf'),
        ('ל', 'Lamed'),
        ('מ', 'Mem'),
        ('נ', 'Nun'),
        ('ס', 'Samekh'),
        ('ע', 'Ayin'),
        ('פ', 'Pe'),
        ('צ', 'Tsadi'),
        ('ק', 'Qof'),
        ('ר', 'Resh'),
        ('ש', 'Shin'),
        ('ת', 'Tav'),
        # Final forms
        ('ך', 'Final Kaf'),
        ('ם', 'Final Mem'),
        ('ן', 'Final Nun'),
        ('ף', 'Final Pe'),
        ('ץ', 'Final Tsadi'),
    ]
    
    # Print the Hebrew alphabet as a reference
    print("\nHebrew alphabet reference:")
    for i, (char, name) in enumerate(hebrew_alphabet):
        print(f"{i+1:2d}. {char} ({name})")
    
    # Guide for interactive mapping
    print("\nTo use this tool:")
    print("1. Examine the byte patterns in your file")
    print("2. For each common byte or sequence, specify which Hebrew letter it maps to")
    print("3. Test the mapping on sample data")
    
    print("\nExample mapping code:")
    print("""
mapping = {
    0x01: 'א',  # Alef
    0x02: 'ב',  # Bet
    # Add more mappings as needed
}

# To apply the mapping:
result = ""
for b in bytes_data:
    if b in mapping:
        result += mapping[b]
    else:
        result += f"[{b:02x}]"  # Mark unmapped bytes
    """)
    
    print("\nStart by analyzing your encoded file with:")
    print("data = analyze_file('your_file.txt')")

if __name__ == "__main__":
    # Analyze the t1.txt file
    analyze_file("t1.txt")
    
    # Provide mapping helper
    build_mapping_helper() 