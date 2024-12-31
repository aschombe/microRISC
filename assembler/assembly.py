import sys

from instruction_set import registers, instruction_set, resolve_register, resolve_opcode, resolve_immediate
from tokenize import tokenize_instruction, tokenize_data

def resolve_label(label, labels) -> str:
    try:
        return labels[label]
    except KeyError:
        print(f"Error: Invalid label: {label}")
        sys.exit(1)

def resolve_adr_label(label, adr_labels) -> str:
    try:
        return adr_labels[label]
    except KeyError:
        print(f"Error: Invalid label: {label}")
        sys.exit(1)

def assemble_text_section(text_section, labels, adr_labels) -> None:
    machine_code = []
    prev_write = None  # register written by the last instruction
    prev_prev_write = None  # register written two instructions ago

    for line_number, line in enumerate(text_section, start=1):
        # tokenize strictly: enforce operand separation and strip extra spaces
        instr, operands, label = tokenize_instruction(line)

        # if there's a label, store it and skip processing for now
        if label is not None:
            if label in labels:
                print(f"Error on line {line_number}: Label '{label}' already defined.")
                sys.exit(1)
            labels[label] = format(len(machine_code), "08b")
            continue

        # skip empty lines or comment-only lines
        if instr is None:
            continue

        try:
            opcode = resolve_opcode(instr)
        except SystemExit:
            print(f"Error on line {line_number}: Invalid instruction '{instr}'. Snippet: {line.strip()}")
            sys.exit(1)

        curr_access = []
        encoded_instruction = ""

        try:
            # identify accessed registers based on instruction type
            if instruction_set[instr]["type"] == "three_reg":
                if len(operands) != 3:
                    raise ValueError(f"Expected 3 operands, found {len(operands)}.")
                rd = resolve_register(operands[0])
                rn = resolve_register(operands[1])
                rm = resolve_register(operands[2])
                curr_access = [rn, rm]
                encoded_instruction = opcode + rd + rn + rm
            elif instruction_set[instr]["type"] == "two_reg" and instr.endswith("I"):  # immediate variant
                if len(operands) != 3:
                    raise ValueError(f"Expected 3 operands, found {len(operands)}.")
                rd = resolve_register(operands[0])
                rn = resolve_register(operands[1])
                imm = resolve_immediate(operands[2])
                curr_access = [rn]
                encoded_instruction = opcode + rd + rn + imm
            elif instruction_set[instr]["type"] == "two_reg":
                if len(operands) != 2:
                    raise ValueError(f"Expected 2 operands, found {len(operands)}.")
                rd = resolve_register(operands[0])
                rn = resolve_register(operands[1])
                curr_access = [rn]
                encoded_instruction = opcode + rd + rn
            elif instr == "MOV":
                if len(operands) != 2:
                    raise ValueError(f"Expected 2 operands, found {len(operands)}.")
                rd = resolve_register(operands[0])
                if operands[1].upper() in registers:
                    rn = resolve_register(operands[1])
                    curr_access = [rn]
                    encoded_instruction = opcode + rd + rn + "0000000000"
                else:
                    raise ValueError(f"Invalid second operand '{operands[1]}'.")
            elif instr == "MOVI":
                if len(operands) != 2:
                    raise ValueError(f"Expected 2 operands, found {len(operands)}.")
                rd = resolve_register(operands[0])
                imm = resolve_immediate(operands[1])
                encoded_instruction = opcode + rd + imm
            elif instruction_set[instr]["type"] == "one_reg":
                if len(operands) != 1:
                    raise ValueError(f"Expected 1 operand, found {len(operands)}.")
                rd = resolve_register(operands[0])
                encoded_instruction = opcode + rd
            elif instruction_set[instr]["type"] == "reg_label":
                if len(operands) != 2:
                    raise ValueError(f"Expected 2 operands, found {len(operands)}.")
                rd = resolve_register(operands[0])
                label = operands[1].upper()
                curr_access = [rd]
                encoded_instruction = opcode + rd + label
            elif instruction_set[instr]["type"] == "no_op":
                encoded_instruction = opcode + "00000000000000000000000000"
            else:
                raise ValueError("Unknown instruction type.")
            
            # insert NOPs before dependent instructions
            hazard_detected = False
            for reg in curr_access:
                if reg == prev_write or reg == prev_prev_write:
                    machine_code.append(resolve_opcode("NOP") + "00000000000000000000000000")
                    hazard_detected = True

            if hazard_detected:
                # re-check previous writes to cover multiple hazards
                prev_prev_write = prev_write
                prev_write = None

            # add the current instruction
            machine_code.append(encoded_instruction)

            # update dependency tracking
            prev_prev_write = prev_write

            if instruction_set[instr]["type"] in ["three_reg", "two_reg"]:
                prev_write = rd
            else:
                prev_write = None

        except ValueError as ve:
            print(f"Error on line {line_number}: {ve} Snippet: {line.strip()}")
            sys.exit(1)
        except KeyError as ke:
            print(f"Error on line {line_number}: Unknown operand '{ke.args[0]}'. Snippet: {line.strip()}")
            sys.exit(1)

    # resolve labels to their addresses inplace
    for i, code in enumerate(machine_code):
        for label in labels:
            if label.upper() in code:
                machine_code[i] = code.replace(label.upper(), resolve_label(label, labels))

    # resolve adr labels to their addresses
    for i, code in enumerate(machine_code):
        for label in adr_labels:
            if label.upper() in code:
                machine_code[i] = code.replace(label.upper(), resolve_adr_label(label, adr_labels))

    # write the machine code to a file
    with open("instructions.o", "w") as f:
        f.write("v3.0 hex words addressed\n")
        for i, code in enumerate(machine_code):
            f.write("{:02x}: ".format(i) + hex(int(code, 2))[2:].zfill(8) + "\n")

    return

def assemble_data_section(data_section, labels, adr_labels) -> None:
    data = []
    for line_number, line in enumerate(data_section, start=1):
        label, values = tokenize_data(line, labels, adr_labels)

        # skip empty lines or comment-only lines
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

    # write the data to a file
    with open("ram.o", "w") as f:
        f.write("v3.0 hex words addressed\n")
        for i, value in enumerate(data):
            value = int(value)
            f.write("{:02x}: ".format(i) + hex(value)[2:].zfill(8) + "\n")

    return