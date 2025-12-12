import re
import sys

def extract_text(lines) -> list[str]:
    in_text = False
    text_section: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower() == "<text>":
            in_text = True
            continue
        if stripped.lower() == "<data>":
            in_text = False
            continue
        if in_text:
            text_section.append(line)
    return text_section


def extract_data(lines) -> list[str]:
    in_data = False
    data_section: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower() == "<data>":
            in_data = True
            continue
        if stripped.lower() == "<text>":
            in_data = False
            continue
        if in_data:
            data_section.append(line)
    return data_section


_block_comment_re = re.compile(r"/\*.*?\*/", re.DOTALL)

def strip_comments(line: str) -> str:
    line = re.sub(r"//.*", "", line)
    line = _block_comment_re.sub("", line)
    return line

def tokenize_instruction(line: str) -> tuple[str | None, str | None, list[str]]:
    """
    Return (label, instr, operands) where:
    - label is a string or None
    - instr is an uppercased mnemonic or None
    - operands is a list of raw operand strings
    """
    line_no_comments = strip_comments(line).strip()
    if not line_no_comments:
        return None, None, []

    label = None
    instr = None
    operands: list[str] = []

    # Label only
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:$", line_no_comments):
        label = line_no_comments[:-1]
        return label, None, []

    # Label + instruction
    if ":" in line_no_comments:
        before, after = line_no_comments.split(":", 1)
        maybe_label = before.strip()
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", maybe_label):
            label = maybe_label
            line_no_comments = after.strip()

    if not line_no_comments:
        return label, None, []

    # Split instruction and operands
    parts = line_no_comments.split(None, 1)
    instr = parts[0].upper()
    rest = parts[1] if len(parts) > 1 else ""

    rest = rest.replace("[", " [ ").replace("]", " ] ")
    tokens = [t for t in re.split(r"[,\s]+", rest) if t]
    operands = tokens

    return label, instr, operands


def tokenize_data_line(line: str):
    """
    Minimal data tokenization for now:
    - label: value1, value2, ...
    Line example:
      myvar: 1, 2, 3
    """
    pass
    # line_no_comments = strip_comments(line).strip()
    # if not line_no_comments:
    #     return None, []
    #
    # # Label only
    # if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:$", line_no_comments):
    #     label = line_no_comments[:-1]
    #     return label, []
    #
    # if ":" not in line_no_comments:
    #     print(f"Error in data section: missing ':' in line: {line_no_comments}")
    #     sys.exit(1)
    #
    # label, rest = line_no_comments.split(":", 1)
    # label = label.strip()
    #
    # values = [v.strip() for v in rest.split(",") if v.strip()]
    # return label, values
