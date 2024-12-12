import argparse
import sys
import os

# populate the registers (R0-R31, SP (R30), CMP (R31))
registers = { }
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
    # So the only thing being used from the instruction set is the opcode
    "MOV":  {"opcode": "110010", "type": "dynamic",   "expected_count": 0},
    "CMP":  {"opcode": "110011", "type": "two_reg",   "expected_count": 3},
    "CBZ":  {"opcode": "110100", "type": "reg_label", "expected_count": 3},
    "CBNZ": {"opcode": "110101", "type": "reg_label", "expected_count": 3},
}

# this will be "label": "address" pairs where address is the next instruction's address
labels = { }

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
        return labels[label.upper()]
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

# assemble the text section
def assemble_text_section(text_section) -> None:
    machine_code = [] 
    for line in text_section:
        tokens = line.replace(",", " ").replace("[", " ").replace("]", " ").replace("#", " ").replace("//", " // ").replace("/*", " /* ").replace("*/", " */ ").split()

        # skip empty lines and comments
        if not tokens or tokens[0] == "//":
            continue

        # add support for comments at the end of the line
        if "//" in tokens:
            tokens = tokens[:tokens.index("//")]
        
        # check if the line is a label
        if tokens[0][-1] == ":":
            labels[tokens[0][:-1].upper()] = format(len(machine_code), "08b")
            tokens = tokens[1:]
            continue

        instr = tokens[0].upper()

        opcode = resolve_opcode(instr)

        if instruction_set[instr]["type"] == "three_reg":
            if len(tokens) != instruction_set[instr]["expected_count"]:
                print("Error: Invalid number of operands for " + instr)
                sys.exit(1)
            else:
                rd = resolve_register(tokens[1])
                rn = resolve_register(tokens[2])
                rm = resolve_register(tokens[3])
                machine_code.append(opcode + rd + rn + rm)
        elif instruction_set[instr]["type"] == "label":
            if len(tokens) != instruction_set[instr]["expected_count"]:
                print("Error: Invalid number of operands for " + instr)
                sys.exit(1)
            else:
                label = tokens[1].upper()
                machine_code.append(opcode + label)
        elif instruction_set[instr]["type"] == "two_reg":
            if len(tokens) != instruction_set[instr]["expected_count"]:
                print("Error: Invalid number of operands for " + instr)
                sys.exit(1)
            else:
                rd = resolve_register(tokens[1])
                rn = resolve_register(tokens[2])
                machine_code.append(opcode + rd + rn)
        elif instr == "MOV":
            if len(tokens) == 3:
                rd = resolve_register(tokens[1])
                rn = resolve_register(tokens[2])
                machine_code.append(opcode + rd + rn + "0000000000")
            elif len(tokens) == 4:
                rd = resolve_register(tokens[1])
                imm = resolve_immediate(tokens[2])
                machine_code.append(opcode + rd + imm)
            else:
                print("Error: Invalid number of operands for " + instr)
                sys.exit(1)
        elif instruction_set[instr]["type"] == "one_reg":
            if len(tokens) != instruction_set[instr]["expected_count"]:
                print("Error: Invalid number of operands for " + instr)
                sys.exit(1)
            else:
                rd = resolve_register(tokens[1])
                machine_code.append(opcode + rd)
        elif instruction_set[instr]["type"] == "reg_label":
            if len(tokens) != instruction_set[instruction_set]["expected_count"]:
                print("Error: Invalid number of operands for " + instr)
                sys.exit(1)
            else:
                rd = resolve_register(tokens[1])
                label = tokens[2].upper()
                machine_code.append(opcode + rd + label)
        elif instruction_set[instr]["type"] == "no_op":
            machine_code.append(opcode + "00000000000000000000000000")
        else:
            print("Error: Invalid instruction: " + instr)
            sys.exit(1)

    # remove the old instructions.o file if it exists
    if os.path.exists("instructions.o"):
        os.remove("instructions.o")

    # resolve labels to their addresses inplace
    for i, code in enumerate(machine_code):
        for label in labels:
            if label in code:
                machine_code[i] = code.replace(label, resolve_label(label))

    # write the machine code to a file
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
