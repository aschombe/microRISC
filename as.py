# usage:
# python3 as.py <input_file>

import sys
import os

registers = { }
for i in range(30):
    registers["R" + str(i)] = format(i, "05b")
registers["CMP"] = "11110"
registers["SP"] = "11111"

opcodes = {
    "NOP": "000000",
    # more to do here
}

# reads a file line by line
def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        print("File not found")
        exit()

# extracts the text section
def extract_text(lines):
    text_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".text":
            for j in range(i+1, len(lines)):
                if lines[j].strip() == ".data":
                    break
                text_section.append(lines[j])

    return text_section

# assembles the text section to hex
def assemble_text_section(text_section):
    return

# extracts the data section
def extract_data(lines):
    data_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".data":
            for j in range(i+1, len(lines)):
                if lines[j].strip() == ".text":
                    break
                data_section.append(lines[j])

    return data_section

# assembles the data section to hex
def assemble_data_section(data_section):
    return

def main():
    # check for correct usage
    if len(sys.argv) != 2:
        print("Usage: python3 as.py <input_file>")
        sys.exit(1)

    # check if file exists
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("Error: File not found")
        sys.exit(1)

    # read the file
    lines = read_file(input_file)

    if not lines:
        print("Error: Input file is empty")
        sys.exit(1)
    
    # extract the text section
    text_section = extract_text(lines)

    if not text_section:
        print("Error: No text section found")
        sys.exit(1)
    else:
        # assemble the text section
        assemble_text_section(text_section)

    # extract the data section
    data_section = extract_data(lines)

    if not data_section:
        print("Warning: No data section found")
    else:
        # assemble the data section
        assemble_data_section(data_section)
    
main()
