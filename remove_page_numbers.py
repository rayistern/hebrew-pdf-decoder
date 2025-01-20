import os
import re
import shutil

def remove_page_numbers(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Create a 'done' directory within the input directory
    done_dir = os.path.join(input_dir, 'done')
    os.makedirs(done_dir, exist_ok=True)

    # Compile a regex pattern to match potential page number lines
    page_number_pattern = re.compile(
        r'^'                      # Start of the line
        r'\s*'                    # Optional whitespace
        r'[\.\-–—]*'              # Optional dots, dashes, or long dashes
        r'\s*'                    # Optional whitespace
        r'('
            r'[0-9]+|'            # One or more digits
            r'[א-ת]{1,4}|'        # One to four Hebrew letters
            r'[A-Za-z]+|'         # One or more Latin letters
            r'.*?[0-9]+.*?|'      # Any text containing digits (e.g., dates)
            r'\W*'                # Non-word characters (e.g., punctuation)
        r')'
        r'\s*'                    # Optional whitespace
        r'$'                      # End of the line
    )

    for filename in sorted(os.listdir(input_dir)):
        input_path = os.path.join(input_dir, filename)

        if os.path.isfile(input_path) and (filename.endswith(".txt") or filename.endswith(".md")):
            output_path = os.path.join(output_dir, filename)

            with open(input_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            # Process the lines
            processed_lines = []
            line_num = 0
            total_lines = len(lines)
            for line in lines:
                line_num += 1
                # Assume page numbers are more likely at the top or bottom 3 lines
                if (
                    page_number_pattern.match(line) and
                    (line_num <= 3 or line_num > total_lines - 3)
                ):
                    print(f"Removed page number line: {line.strip()}")
                else:
                    processed_lines.append(line)

            # Write the processed text to output file
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.writelines(processed_lines)

            print(f"Processed file has been saved to {output_path}")

            # Move the processed file to 'done' folder
            shutil.move(input_path, os.path.join(done_dir, filename))
            print(f"Moved {input_path} to {done_dir}")

if __name__ == "__main__":
    input_dir = "processed_files"
    output_dir = "final_files"

    remove_page_numbers(input_dir, output_dir) 