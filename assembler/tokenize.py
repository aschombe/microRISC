import re, sys

# class Tokenizer:
#     def __init__(self, lines):
#         self.lines = lines
#         self.labels = {}
#         self.adr_labels = {}
#         self.instructions = []
#         self.data = []

#     def extract_text(self) -> list:
#         text_section = []
#         for i, line in enumerate(self.lines):
#             if line.strip() == ".text":
#                 for j in range(i + 1, len(self.lines)):
#                     if self.lines[j].strip() == ".data":
#                         break
#                     text_section.append(self.lines[j])
#         return text_section
    
#     def extract_data(self) -> list:
#         data_section = []
#         for i, line in enumerate(self.lines):
#             if line.strip() == ".data":
#                 for j in range(i + 1, len(self.lines)):
#                     if self.lines[j].strip() == ".text":
#                         break
#                     data_section.append(self.lines[j])
#         return data_section
    
#     def tokenize_instruction(self, line) -> tuple:
#         if line.startswith("//"):
#             return None, [], None

#         line = re.sub(r"//.*", "", line)
#         line = line.strip()
#         if not line:
#             return None, [], None

#         instr = None
#         operands = []
#         label = None

#         if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:$", line):
#             label = line[:-1]
#             return instr, operands, label

#         two_reg_imm_pattern = r"^(ADDI|SUBI|MULI|DIVI) R\d{1,2}, R\d{1,2}, \d+$"
#         three_reg_pattern = r"^(ADD|SUB|MUL|DIV|AND|ORR|XOR|LSL|LSR|ASR) R\d{1,2}, R\d{1,2}, R\d{1,2}$"
#         one_reg_pattern = r"^(NEG) R\d{1,2}$"
#         three_reg_mem_pattern = r"^(LDR|STR) R\d{1,2}, \[R\d{1,2}, R\d{1,2}\]$"
#         reg_label_pattern = r"^(ADR|CBZ|CBNZ) R\d{1,2}, [a-zA-Z_][a-zA-Z0-9_]*$"
#         label_pattern = r"^(B|BEQ|BNE|BGT|BLT|BGE|BLE) [a-zA-Z_][a-zA-Z0-9_]*$"
#         cmp_pattern = r"^(CMP) R\d{1,2}, R\d{1,2}$"
#         nop_pattern = r"^(NOP)$"
#         # mov_pattern = r"^(MOV) R\d{1,2}, (R\d{1,2}|\d+)$"
#         # mov and movi
#         mov_pattern = r"^(MOV) R\d{1,2}, R\d{1,2}$"
#         movi_pattern = r"^(MOVI) R\d{1,2}, \d+$"

#         patterns = {
#             "three_reg": three_reg_pattern,
#             "one_reg": one_reg_pattern,
#             "three_reg_mem": three_reg_mem_pattern,
#             "reg_label": reg_label_pattern,
#             "label": label_pattern,
#             "cmp": cmp_pattern,
#             "nop": nop_pattern,
#             "mov": mov_pattern,
#             "movi": movi_pattern,
#             "two_reg_imm": two_reg_imm_pattern,
#         }

#         for instr_type, pattern in patterns.items():
#             if re.match(pattern, line, re.IGNORECASE):
#                 tokens = re.split(r"\s|,|\s*,\s*", line)
#                 tokens = [token.strip() for token in tokens if token]

#                 # strip brackets from memory instructions
#                 if instr_type == "three_reg_mem":
#                     tokens[2] = tokens[2][1:]
#                     tokens[3] = tokens[3][:-1]

#                 instr = tokens[0].upper()
#                 operands = tokens[1:]
#                 return instr, operands, label
            
#         print(f"Error: Invalid instruction format in line: '{line}'")
#         sys.exit(1)

#     def tokenize_data(self, line) -> tuple:
#         if line.startswith("//"):
#             return None, [], None

#         # remove comments (start of line or after an instruction, //)
#         line = re.sub(r"//.*", "", line)

#         # remove leading and trailing whitespaces
#         line = line.strip()

#         # split the line on spaces, then on commas
#         tokens = re.split(r"\s|:", line)

#         # remove empty tokens
#         tokens = [token for token in tokens if token]

#         # remove leading and trailing whitespaces from each token
#         tokens = [token.strip() for token in tokens]

#         label = None
#         values = []

#         # check if the line is empty
#         if not line:
#             return label, values

#         # use regex to check if its a label, and make sure theres no instruction on the same line (throw an error)
#         if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:$", line):
#             if len(tokens) > 1:
#                 print(f"Error: Label '{line}' must be on its own line.")
#                 sys.exit(1)
#             label = line[:-1]
#             return label, values

#         # based on what the instruction is, tokenize it accordingly
#         label = tokens[0].strip()

#         # check if the label is already in the labels dictionary
#         if label in self.labels:
#             print(f"Error: Label '{label}' already defined.")
#             sys.exit(1)

#         # check if the label is already in the adr_labels dictionary
#         if label in self.adr_labels:
#             print(f"Error: Label '{label}' already defined.")
#             sys.exit(1)

#         values = [token.strip() for token in tokens[1].split(",")]

#         return label, values
    
#     def tokenize(self):
#         text_section = self.extract_text()
#         data_section = self.extract_data()

#         for line in text_section:
#             instr, operands, label = self.tokenize_instruction(line)
#             self.instructions.append((instr, operands, label))
        
#         for line in data_section:
#             label, values = self.tokenize_data(line)
#             self.data.append((label, values))
        
#         return self.instructions, self.data

# un-oop it, and make it just functions

def extract_text(lines) -> list:
    text_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".text":
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == ".data":
                    break
                text_section.append(lines[j])
    return text_section

def extract_data(lines) -> list:
    data_section = []
    for i, line in enumerate(lines):
        if line.strip() == ".data":
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == ".text":
                    break
                data_section.append(lines[j])
    return data_section

def tokenize_instruction(line) -> tuple:
    if line.startswith("//"):
        return None, [], None

    line = re.sub(r"//.*", "", line)
    line = line.strip()
    if not line:
        return None, [], None

    instr = None
    operands = []
    label = None

    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:$", line):
        label = line[:-1]
        return instr, operands, label

    two_reg_imm_pattern = r"^(ADDI|SUBI|MULI|DIVI) R\d{1,2}, R\d{1,2}, \d+$"
    three_reg_pattern = r"^(ADD|SUB|MUL|DIV|AND|ORR|XOR|LSL|LSR|ASR) R\d{1,2}, R\d{1,2}, R\d{1,2}$"
    one_reg_pattern = r"^(NEG) R\d{1,2}$"
    three_reg_mem_pattern = r"^(LDR|STR) R\d{1,2}, \[R\d{1,2}, R\d{1,2}\]$"
    reg_label_pattern = r"^(ADR|CBZ|CBNZ) R\d{1,2}, [a-zA-Z_][a-zA-Z0-9_]*$"
    label_pattern = r"^(B|BEQ|BNE|BGT|BLT|BGE|BLE) [a-zA-Z_][a-zA-Z0-9_]*$"
    cmp_pattern = r"^(CMP) R\d{1,2}, R\d{1,2}$"
    nop_pattern = r"^(NOP)$"
    # mov_pattern = r"^(MOV) R\d{1,2}, (R\d{1,2}|\d+)$"
    # mov and movi
    mov_pattern = r"^(MOV) R\d{1,2}, R\d{1,2}$"
    movi_pattern = r"^(MOVI) R\d{1,2}, \d+$"

    patterns = {
        "three_reg": three_reg_pattern,
        "one_reg": one_reg_pattern,
        "three_reg_mem": three_reg_mem_pattern,
        "reg_label": reg_label_pattern,
        "label": label_pattern,
        "cmp": cmp_pattern,
        "nop": nop_pattern,
        "mov": mov_pattern,
        "movi": movi_pattern,
        "two_reg_imm": two_reg_imm_pattern,
    }

    for instr_type, pattern in patterns.items():
        if re.match(pattern, line, re.IGNORECASE):
            tokens = re.split(r"\s|,|\s*,\s*", line)
            tokens = [token.strip() for token in tokens if token]

            # strip brackets from memory instructions
            if instr_type == "three_reg_mem":
                tokens[2] = tokens[2][1:]
                tokens[3] = tokens[3][:-1]

            instr = tokens[0].upper()
            operands = tokens[1:]
            return instr, operands, label
        
    print(f"Error: Invalid instruction format in line: '{line}'")
    sys.exit(1)

def tokenize_data(line, labels, adr_labels) -> tuple:
    if line.startswith("//"):
        return None, [], None

    # remove comments (start of line or after an instruction, //)
    line = re.sub(r"//.*", "", line)

    # remove leading and trailing whitespaces
    line = line.strip()

    # split the line on spaces, then on commas
    tokens = re.split(r"\s|:", line)

    # remove empty tokens
    tokens = [token for token in tokens if token]

    # remove leading and trailing whitespaces from each token
    tokens = [token.strip() for token in tokens]

    values = []

    # check if the line is empty
    if not line:
        return label, values

    # use regex to check if its a label, and make sure theres no instruction on the same line (throw an error)
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:$", line):
        if len(tokens) > 1:
            print(f"Error: Label '{line}' must be on its own line.")
            sys.exit(1)
        label = line[:-1]
        return label, values

    # based on what the instruction is, tokenize it accordingly
    label = tokens[0].strip()

    # check if the label is already in the labels dictionary
    if label in labels:
        print(f"Error: Label '{label}' already defined.")
        sys.exit(1)

    # check if the label is already in the adr_labels dictionary
    if label in adr_labels:
        print(f"Error: Label '{label}' already defined.")
        sys.exit(1)

    values = [token.strip() for token in tokens[1].split(",")]

    return label, values

def tokenize(lines, labels, adr_labels):
    instructions = []
    data = []

    text_section = extract_text(lines)
    data_section = extract_data(lines)

    for line in text_section:
        instr, operands, label = tokenize_instruction(line)
        instructions.append((instr, operands, label))
    
    for line in data_section:
        label, values = tokenize_data(line, labels, adr_labels)
        data.append((label, values))
    
    return instructions, data