#!/usr/bin/python

import argparse
import sys
import os
import re

# populate the registers (R0-R31, SP (R30), CMP (R31))
registers = {}
for i in range(32):
    registers["R" + str(i)] = format(i, "05b")
registers["SP"] = "11110"
registers["CMP"] = "11111"

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

    # Memory instructions
    "LDR":  {"opcode": "010000", "type": "three_reg", "expected_count": 4},
    "STR":  {"opcode": "010001", "type": "three_reg", "expected_count": 4},
    "ADR":  {"opcode": "010010", "type": "reg_label", "expected_count": 3},

    # Branch instructions
    "B":    {"opcode": "100000", "type": "label",     "expected_count": 2},
    # "BL":   {"opcode": "100001", "type": "label",     "expected_count": 2},
    "BEQ":  {"opcode": "100010", "type": "label",     "expected_count": 2},
    "BNE":  {"opcode": "100011", "type": "label",     "expected_count": 2},
    "BGT":  {"opcode": "100100", "type": "label",     "expected_count": 2},
    "BLT":  {"opcode": "100101", "type": "label",     "expected_count": 2},
    "BGE":  {"opcode": "100110", "type": "label",     "expected_count": 2},
    "BLE":  {"opcode": "100111", "type": "label",     "expected_count": 2},

    # Special instructions
    "NOP":  {"opcode": "110000", "type": "no_op",     "expected_count": 1},
    # "RET":  {"opcode": "110001", "type": "no_op",     "expected_count": 1},
    # MOV is a special case where it can take either two registers or a register and an immediate value
    # So the only thing being used from its instruction set entry is the opcode
    "MOV":  {"opcode": "110010", "type": "dynamic",   "expected_count": 0},
    "CMP":  {"opcode": "110011", "type": "two_reg",   "expected_count": 3},
    "CBZ":  {"opcode": "110100", "type": "reg_label", "expected_count": 3},
    "CBNZ": {"opcode": "110101", "type": "reg_label", "expected_count": 3},
}

# this will be "label": "address" pairs where address is the next instruction's (relative to the label) address
labels = {}

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
    # instruction name and operands should be case insensitive
    # Strict tokenization, each instruction, after spaces are stripped, must follow a format depending on the instruction
    # Spacing between operands is not enforced (e.g ADD R0,R1,R2 is valid)
    # Labels MUST be on their own line (can't have an instruction follow)
    # Instruction types:
    # 1. Three register instructions: ADD, SUB, MUL, DIV, AND, ORR, XOR, LSL, LSR, ASR
    # Format: <INSTRUCTION> <Rd>, <Rn>, <Rm>
    # 2. One register instructions: NEG
    # Format: <INSTRUCTION> <Rd>
    # 3. Three Register bracketed instructions: LDR, STR
    # Format <INSTRUCTION> <Rd>, [<Rn>, <Rm>]
    # 4. Register label instructions: ADR, CBZ, CBNZ
    # Format: <INSTRUCTION> <Rd>, <label>
    # 5. Label instructions: B, BEQ, BNE, BGT, BLT, BGE, BLE
    # Format: <INSTRUCTION> <label>
    # 6. Two register instructions: CMP
    # Format: <INSTRUCTION> <Rn>, <Rm>
    # 7. No operand instructions: NOP
    # Format: <INSTRUCTION>
    # 8. MOV instruction: MOV
    # Format: MOV <Rd>, <Rn> or MOV <Rd>, <imm>
    
    if line.startswith("//"):
        return None, [], None

    # Remove comments (start of line or after an instruction, //)
    line = re.sub(r"//.*", "", line)

    # Remove leading and trailing whitespaces
    line = line.strip()

    # Split the line on spaces, then on commas
    tokens = re.split(r"\s|,", line)

    # Remove empty tokens
    tokens = [token for token in tokens if token]

    # Remove leading and trailing whitespaces from each token
    tokens = [token.strip() for token in tokens]

    instr = None
    operands = []
    label = None

    # Check if the line is empty
    if not line:
        return instr, operands, label

    # Use regex to check if its a label, and make sure theres no instruction on the same line (throw an error)
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:$", line):
        if len(tokens) > 1:
            print(f"Error: Label '{line}' must be on its own line.")
            sys.exit(1)
        label = line[:-1]
        return instr, operands, label

    # based on what the instruction is, tokenize it accordingly
    instr = tokens[0].strip().upper()

    if instr in ["ADD", "SUB", "MUL", "DIV", "AND", "ORR", "XOR", "LSL", "LSR", "ASR"]:
        # check if the instruction is of the form <INSTRUCTION> <Rd>, <Rn>, <Rm>
        if len(tokens) != 4:
            print(f"Error: Expected 3 operands in '{line}'.")
            sys.exit(1)
        operands = [tokens[1].strip(), tokens[2].strip(), tokens[3].strip()]
    elif instr == "NEG":
        if len(tokens) != 2:
            print(f"Error: Expected 1 operand in '{line}'.")
            sys.exit(1)
        operands = [tokens[1].strip()]
    elif instr in ["LDR", "STR"]:
        if len(tokens) != 4:
            print(f"Error: Expected 3 operands in '{line}'.")
            sys.exit(1)
        if tokens[2][0] != "[" or tokens[3][-1] != "]":
            print(f"Error: Expected '[' and ']' around memory operands in '{line}'.")
            sys.exit(1)
        operands = [tokens[1].strip(), tokens[2].strip()[1:], tokens[3].strip()[:-1]]
    elif instr in ["ADR", "CBZ", "CBNZ"]:
        if len(tokens) != 3:
            print(f"Error: Expected 2 operands in '{line}'.")
            sys.exit(1)
        operands = [tokens[1].strip(), tokens[2].strip()]
    elif instr in ["B", "BEQ", "BNE", "BGT", "BLT", "BGE", "BLE"]:
        if len(tokens) != 2:
            print(f"Error: Expected 1 operand in '{line}'.")
            sys.exit(1)
        operands = [tokens[1].strip()]
    elif instr == "CMP":
        if len(tokens) != 3:
            print(f"Error: Expected 2 operands in '{line}'.")
            sys.exit(1)
        operands = [tokens[1].strip(), tokens[2].strip()]
    elif instr == "NOP":
        if len(tokens) != 1:
            print(f"Error: Expected no operands in '{line}'.")
            sys
    elif instr == "MOV":
        if len(tokens) != 3:
            print(f"Error: Expected 2 operands in '{line}'.")
            sys.exit(1)
        operands = [tokens[1].strip(), tokens[2].strip()]
    else:
        print(f"Error: Unknown instruction '{instr}'.")
        sys.exit(1)

    return instr, operands, label

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

# assemble the data section
def assemble_data_section(data_section) -> None:
    print("Warning: Data section not supported yet")
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
    
    text_section = extract_text(lines)

    # check if the text section is empty
    if not text_section:
        print("Error: No text section found")
        sys.exit(1)
    else:
        assemble_text_section(text_section)

    data_section = extract_data(lines)

    # check if the data section is empty
    if not data_section:
        print("Warning: No data section found")
    else:
        assemble_data_section(data_section)
    
    return

if __name__ == "__main__":
    main()
