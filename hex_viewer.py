def view_file_hex(filename):
    """Display file contents as hex bytes with their ASCII/Unicode representation"""
    with open(filename, 'rb') as f:
        content = f.read()
    
    print(f"\nHex dump of {filename} ({len(content)} bytes):")
    print("Offset | Hex bytes                                | ASCII/Unicode")
    print("-------|------------------------------------------|----------------")
    
    # Display hex and ASCII in rows of 16 bytes
    for i in range(0, len(content), 16):
        chunk = content[i:i+16]
        
        # Format as hex
        hex_str = ' '.join(f"{b:02x}" for b in chunk)
        hex_padding = ' ' * (48 - len(hex_str))
        
        # Format as ASCII/Unicode (replace control chars with dots)
        char_str = ''
        for b in chunk:
            if 32 <= b <= 126:  # Printable ASCII
                char_str += chr(b)
            else:
                char_str += '.'
        
        print(f"{i:06x} | {hex_str}{hex_padding} | {char_str}")
    
    return content

if __name__ == "__main__":
    # View both files
    print("Viewing t1.txt")
    view_file_hex("t1.txt")
    
    try:
        print("\nViewing extracted_pages/t1.txt")
        view_file_hex("extracted_pages/t1.txt")
    except FileNotFoundError:
        print("\nFile extracted_pages/t1.txt not found") 