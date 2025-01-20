# text_processor.py

import os
import re
from bidi.algorithm import get_display
import shutil  # Import shutil to move files

def process_text_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Create a 'done' directory within the input directory
    done_dir = os.path.join(input_dir, 'done')
    os.makedirs(done_dir, exist_ok=True)

    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith("_raw.txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace("_raw.txt", ".md"))

            with open(input_path, 'r', encoding='utf-8') as infile:
                text = infile.read()

            # Process the text
            processed_text = clean_text(text)

            # Correct the text direction
            final_text = correct_text_direction(processed_text)

            # Write the processed text to output file
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(final_text)

            print(f"Processed text has been saved to {output_path}")

            # Move the processed file to 'done' folder
            shutil.move(input_path, os.path.join(done_dir, filename))
            print(f"Moved {input_path} to {done_dir}")

def clean_text(text):
    # Remove sequences of numbers (footnote markers), possibly with punctuation, surrounded by newlines
    text = re.sub(r'\n\s*\d+[\s]*[.,]?\s*\n', '\n', text)

    # Remove hyphenation at line breaks
    text = re.sub(r'-\s*\n\s*', '', text)

    # Normalize multiple newlines to a single newline
    text = re.sub(r'\n\s*\n+', '\n', text)

    # Normalize multiple spaces to a single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Strip leading and trailing whitespace on each line
    text = '\n'.join(line.strip() for line in text.split('\n'))

    return text

def correct_text_direction(text):
    # Correct the text direction using python-bidi
    final_text = get_display(text)

    # Optionally, add Right-to-Left Mark at the beginning
    final_text = '\u200F' + final_text

    return final_text

if __name__ == "__main__":
    input_dir = "extracted_pages"
    output_dir = "input_files"

    process_text_files(input_dir, output_dir)