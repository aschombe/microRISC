#!/usr/bin/python

import argparse
import sys
import os
import re

# populate the registers (R0-R31, SP (R30), CMP (R31))
registers = {}
for i in range(32):
    registers["R" + str(i)] = format(i, "05b")
registers["CMP"] = "11110"
registers["LR"] = "11111"

instruction_set = {
    # expected count is the expected number of tokens in the instruction's line
    # Arithemtic and logic instructions
    "ADD":  {"opcode": "000000", "type": "three_reg", "expected_count": 4},
    "SUB":  {"opcode": "000001", "type": "three_reg", "expected_count": 4},
    "MUL":  {"opcode": "000010", "type": "three_reg", "expected_count": 4},
    "DIV":  {"opcode": "000011", "type": "three_reg", "expected_count": 4},
    "AND":  {"opcode": "000100", "type": "three_reg", "expected_count": 4},
    "ORR":  {"opcode": "000101", "type": "three_reg", "expected_count": 4},
    "XOR":  {"opcode": "000110", "type": "three_reg", "expected_count": 4},
    "LSL":  {"opcode": "000111", "type": "three_reg", "expected_count": 4},
    "LSR":  {"opcode": "001000", "type": "three_reg", "expected_count": 4},
    "ASR":  {"opcode": "001001", "type": "three_reg", "expected_count": 4},
    "NEG":  {"opcode": "001010", "type": "one_reg",   "expected_count": 2},
    "ADDI": {"opcode": "001011", "type": "two_reg",   "expected_count": 4},
    "SUBI": {"opcode": "001100", "type": "two_reg",   "expected_count": 4},
    "MULI": {"opcode": "001101", "type": "two_reg",   "expected_count": 4},
    "DIVI": {"opcode": "001110", "type": "two_reg",   "expected_count": 4},

    # Memory instructions
    "LDR":  {"opcode": "010000", "type": "three_reg", "expected_count": 4},
    "STR":  {"opcode": "010001", "type": "three_reg", "expected_count": 4},
    "ADR":  {"opcode": "010010", "type": "reg_label", "expected_count": 3},

    # Branch instructions
    "B":    {"opcode": "100000", "type": "label",     "expected_count": 2},
    "BL":   {"opcode": "100001", "type": "label",     "expected_count": 2},
    "BEQ":  {"opcode": "100010", "type": "label",     "expected_count": 2},
    "BNE":  {"opcode": "100011", "type": "label",     "expected_count": 2},
    "BGT":  {"opcode": "100100", "type": "label",     "expected_count": 2},
    "BLT":  {"opcode": "100101", "type": "label",     "expected_count": 2},
    "BGE":  {"opcode": "100110", "type": "label",     "expected_count": 2},
    "BLE":  {"opcode": "100111", "type": "label",     "expected_count": 2},

    # Special instructions
    "NOP":  {"opcode": "110000", "type": "no_op",     "expected_count": 1},
    "RET":  {"opcode": "110001", "type": "no_op",     "expected_count": 1},
    # MOV is a special case where it can take either two registers or a register and an immediate value
    # So the only thing being used from its instruction set entry is the opcode
    "MOV":  {"opcode": "110010", "type": "dynamic",   "expected_count": 0},
    "CMP":  {"opcode": "110011", "type": "two_reg",   "expected_count": 3},
    "CBZ":  {"opcode": "110100", "type": "reg_label", "expected_count": 3},
    "CBNZ": {"opcode": "110101", "type": "reg_label", "expected_count": 3},
}

# this will be "label": "address" pairs where address is the next instruction's (relative to the label) address
labels = {}

# this will be "adr_label": "address" pairs where address is the index of the label in memory
adr_labels = {}

# read the input file
def read_file(file_name) -> list:
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        print("File not found")
        exit()

# resolve the register to its binary representation
def resolve_register(register) -> str:
    try:
        return registers[register.upper()]
    except KeyError:
        print("Error: Invalid register: " + register)
        sys.exit(1)

# resolve the instruction to its binary opcode representation
def resolve_opcode(opcode) -> str:
    try:
        return instruction_set[opcode.upper()]["opcode"]
    except KeyError:
        print("Error: Invalid opcode: " + opcode)
        sys.exit(1)

# resolve the immediate value to its binary representation
def resolve_immediate(imm) -> str:
    try:
        return format(int(imm), "012b")
    except ValueError:
        print("Error: Invalid immediate value: " + imm)
        sys.exit(1)

# resolve the label to its address
def resolve_label(label) -> str:
    try:
        return labels[label]
    except KeyError:
        print("Error: Invalid label: " + label)
        sys.exit(1)

# resolve the ADR label to its address
def resolve_adr_label(label) -> str:
    try:
        return adr_labels[label]
    except KeyError:
        print("Error: Invalid label: " + label)
        sys.exit(1)

# extract the text section from the input file
def extract_text(lines) -> list:
    text_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".text":
            for j in range(i+1, len(lines)):
                if lines[j].strip() == ".data":
                    break
                text_section.append(lines[j])

    return text_section

# tokenize the line
def tokenize_instruction(line) -> tuple:
    if line.startswith("//"):
        return None, [], None

    # Remove comments (start of line or after an instruction, //)
    line = re.sub(r"//.*", "", line)

    # Remove leading and trailing whitespaces
    line = line.strip()

    # Check if the line is empty
    if not line:
        return None, [], None

    instr = None
    operands = []
    label = None

    # Use regex to check if it's a label, ensuring no instruction follows (throw an error if it does)
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:$", line):
        label = line[:-1]
        return instr, operands, label

    # Validate formats using regex
    three_reg_pattern = r"^(ADD|SUB|MUL|DIV|AND|ORR|XOR|LSL|LSR|ASR) R\d{1,2}, R\d{1,2}, R\d{1,2}$"
    one_reg_pattern = r"^(NEG) R\d{1,2}$"
    three_reg_mem_pattern = r"^(LDR|STR) R\d{1,2}, \[R\d{1,2}, R\d{1,2}\]$"
    reg_label_pattern = r"^(ADR|CBZ|CBNZ) R\d{1,2}, [a-zA-Z_][a-zA-Z0-9_]*$"
    label_pattern = r"^(B|BEQ|BNE|BGT|BLT|BGE|BLE) [a-zA-Z_][a-zA-Z0-9_]*$"
    cmp_pattern = r"^(CMP) R\d{1,2}, R\d{1,2}$"
    nop_pattern = r"^(NOP)$"
    mov_pattern = r"^(MOV) R\d{1,2}, (R\d{1,2}|\d+)$"

    patterns = {
        "three_reg": three_reg_pattern,
        "one_reg": one_reg_pattern,
        "three_reg_mem": three_reg_mem_pattern,
        "reg_label": reg_label_pattern,
        "label": label_pattern,
        "cmp": cmp_pattern,
        "nop": nop_pattern,
        "mov": mov_pattern,
    }

    for instr_type, pattern in patterns.items():
        if re.match(pattern, line, re.IGNORECASE):
            tokens = re.split(r"\s|,", line)
            tokens = [token.strip() for token in tokens if token]
            instr = tokens[0].upper()
            operands = tokens[1:]
            return instr, operands, label

    # If no pattern matches, raise an error
    print(f"Error: Invalid instruction format in line: '{line}'")
    sys.exit(1)

def assemble_text_section(text_section) -> None:
    machine_code = []
    for line_number, line in enumerate(text_section, start=1):
        # Tokenize strictly: enforce operand separation and strip extra spaces
        instr, operands, label = tokenize_instruction(line)

        # If there's a label, store it and skip processing for now
        if label is not None:
            if label in labels:
                print(f"Error on line {line_number}: Label '{label}' already defined.")
                sys.exit(1)
            labels[label] = format(len(machine_code), "08b")
            continue

        # Skip empty lines or comment-only lines
        if instr is None:
            continue

        try:
            opcode = resolve_opcode(instr)
        except SystemExit:
            print(f"Error on line {line_number}: Invalid instruction '{instr}'. Snippet: {line.strip()}")
            sys.exit(1)

        try:
            if instruction_set[instr]["type"] == "three_reg":
                if len(operands) != (instruction_set[instr]["expected_count"] - 1):
                    raise ValueError(f"Expected {instruction_set[instr]['expected_count'] - 1} operands, found {len(operands) - 1}.")
                rd = resolve_register(operands[0])
                rn = resolve_register(operands[1])
                rm = resolve_register(operands[2])
                machine_code.append(opcode + rd + rn + rm)
            elif instruction_set[instr]["type"] == "label":
                if len(operands) != (instruction_set[instr]["expected_count"] - 1):
                    raise ValueError(f"Expected {instruction_set[instr]['expected_count']} - 1 operands, found {len(operands) - 1}.")
                label = operands[0].upper()
                machine_code.append(opcode + label)
            elif instruction_set[instr]["type"] == "two_reg":
                if len(operands) != (instruction_set[instr]["expected_count"] - 1):
                    raise ValueError(f"Expected {instruction_set[instr]['expected_count'] - 1} operands, found {len(operands) - 1}.")
                rd = resolve_register(operands[0])
                rn = resolve_register(operands[1])
                machine_code.append(opcode + rd + rn)
            elif instr == "MOV":
                if len(operands) != 2:
                    raise ValueError(f"Expected 3 operands, found {len(operands) - 1}.")
                if operands[1].upper() in registers:
                    rd = resolve_register(operands[0])
                    rn = resolve_register(operands[1])
                    machine_code.append(opcode + rd + rn + "0000000000")
                elif operands[1].isdigit():
                    rd = resolve_register(operands[0])
                    imm = resolve_immediate(operands[1])
                    machine_code.append(opcode + rd + imm)
                else:
                    raise ValueError(f"Invalid second operand '{operands[1]}'.")
            elif instruction_set[instr]["type"] == "one_reg":
                if len(operands) != (instruction_set[instr]["expected_count"] - 1):
                    raise ValueError(f"Expected {instruction_set[instr]['expected_count'] - 1} operands, found {len(operands) - 1}.")
                rd = resolve_register(operands[0])
                machine_code.append(opcode + rd)
            elif instruction_set[instr]["type"] == "reg_label":
                if len(operands) != (instruction_set[instr]["expected_count"] - 1):
                    raise ValueError(f"Expected {instruction_set[instr]['expected_count']} - 1 operands, found {len(operands) - 1}.")
                rd = resolve_register(operands[0])
                label = operands[1].upper()
                machine_code.append(opcode + rd + label)
            elif instruction_set[instr]["type"] == "no_op":
                machine_code.append(opcode + "00000000000000000000000000")
            else:
                raise ValueError("Unknown instruction type.")
        except ValueError as ve:
            print(f"Error on line {line_number}: {ve} Snippet: {line.strip()}")
            sys.exit(1)
        except KeyError as ke:
            print(f"Error on line {line_number}: Unknown operand '{ke.args[0]}'. Snippet: {line.strip()}")
            sys.exit(1)

    # Resolve labels to their addresses inplace
    for i, code in enumerate(machine_code):
        for label in labels:
            if label.upper() in code:
                machine_code[i] = code.replace(label.upper(), resolve_label(label))

    # Resolve ADR labels to their addresses
    for i, code in enumerate(machine_code):
        for label in adr_labels:
            if label.upper() in code:
                machine_code[i] = code.replace(label.upper(), resolve_adr_label(label))

    # Write the machine code to a file
    with open("instructions.o", "w") as f:
        f.write("v3.0 hex words addressed\n")
        for i, code in enumerate(machine_code):
            f.write("{:02x}: ".format(i) + hex(int(code, 2))[2:].zfill(8) + "\n")

    return

# extract the data section from the input file
def extract_data(lines) -> list:
    data_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".data":
            for j in range(i+1, len(lines)):
                if lines[j].strip() == ".text":
                    break
                data_section.append(lines[j])

    return data_section

def tokenize_data(line) -> tuple:
    if line.startswith("//"):
        return None, [], None

    # Remove comments (start of line or after an instruction, //)
    line = re.sub(r"//.*", "", line)

    # Remove leading and trailing whitespaces
    line = line.strip()

    # Split the line on spaces, then on commas
    tokens = re.split(r"\s|:", line)

    # Remove empty tokens
    tokens = [token for token in tokens if token]

    # Remove leading and trailing whitespaces from each token
    tokens = [token.strip() for token in tokens]

    label = None
    values = []

    # Check if the line is empty
    if not line:
        return label, values

    # Use regex to check if its a label, and make sure theres no instruction on the same line (throw an error)
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:$", line):
        if len(tokens) > 1:
            print(f"Error: Label '{line}' must be on its own line.")
            sys.exit(1)
        label = line[:-1]
        return label, values

    # based on what the instruction is, tokenize it accordingly
    label = tokens[0].strip()

    # Check if the label is already in the labels dictionary
    if label in labels:
        print(f"Error: Label '{label}' already defined.")
        sys.exit(1)

    # Check if the label is already in the adr_labels dictionary
    if label in adr_labels:
        print(f"Error: Label '{label}' already defined.")
        sys.exit(1)

    values = [token.strip() for token in tokens[1].split(",")]

    return label, values

# assemble the data section
def assemble_data_section(data_section) -> None:
    data = []
    for line_number, line in enumerate(data_section, start=1):
        label, values = tokenize_data(line)

        # Skip empty lines or comment-only lines
        if label is None:
            continue

        try:
            if len(values) == 1:
                data.append(values[0])
                # add to the adr_labels dictionary
                adr_labels[label] = format(len(data) - 1, "08b")
            else:
                data.extend(values)
        except ValueError as ve:
            print(f"Error on line {line_number}: {ve} Snippet: {line.strip()}")
            sys.exit(1)

    # Write the data to a file
    with open("ram.o", "w") as f:
        f.write("v3.0 hex words addressed\n")
        for i, value in enumerate(data):
            # f.write("{:02x}: ".format(i) + hex(int(value, 2))[2:].zfill(8) + "\n")
            # value is a string, so we need to convert it to an integer first
            value = int(value)
            f.write("{:02x}: ".format(i) + hex(value)[2:].zfill(8) + "\n")

    return

# main function
def main() -> None:
    parser = argparse.ArgumentParser(description="Assembler for the microRISC processor")
    parser.add_argument("input_file", help="The input file to be assembled")
    args = parser.parse_args()
    input_file = args.input_file

    # check if the file exists
    if not os.path.exists(input_file):
        print("Error: File not found")
        sys.exit(1)

    # check file extension
    if not input_file.endswith(".s"):
        print("Error: Invalid file extension")
        sys.exit(1)

    lines = read_file(input_file)

    # check if the file is empty
    if not lines:
        print("Error: Input file is empty")
        sys.exit(1)
    
    data_section = extract_data(lines)

    # check if the data section is empty
    if not data_section:
        print("Warning: No data section found")
    else:
        assemble_data_section(data_section)

    text_section = extract_text(lines)

    # check if the text section is empty
    if not text_section:
        print("Error: No text section found")
        sys.exit(1)
    else:
        assemble_text_section(text_section)
        
    return

if __name__ == "__main__":
    main()
