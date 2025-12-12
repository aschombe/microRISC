import sys

registers = {f"R{i}": format(i, "05b") for i in range(32)}
registers["ZR"] = registers["R0"]
registers["SP"] = registers["R30"]
registers["LR"] = registers["R31"]

instruction_set = {
    # ALU: OP Rd, Rn, Rm / Imm  (I bit in encoding)
    "ADD":  {"opcode": "000000", "kind": "alu",     "mnemonic": "ADD"},
    "SUB":  {"opcode": "000001", "kind": "alu",     "mnemonic": "SUB"},
    "MUL":  {"opcode": "000010", "kind": "alu",     "mnemonic": "MUL"},
    "DIV":  {"opcode": "000011", "kind": "alu",     "mnemonic": "DIV"},
    "AND":  {"opcode": "000100", "kind": "alu",     "mnemonic": "AND"},
    "ORR":  {"opcode": "000101", "kind": "alu",     "mnemonic": "ORR"},
    "XOR":  {"opcode": "000110", "kind": "alu",     "mnemonic": "XOR"},
    "LSL":  {"opcode": "000111", "kind": "alu",     "mnemonic": "LSL"},
    "LSR":  {"opcode": "001000", "kind": "alu",     "mnemonic": "LSR"},
    "ASR":  {"opcode": "001001", "kind": "alu",     "mnemonic": "ASR"},
    "NEG":  {"opcode": "001010", "kind": "neg",     "mnemonic": "NEG"},  # unary

    # Memory: LDR/STR Rd, [Rn, Rm/Imm], ADR Rd, Label
    "LDR":  {"opcode": "010000", "kind": "mem",     "mnemonic": "LDR"},
    "STR":  {"opcode": "010001", "kind": "mem",     "mnemonic": "STR"},
    "ADR":  {"opcode": "010010", "kind": "adr",     "mnemonic": "ADR"},  # PC-relative

    # Branches: PC-relative, 20-bit signed
    "B":    {"opcode": "100000", "kind": "branch",  "mnemonic": "B"},
    "BL":   {"opcode": "100001", "kind": "branch",  "mnemonic": "BL"},
    "BEQ":  {"opcode": "100010", "kind": "branch",  "mnemonic": "BEQ"},
    "BNE":  {"opcode": "100011", "kind": "branch",  "mnemonic": "BNE"},
    "BGT":  {"opcode": "100100", "kind": "branch",  "mnemonic": "BGT"},
    "BLT":  {"opcode": "100101", "kind": "branch",  "mnemonic": "BLT"},
    "BGE":  {"opcode": "100110", "kind": "branch",  "mnemonic": "BGE"},
    "BLE":  {"opcode": "100111", "kind": "branch",  "mnemonic": "BLE"},
    "CBZ":  {"opcode": "110101", "kind": "cb",      "mnemonic": "CBZ"},
    "CBNZ": {"opcode": "110110", "kind": "cb",      "mnemonic": "CBNZ"},

    # Special / misc
    "NOP":  {"opcode": "110000", "kind": "nop",     "mnemonic": "NOP"},
    "RET":  {"opcode": "110001", "kind": "ret",     "mnemonic": "RET"},
    "MOV":  {"opcode": "110010", "kind": "mov",     "mnemonic": "MOV"},  # ALU-like
    "CMP":  {"opcode": "110100", "kind": "cmp",     "mnemonic": "CMP"},  # Rn, Rm/Imm
}

def resolve_register(reg: str) -> str:
    try:
        return registers[reg.upper()]
    except KeyError:
        print(f"Error: Invalid register: {reg}")
        sys.exit(1)


def resolve_opcode(mnemonic: str) -> str:
    try:
        return instruction_set[mnemonic.upper()]["opcode"]
    except KeyError:
        print(f"Error: Invalid opcode: {mnemonic}")
        sys.exit(1)


def parse_immediate(imm_str: str, bits: int, signed: bool = False) -> str:
    """
    Parse an immediate and return a bits-wide binary string, with optional sign-extension.
    """
    try:
        val = int(imm_str, 0)  # supports decimal, 0x.., 0b..
    except ValueError:
        print(f"Error: Invalid immediate value: {imm_str}")
        sys.exit(1)

    if signed:
        min_val = -(1 << (bits - 1))
        max_val = (1 << (bits - 1)) - 1
        if val < min_val or val > max_val:
            print(f"Error: Signed immediate {val} out of range for {bits} bits.")
            sys.exit(1)
        if val < 0:
            val = (1 << bits) + val
    else:
        if val < 0 or val >= (1 << bits):
            print(f"Error: Unsigned immediate {val} out of range for {bits} bits.")
            sys.exit(1)

    return format(val, f"0{bits}b")
