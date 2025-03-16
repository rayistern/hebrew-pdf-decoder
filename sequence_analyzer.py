def analyze_sequences(filename, max_sequence_length=3):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Record sequences of characters and their frequency
    sequences = {}
    
    # Analyze different sequence lengths
    for seq_len in range(1, max_sequence_length + 1):
        for i in range(len(content) - seq_len + 1):
            seq = content[i:i+seq_len]
            if any(c.isspace() for c in seq):
                continue
            if seq not in sequences:
                sequences[seq] = 0
            sequences[seq] += 1
    
    # Print most common sequences
    print(f"Most common character sequences in {filename}:")
    print("Sequence | Length | Hex | Count")
    print("---------|--------|-----|------")
    
    for seq, count in sorted(sequences.items(), key=lambda x: x[1], reverse=True)[:50]:
        hex_repr = ' '.join(f"{ord(c):04x}" for c in seq)
        print(f"{repr(seq):10s} | {len(seq):6d} | {hex_repr} | {count:6d}")
    
    return sequences

if __name__ == "__main__":
    analyze_sequences("extracted_pages/t1.txt", max_sequence_length=3) 