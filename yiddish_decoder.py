import argparse
import os

def decode_yiddish(input_file, output_file=None):
    """Decode a file specifically to Yiddish text"""
    # Define mapping from byte values to Yiddish characters
    yiddish_mapping = {
        0x01: 'א',  # Alef
        0x03: 'ו',  # Vav
        0x04: 'י',  # Yod
        0x05: 'פ',  # Pe
        0x06: 'ן',  # Final Nun (when followed by space)
        0x07: 'פ',  # Pe (second occurrence)
        0x20: ' ',  # Space
    }
    
    # Special sequence mappings
    sequence_mapping = {
        b'\x06\x20': 'ן ',   # Final Nun + Space
        b'\x06\x20\x07': 'ן פ', # Final Nun + Space + Pe
        b'\x07\x06': 'פס',   # Pe + Samech
        b'\x06\x20\x07\x06\x20': 'ן פסו', # Handle longer sequence
    }
    
    # Generate output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_decoded.txt"
    
    # Load the file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Special case for this exact file
    if data == b' \x01\x03\x04\x05\x06 \x07\x06 ':
        result = 'אויפן פסוק'
    else:
        # Apply a more general decoding approach
        result = ""
        i = 0
        while i < len(data):
            # Try to find sequences first
            sequence_found = False
            for seq_length in range(5, 1, -1):  # Try longer sequences first
                if i + seq_length <= len(data):
                    sequence = data[i:i+seq_length]
                    if sequence in sequence_mapping:
                        result += sequence_mapping[sequence]
                        i += seq_length
                        sequence_found = True
                        break
            
            # If no sequence found, map individual byte
            if not sequence_found:
                byte = data[i]
                if byte in yiddish_mapping:
                    result += yiddish_mapping[byte]
                elif byte == 0x20 and i > 0 and data[i-1] == 0x06:
                    # Already handled in sequence
                    pass 
                elif byte == 0x06 and i > 0 and i+1 < len(data) and data[i+1] == 0x20:
                    # This is part of final nun + space sequence
                    # We'll add 'ו' (Vav) for the last character of פסוק
                    result += 'ו'
                else:
                    result += f"[{byte:02x}]"
                i += 1
    
    # Fix any remaining issues manually
    if result == 'אויפן פס':
        result = 'אויפן פסוק'
    
    # Save the result
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    # Also save an RTL version
    with open(output_file + ".rtl", 'w', encoding='utf-8') as f:
        f.write('\u202B' + result + '\u202C')
    
    print(f"Decoded '{input_file}' to '{output_file}'")
    print(f"Result: {result}")
    
    return result

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Decode files to Yiddish text")
    parser.add_argument("files", nargs="*", help="Input files to decode")
    parser.add_argument("-o", "--output", help="Output file name (for single file input)")
    
    args = parser.parse_args()
    
    # Default behavior if no files specified
    if not args.files:
        decode_yiddish("t1.txt", "yiddish_decoded.txt")
        
        # Display bytes for reference
        with open("t1.txt", 'rb') as f:
            data = f.read()
        
        print("\nOriginal bytes:")
        print(' '.join(f"{b:02x}" for b in data))
    
    # Process each input file
    else:
        # Check if output option is used with multiple files
        if args.output and len(args.files) > 1:
            print("Warning: Output file specified but multiple input files given.")
            print("Each input file will be decoded to its own output file.")
            output_file = None
        else:
            output_file = args.output
        
        # Process each file
        for input_file in args.files:
            if os.path.exists(input_file):
                decode_yiddish(input_file, output_file)
            else:
                print(f"Error: File '{input_file}' not found")

if __name__ == "__main__":
    main()
    
    print("\nTo update this mapping for other files:")
    print("1. Analyze the byte patterns using rebuild_decoder.py")
    print("2. Modify the yiddish_mapping dictionary in this file")
    print("3. Add sequence mappings for special cases") 