== Other

These are other instructions that don't fit under the existing categories:

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Rn],
    [Unused],
  ),
  [MOV Rd, Rn],
  [Item2.26],
  [5 bits],
  [5 bits],
  [16 bits],
)

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Imm],
  ),
  [MOV Rd, Imm],
  [Item2.27],
  [5 bits],
  [21 bits],
)

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Label],
    [Unused],
  ),
  [ADR Rd, Label],
  [Item2.28],
  [5 bits],
  [20 bits],
  [1 bit],
)

#table(
  columns: 4,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Unused],
  ),
  [NEG Rd],
  [Item2.29],
  [5 bits],
  [21 bits],
)

#table(
  columns: 3,
  table.header(
    [Syntax],
    [Opcode],
    [Unused],
  ),
  [NOP],
  [Item2.30],
  [26 bits],
)



