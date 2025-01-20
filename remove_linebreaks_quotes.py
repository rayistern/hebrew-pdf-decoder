import os
import re
import shutil

def remove_linebreaks_around_quotes(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Create a 'done' directory within the input directory
    done_dir = os.path.join(input_dir, 'done')
    os.makedirs(done_dir, exist_ok=True)

    for filename in sorted(os.listdir(input_dir)):
        input_path = os.path.join(input_dir, filename)

        if os.path.isfile(input_path) and (filename.endswith(".txt") or filename.endswith(".md")):
            output_path = os.path.join(output_dir, filename)

            with open(input_path, 'r', encoding='utf-8') as infile:
                text = infile.read()

            # Remove line breaks around double quotes
            processed_text = remove_linebreaks_around_double_quotes(text)

            # Write the processed text to output file
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(processed_text)

            print(f"Processed file has been saved to {output_path}")

            # Move the processed file to 'done' folder
            shutil.move(input_path, os.path.join(done_dir, filename))
            print(f"Moved {input_path} to {done_dir}")

def remove_linebreaks_around_double_quotes(text):
    # Define the double quote characters (standard and Hebrew double quote U+05F4)
    double_quotes = r'["״]'

    # Remove line breaks immediately after opening double quotes
    text = re.sub(fr'({double_quotes})\s*\n\s*', r'\1', text)

    # Remove line breaks immediately before closing double quotes
    text = re.sub(fr'\s*\n\s*({double_quotes})', r'\1', text)

    # Remove line breaks around standalone double quotes
    text = re.sub(fr'\n\s*({double_quotes})\s*\n', r'\1', text)

    # Return the processed text
    return text

if __name__ == "__main__":
    input_dir = "input_files"
    output_dir = "processed_files"

    remove_linebreaks_around_quotes(input_dir, output_dir) 