#!/usr/bin/env python3

import argparse
from tokenize import extract_data, extract_text
from assembly import assemble_data_section, assemble_text_section

labels = {}
adr_labels = {}

def read_file(path: str):
    try:
        with open(path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: file '{path}' not found.")
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description="microRISC assembler")
    parser.add_argument("input_file", type=str, help="Assembly source file")
    args = parser.parse_args()

    lines = read_file(args.input_file)
    if not lines:
        print("Error: input file is empty.")
        raise SystemExit(1)

    data_section = extract_data(lines)
    if data_section:
        assemble_data_section(data_section, labels, adr_labels)

    text_section = extract_text(lines)
    if not text_section:
        print("Error: no <text> section found.")
        raise SystemExit(1)

    assemble_text_section(text_section, labels, adr_labels)


if __name__ == "__main__":
    main()
