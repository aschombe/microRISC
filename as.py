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
    "NOP":  {"opcode": "000000", "type": "no_op",     "expected_count": 1},
    "ADD":  {"opcode": "000001", "type": "three_reg", "expected_count": 4},
    "SUB":  {"opcode": "000011", "type": "three_reg", "expected_count": 4},
    "MUL":  {"opcode": "000101", "type": "three_reg", "expected_count": 4},
    "DIV":  {"opcode": "001001", "type": "three_reg", "expected_count": 4},
    "AND":  {"opcode": "010001", "type": "three_reg", "expected_count": 4},
    "ORR":  {"opcode": "100001", "type": "three_reg", "expected_count": 4},
    "XOR":  {"opcode": "000111", "type": "three_reg", "expected_count": 4},
    "LSL":  {"opcode": "001101", "type": "three_reg", "expected_count": 4},
    "LSR":  {"opcode": "011001", "type": "three_reg", "expected_count": 4},
    "ASR":  {"opcode": "110001", "type": "three_reg", "expected_count": 4},
    "LDR":  {"opcode": "000010", "type": "three_reg", "expected_count": 4},
    "STR":  {"opcode": "000110", "type": "three_reg", "expected_count": 4},
    "B":    {"opcode": "bOpcod", "type": "label",     "expected_count": 2},
    "BL":   {"opcode": "blOpco", "type": "label",     "expected_count": 2},
    "BEQ":  {"opcode": "beqOpc", "type": "label",     "expected_count": 2},
    "BNE":  {"opcode": "bneOpc", "type": "label",     "expected_count": 2},
    "BGT":  {"opcode": "bgtOpc", "type": "label",     "expected_count": 2},
    "BLT":  {"opcode": "bltOpc", "type": "label",     "expected_count": 2},
    "BGE":  {"opcode": "bgeOpc", "type": "label",     "expected_count": 2},
    "BLE":  {"opcode": "bleOpc", "type": "label",     "expected_count": 2},
    "CMP":  {"opcode": "cmpOpc", "type": "two_reg",   "expected_count": 3},
    "CBZ":  {"opcode": "cbzOpc", "type": "reg_label", "expected_count": 3},
    "CBNZ": {"opcode": "cbnzOp", "type": "reg_label", "expected_count": 3},
    "RET":  {"opcode": "retOpc", "type": "no_op",     "expected_count": 1},
    "ADR":  {"opcode": "adrOpc", "type": "reg_label", "expected_count": 3},
    "NEG":  {"opcode": "negOpc", "type": "one_reg",   "expected_count": 2},
    "MOV":  {"opcode": "movOpc", "type": "dynamic",   "expected_count": 0},
}

def read_file(file_name) -> list:
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        print("File not found")
        exit()

def resolve_register(register) -> str:
    try:
        return registers[register.upper()]
    except KeyError:
        print("Error: Invalid register: " + register)
        sys.exit(1)

def resolve_opcode(opcode) -> str:
    try:
        return instruction_set[opcode.upper()]["opcode"]
    except KeyError:
        print("Error: Invalid opcode: " + opcode)
        sys.exit(1)

def resolve_immediate(imm) -> str:
    try:
        return format(int(imm), "012b")
    except ValueError:
        print("Error: Invalid immediate value: " + imm)
        sys.exit(1)

def resolve_label(label) -> str:
    print("Warning: Label resolution not supported yet")
    return

def extract_text(lines) -> list:
    text_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".text":
            for j in range(i+1, len(lines)):
                if lines[j].strip() == ".data":
                    break
                text_section.append(lines[j])

    return text_section

def assemble_text_section(text_section) -> None:
    machine_code = [] 
    for line in text_section:
        tokens = line.replace(",", " ").replace("[", " ").replace("]", " ").replace("#", " ").split()

        if not tokens:
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
                label = tokens[1]
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
                label = tokens[2]
                machine_code.append(opcode + rd + label)
        elif instruction_set[instr]["type"] == "no_op":
            machine_code.append(opcode + "00000000000000000000000000")
        else:
            print("Error: Invalid instruction: " + instr)
            sys.exit(1)

    if os.path.exists("instructions.o"):
        os.remove("instructions.o")

    with open("instructions.o", "w") as f:
        f.write("v3.0 hex words addressed\n")
        for i, code in enumerate(machine_code):
            f.write("{:02x}: ".format(i) + hex(int(code, 2))[2:].zfill(8) + "\n")

    return

def extract_data(lines) -> list:
    data_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".data":
            for j in range(i+1, len(lines)):
                if lines[j].strip() == ".text":
                    break
                data_section.append(lines[j])

    return data_section

def assemble_data_section(data_section) -> None:
    print("Warning: Data section not supported yet")
    return

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 as.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("Error: File not found")
        sys.exit(1)

    lines = read_file(input_file)

    if not lines:
        print("Error: Input file is empty")
        sys.exit(1)
    
    text_section = extract_text(lines)

    if not text_section:
        print("Error: No text section found")
        sys.exit(1)
    else:
        assemble_text_section(text_section)

    data_section = extract_data(lines)

    if not data_section:
        print("Warning: No data section found")
    else:
        assemble_data_section(data_section)
    
    return

if __name__ == "__main__":
    main()
