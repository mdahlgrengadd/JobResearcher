import os
import re


def split_markdown_files(input_file, output_dir='docs'):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the combined markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content by file markers
    # Looking for patterns like "// 1. main.md" or similar
    files_content = re.split(r'// \d+\. [\w-]+\.md\n', content)
    # Get all filenames
    filenames = re.findall(r'// \d+\. ([\w-]+\.md)\n', content)

    # Remove empty first split if it exists
    if not files_content[0].strip():
        files_content = files_content[1:]

    # Ensure we have matching numbers of files and content blocks
    if len(files_content) != len(filenames):
        raise ValueError(
            "Mismatch between number of file markers and content blocks")

    # Write each section to its own file
    for filename, content in zip(filenames, files_content):
        output_path = os.path.join(output_dir, filename)
        # Remove trailing whitespace but keep newlines
        cleaned_content = '\n'.join(line.rstrip()
                                    for line in content.strip().splitlines())

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Created {output_path}")


def main():
    # Specify the input file containing all markdown content
    input_file = 'landing_page.md'

    try:
        split_markdown_files(input_file)
        print("\nMarkdown files have been successfully split!")
        print("Check the 'docs' directory for the individual files.")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
