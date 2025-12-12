== Memory

Load and store instructions use either a register index or an immediate offset from a base register. The I flag selects between the two.

#table(
  columns: 7,
  table.header(
    [Syntax], [Opcode], [I], [Rd], [Rn], [Rm / Imm], [Notes],
  ),
  [LDR Rd, [Rn, Rm/Imm]], [010000], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)], [Load word from Rn + Rm/Imm],
  [STR Rd, [Rn, Rm/Imm]], [010001], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)], [Store word to Rn + Rm/Imm],
)

#table(
  columns: 5,
  table.header(
    [Syntax], [Opcode], [Rd], [Imm], [Notes],
  ),
  [ADR Rd, Label], [010010], [5 bits], [20 bits], [PC-relative address of label],
)
