import sys

# Registers and instructions
registers = {f"R{i}": format(i, "05b") for i in range(32)}
registers["CMP"] = "11110"
registers["LR"] = "11111"

instruction_set = {
    # expected count is the expected number of tokens in the instruction's line (including the instruction itself)
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
    "MOV":  {"opcode": "110010", "type": "dynamic",   "expected_count": 0},
    "MOVI": {"opcode": "110011", "type": "dynamic",   "expected_count": 0},
    "CMP":  {"opcode": "110100", "type": "two_reg",   "expected_count": 3},
    "CBZ":  {"opcode": "110101", "type": "reg_label", "expected_count": 3},
    "CBNZ": {"opcode": "110110", "type": "reg_label", "expected_count": 3},
}

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