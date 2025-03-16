def create_hebrew_pattern_mapping():
    """Create a mapping from character patterns to Hebrew text"""
    # Define mapping using hex codes for reliability
    char_map = {
        # Control characters (0x00-0x1F)
        '\x01': 'ת',  # Tav
        '\x02': 'י',  # Yod
        '\x03': 'ר',  # Resh
        '\x04': ' ',  # Space
        '\x05': 'ב',  # Bet
        '\x06': 'נ',  # Nun
        '\x07': 'ח',  # Chet
        '\x0b': 'ט',  # Tet
        '\x0c': 'ק',  # Kuf
        '\x0e': 'ך',  # Final Kaf
        '\x0f': 'ד',  # Dalet
        '\x10': 'ג',  # Gimel
        '\x11': 'ע',  # Ayin
        '\x12': 'כ',  # Kaf
        '\x13': 'צ',  # Tsadi
        '\x14': 'מ',  # Mem
        '\x15': 'פ',  # Pe
        '\x16': 'ס',  # Samech
        '\x17': 'ף',  # Final Pe
        
        # Extended Unicode characters
        '\u02d9': 'א',  # Alef - '˙'
        '\u02c7': 'א',  # Alef - 'ˇ'
        '\u02c6': 'ו',  # Vav - 'ˆ'
        '\u02d8': '.',  # Period - '˘'
        '\u02dd': 'ז',  # Zayin - '˝'
        '\u02db': 'ה',  # He - '˛'
        '\u00b0': 'ט',  # Tet - '°'
        '\u02dc': 'ן',  # Final Nun - '˜'
        
        # ASCII symbols
        '!': 'ש',       # Shin
        '"': 'ל',       # Lamed
        '#': 'ם',       # Final Mem
        ' ': ' ',       # Regular space (0x20)
        
        # Additional characters found in our analysis
        '\x86': 'א',    # Another Alef variant
        '\x87': 'ו',    # Another Vav variant
        '\x99': 'ה',    # Another He variant
        '\x9b': 'צ',    # Another Tsadi variant
        '\x9c': 'ש',    # Another Shin variant

        # New mappings based on context and image comparison
        '\x88': 'ל',    # Possible Lamed variant
        '\x89': 'ם',    # Possible Final Mem variant
        '\x8A': 'ן',    # Possible Final Nun variant
        '\x8B': 'י',    # Possible Yod variant
        '\x8C': 'ח',    # Possible Chet variant
        '\x8D': 'צ',    # Possible Tsadi variant
        '\x8E': 'ר',    # Possible Resh variant
        '\x8F': 'ה',    # Possible He variant
    }
    
    # Expanded sequence patterns
    sequence_map = {
        # Previously identified
        '\x03\u02d8': 'ר.',    # Resh-period
        '\x11\x12': 'עכ',      # Ayin-Kaf
        '\x02\x14': 'ימ',      # Yod-Mem
        '\x11\u02d8': 'ע.',    # Ayin-period
        '\u02dd\u02db': 'זה',   # Zayin-He
        
        # New sequences based on common Hebrew combinations
        '!\x02': 'שי',        # Shin-Yod
        '\x01\x03': 'תר',      # Tav-Resh
        '\x05\x06': 'בנ',      # Bet-Nun
        '\x14\x03': 'מר',      # Mem-Resh
        '\x06\x11': 'נע',      # Nun-Ayin
        '\x05\x16': 'בס',      # Bet-Samech
        '\u02c6\x01': 'ות',    # Vav-Tav
        '!\x14': 'שמ',        # Shin-Mem
        '\x14!\x15\x01': 'משפט', # Mem-Shin-Pe-Tet
    }
    
    return char_map, sequence_map

def decode_with_patterns(input_file, output_file):
    """Decode file using both character and sequence mappings"""
    char_map, sequence_map = create_hebrew_pattern_mapping()
    
    # Read file in binary mode to handle control characters correctly
    with open(input_file, 'rb') as f:
        content_bytes = f.read()
    
    # Convert to string using Latin-1 which can represent all byte values
    content = content_bytes.decode('latin-1')
    
    # Debug: Print first few bytes as hex
    print("First 20 bytes as hex:")
    print(' '.join(f"{ord(c):02x}" for c in content[:20]))
    
    # Better sequence handling - process the string character by character
    result = ""
    i = 0
    while i < len(content):
        # Check if any sequence matches at the current position
        sequence_found = False
        for seq, replacement in sequence_map.items():
            if content[i:i+len(seq)] == seq:
                result += replacement
                i += len(seq)
                sequence_found = True
                # Debug output for sequence matches
                print(f"Found sequence: '{seq}' -> '{replacement}' at position {i}")
                break
        
        # If no sequence found, map individual character
        if not sequence_found:
            char = content[i]
            if char in char_map:
                result += char_map[char]
            elif char in ['\n', '\r', '\t']:
                result += char
            else:
                result += '□'  # Placeholder for unmapped chars
            i += 1
    
    # Write output files
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    with open(output_file + ".rtl", 'w', encoding='utf-8') as f:
        f.write('\u202B' + result + '\u202C')
    
    print(f"Decoded text saved to {output_file}")
    print(f"RTL version saved to {output_file}.rtl")
    print(f"Preview (first 100 chars):")
    print(result[:100])

if __name__ == "__main__":
    decode_with_patterns("extracted_pages/t1.txt", "hebrew_decoded_patterns.txt") 