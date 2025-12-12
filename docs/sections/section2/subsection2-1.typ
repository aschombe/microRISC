== Arithmetic and Logical

The ALU instructions share one encoding each. The I flag selects whether the second operand comes from a register Rm or from an immediate value Imm.

#table(
  columns: 6,
  table.header(
    [Syntax], [Opcode], [I], [Rd], [Rn], [Rm / Imm],
  ),
  [ADD Rd, Rn, Rm/Imm], [000000], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [SUB Rd, Rn, Rm/Imm], [000001], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [MUL Rd, Rn, Rm/Imm], [000010], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [DIV Rd, Rn, Rm/Imm], [000011], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [AND Rd, Rn, Rm/Imm], [000100], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [ORR Rd, Rn, Rm/Imm], [000101], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [XOR Rd, Rn, Rm/Imm], [000110], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [LSL Rd, Rn, Rm/Imm], [000111], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [LSR Rd, Rn, Rm/Imm], [001000], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [ASR Rd, Rn, Rm/Imm], [001001], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
)

#table(
  columns: 4,
  table.header(
    [Syntax], [Opcode], [Rd], [Notes],
  ),
  [NEG Rd], [001010], [5 bits], [Unary negate; uses Rn field internally],
)
