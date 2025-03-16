with open('t1.txt', 'rb') as file:
    lines = file.readlines()

for line_number, line in enumerate(lines, start=1):
    # Decode the line using 'latin1' to avoid decoding errors
    decoded_line = line.decode('latin1')
    positions = [pos for pos, char in enumerate(decoded_line) if char == ',']
    for pos in positions:
        char = decoded_line[pos]
        char_code = ord(char)
        print(f"Character '{char}' at line {line_number}, position {pos}: code {char_code}") 