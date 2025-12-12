import sys

from instruction_set import (
    registers,
    instruction_set,
    resolve_register,
    resolve_opcode,
    parse_immediate,
)
from tokenize import (
    tokenize_instruction,
    tokenize_data_line,
    extract_data,
    extract_text,
)


def assemble_text_section(text_section, labels, adr_labels):
    """
    Two-pass assembly for text:
    - Pass 1: collect labels and instruction skeletons
    - Pass 2: encode instructions into 32-bit words
    """
    instructions = []
    pc = 0  # word address

    # Pass 1: collect labels and instruction skeletons
    for line_number, line in enumerate(text_section, start=1):
        label, instr, operands = tokenize_instruction(line)

        if label is not None:
            if label in labels:
                print(f"Error on line {line_number}: Label '{label}' already defined.")
                sys.exit(1)
            labels[label] = pc

        if instr is None:
            continue

        mnem = instr.upper()
        if mnem not in instruction_set:
            print(f"Error on line {line_number}: Unknown instruction '{instr}'.")
            sys.exit(1)

        instructions.append(
            {
                "line_number": line_number,
                "line": line.rstrip("\n"),
                "label": label,
                "mnemonic": mnem,
                "operands": operands,
                "pc": pc,
            }
        )
        pc += 1

    # Pass 2: encode instructions
    machine_words = []

    for inst in instructions:
        line_number = inst["line_number"]
        mnem = inst["mnemonic"]
        operands = inst["operands"]
        pc = inst["pc"]

        meta = instruction_set[mnem]
        kind = meta["kind"]
        opcode_bits = meta["opcode"]

        try:
            if kind == "alu":
                word = encode_alu(mnem, opcode_bits, operands, line_number)
            elif kind == "neg":
                word = encode_neg(opcode_bits, operands, line_number)
            elif kind == "mem":
                word = encode_mem(mnem, opcode_bits, operands, line_number)
            elif kind == "adr":
                word = encode_adr(opcode_bits, operands, labels, pc, line_number)
            elif kind == "branch":
                word = encode_branch(mnem, opcode_bits, operands, labels, pc, line_number)
            elif kind == "cb":
                word = encode_cb(mnem, opcode_bits, operands, labels, pc, line_number)
            elif kind == "nop":
                word = opcode_bits + "0" * (32 - 6)
            elif kind == "ret":
                word = opcode_bits + "0" * (32 - 6)
            elif kind == "mov":
                word = encode_mov(opcode_bits, operands, line_number)
            elif kind == "cmp":
                word = encode_cmp(opcode_bits, operands, line_number)
            else:
                raise ValueError(f"Unsupported instruction kind '{kind}'.")

            machine_words.append(word)

        except ValueError as ve:
            print(f"Error on line {line_number}: {ve} Snippet: {inst['line']}")
            sys.exit(1)

    with open("instructions.hex", "w") as f:
        f.write("v3.0 hex words addressed\n")
        for i, word in enumerate(machine_words):
            f.write(f"{i:02x}: {int(word, 2):08x}\n")



def encode_alu(mnem, opcode_bits, operands, line_number) -> str:
    if len(operands) != 3:
        raise ValueError(f"{mnem} expects 3 operands (Rd, Rn, Rm/Imm).")

    rd_str, rn_str, op2_str = operands
    rd = resolve_register(rd_str)
    rn = resolve_register(rn_str)

    if op2_str.upper() in registers:
        rm = resolve_register(op2_str)
        I = "0"
        rm_bits = rm
        imm_bits = "0" * 10
    else:
        I = "1"
        rm_bits = "0" * 5
        imm_bits = parse_immediate(op2_str, 10, signed=False)

    word = (
        opcode_bits +    # 31..26
        I +              # 25
        rd +             # 24..20
        rn +             # 19..15
        rm_bits +        # 14..10
        imm_bits         # 9..0
    )
    return word


def encode_neg(opcode_bits, operands, line_number) -> str:
    if len(operands) != 1:
        raise ValueError("NEG expects 1 operand (Rd).")
    rd = resolve_register(operands[0])
    I = "0"
    rn = rd
    rm_bits = "0" * 5
    imm_bits = "0" * 10
    word = opcode_bits + I + rd + rn + rm_bits + imm_bits
    return word


def encode_mem(mnem, opcode_bits, operands, line_number) -> str:
    """
    LDR/STR Rd, [Rn, Rm/Imm]
    Operands like: ["R0", "[", "R1", "R2", "]"] or ["R0", "[", "R1", "4", "]"]
    """
    if len(operands) < 4:
        raise ValueError(f"{mnem} expects syntax: {mnem} Rd, [Rn, Rm/Imm].")

    rd_str = operands[0]
    if operands[1] != "[" or operands[-1] != "]":
        raise ValueError(f"{mnem} expects memory operand in brackets: [Rn, Rm/Imm].")

    rn_str = operands[2]
    op2_str = operands[3]

    rd = resolve_register(rd_str)
    rn = resolve_register(rn_str)

    if op2_str.upper() in registers:
        rm = resolve_register(op2_str)
        I = "0"
        rm_bits = rm
        imm_bits = "0" * 10
    else:
        I = "1"
        rm_bits = "0" * 5
        imm_bits = parse_immediate(op2_str, 10, signed=False)

    word = opcode_bits + I + rd + rn + rm_bits + imm_bits
    return word


def encode_mov(opcode_bits, operands, line_number) -> str:
    if len(operands) != 2:
        raise ValueError("MOV expects 2 operands (Rd, Rn/Imm).")
    rd_str, op2_str = operands
    rd = resolve_register(rd_str)
    rn = "00000"  # MOV Rd, op2 => treat Rn as zero

    if op2_str.upper() in registers:
        rm = resolve_register(op2_str)
        I = "0"
        rm_bits = rm
        imm_bits = "0" * 10
    else:
        I = "1"
        rm_bits = "0" * 5
        imm_bits = parse_immediate(op2_str, 10, signed=False)

    word = opcode_bits + I + rd + rn + rm_bits + imm_bits
    return word


def encode_cmp(opcode_bits, operands, line_number) -> str:
    if len(operands) != 2:
        raise ValueError("CMP expects 2 operands (Rn, Rm/Imm).")
    rn_str, op2_str = operands
    rn = resolve_register(rn_str)
    rd = "00000"  # unused

    if op2_str.upper() in registers:
        rm = resolve_register(op2_str)
        I = "0"
        rm_bits = rm
        imm_bits = "0" * 10
    else:
        I = "1"
        rm_bits = "0" * 5
        imm_bits = parse_immediate(op2_str, 10, signed=False)

    word = opcode_bits + I + rd + rn + rm_bits + imm_bits
    return word


# -----------------------------
# ADR / Branch / CBZ / CBNZ (20-bit Offset layout)
# Layout:
# 31..26 opcode
# 25    unused
# 24..20 unused
# 19..15 Rn (only for CBZ/CBNZ; otherwise 0)
# 19..0  Offset (signed, 20 bits)
# -----------------------------

def encode_adr(opcode_bits, operands, labels, pc, line_number) -> str:
    if len(operands) != 2:
        raise ValueError("ADR expects 2 operands (Rd, Label).")
    rd_str, label = operands
    rd = resolve_register(rd_str)

    if label not in labels:
        raise ValueError(f"Unknown label '{label}' for ADR.")

    target = labels[label]
    offset = target - (pc + 1)
    offset_bits = parse_immediate(str(offset), 20, signed=True)

    # Layout: opcode (6) | 0 (1) | unused (5) | Rn (5) | Offset(20)
    # For ADR, Rn is not used; keep 0. Offset uses bits 19..0.
    I = "0"
    unused_rd = "00000"
    rn = "00000"
    word = (
        opcode_bits +
        I +
        unused_rd +
        rn +
        offset_bits
    )
    return word


def encode_branch(mnem, opcode_bits, operands, labels, pc, line_number) -> str:
    if len(operands) != 1:
        raise ValueError(f"{mnem} expects 1 operand (Label).")
    label = operands[0]
    if label not in labels:
        raise ValueError(f"Unknown label '{label}' for branch '{mnem}'.")

    target = labels[label]
    offset = target - (pc + 1)
    offset_bits = parse_immediate(str(offset), 20, signed=True)

    I = "0"
    unused_rd = "00000"
    rn = "00000"  # Rn unused for B/BL/BEQ/...
    word = (
        opcode_bits +
        I +
        unused_rd +
        rn +
        offset_bits
    )
    return word


def encode_cb(mnem, opcode_bits, operands, labels, pc, line_number) -> str:
    if len(operands) != 2:
        raise ValueError(f"{mnem} expects 2 operands (Rn, Label).")
    rn_str, label = operands
    rn = resolve_register(rn_str)

    if label not in labels:
        raise ValueError(f"Unknown label '{label}' for {mnem}.")

    target = labels[label]
    offset = target - (pc + 1)
    offset_bits = parse_immediate(str(offset), 20, signed=True)

    I = "0"
    unused_rd = "00000"
    word = (
        opcode_bits +
        I +
        unused_rd +
        rn +
        offset_bits
    )
    return word


def assemble_data_section(data_section, labels, adr_labels):
    """
    Minimal data support can be added later.
    """
    pass
