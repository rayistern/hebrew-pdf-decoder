def direct_decode(input_file, output_file):
    """
    Directly decode a file using a simple mapping table
    based on our analysis of the character patterns
    """
    # Comprehensive mapping from byte values to Hebrew characters
    byte_to_hebrew = {
        # ASCII and control characters (0x00-0x1F)
        0x01: 'ת',  # Tav
        0x02: 'י',  # Yod
        0x03: 'ר',  # Resh
        0x04: ' ',  # Space
        0x05: 'ב',  # Bet
        0x06: 'נ',  # Nun
        0x07: 'ח',  # Chet
        0x0b: 'ט',  # Tet
        0x0c: 'ק',  # Kuf
        0x0e: 'ך',  # Final Kaf
        0x0f: 'ד',  # Dalet
        0x10: 'ג',  # Gimel
        0x11: 'ע',  # Ayin
        0x12: 'כ',  # Kaf
        0x13: 'צ',  # Tsadi
        0x14: 'מ',  # Mem
        0x15: 'פ',  # Pe
        0x16: 'ס',  # Samech
        0x17: 'ף',  # Final Pe
        
        # ASCII space
        0x20: ' ',  # Space
        
        # Extended characters
        0x86: 'א',  # Alef variant
        0x87: 'ו',  # Vav variant
        0x99: 'ה',  # He variant
        0x9b: 'צ',  # Tsadi variant
        0x9c: 'ש',  # Shin variant
        
        # Unicode characters
        0xC7: 'א',  # Alef (first byte of \u02c7)
        0xC6: 'ו',  # Vav (first byte of \u02c6)
        0xD8: '.',  # Period (first byte of \u02d8)
        0xDD: 'ז',  # Zayin (first byte of \u02dd)
        0xDB: 'ה',  # He (first byte of \u02db)
        0xB0: 'ט',  # Tet (first byte of \u00b0)
        0xDC: 'ן',  # Final Nun (first byte of \u02dc)
    }
    
    # Read file as bytes
    with open(input_file, 'rb') as f:
        content_bytes = f.read()
    
    # Decode directly from bytes to Hebrew
    result = ""
    i = 0
    while i < len(content_bytes):
        b = content_bytes[i]
        
        # Skip second byte of Unicode characters
        if i > 0 and content_bytes[i-1] in [0xC7, 0xC6, 0xD8, 0xDD, 0xDB, 0xDC]:
            i += 1
            continue
            
        # Look up the mapping
        if b in byte_to_hebrew:
            result += byte_to_hebrew[b]
        elif b in [10, 13]:  # newlines
            result += chr(b)
        else:
            # Mark unmapped bytes
            result += f"[{b:02x}]"
        
        i += 1
    
    # Write the result with both normal and RTL versions
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    with open(output_file + ".rtl", 'w', encoding='utf-8') as f:
        f.write('\u202B' + result + '\u202C')  # RTL markers
    
    print(f"Decoded output saved to {output_file}")
    print(f"RTL version saved to {output_file}.rtl")
    print(f"Result: {result}")
    
    return result

if __name__ == "__main__":
    # Decode our two test files
    direct_decode("t1.txt", "t1_decoded.txt")
    
    # Also try with the larger file if it exists
    try:
        direct_decode("extracted_pages/t1.txt", "extracted_t1_decoded.txt")
        print("\nAlso decoded the larger extracted file")
    except FileNotFoundError:
        print("\nNo extracted_pages/t1.txt file found") 