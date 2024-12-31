import argparse
from file_utils import read_file
from assembly import assemble_data_section, assemble_text_section
from tokenize import extract_data, extract_text

labels = {}
adr_labels = {}

def main():
    parser = argparse.ArgumentParser(description="Assembler for custom assembly language.")
    parser.add_argument("input_file", type=str, help="Path to the input assembly file.")
    args = parser.parse_args()

    lines = read_file(args.input_file)

    if not lines:
        print("Error: Input file is empty.")
        return

    data_section = extract_data(lines)
    if not data_section:
        print("Warning: No data section found.")
    else:
        assemble_data_section(data_section, labels, adr_labels)

    text_section = extract_text(lines)
    if not text_section:
        print("Error: No text section found.")
        return
    else:
        assemble_text_section(text_section, labels, adr_labels)

if __name__ == "__main__":
    main()
