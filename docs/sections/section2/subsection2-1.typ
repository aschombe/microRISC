== Arithmetic and Logical

The following arithmetic and logical operations are supported:

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Rn],
    [Rm],
    [Unused],
  ),
  [ADD Rd, Rn, Rm],
  [000000],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [SUB Rd, Rn, Rm],
  [000001],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [MUL Rd, Rn, Rm],
  [000010],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [DIV Rd, Rn, Rm],
  [000011],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [AND Rd, Rn, Rm],
  [000100],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [ORR Rd, Rn, Rm],
  [000101],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [XOR Rd, Rn, Rm],
  [000110],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [LSL Rd, Rn, Rm],
  [000111],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [LSR Rd, Rn, Rm],
  [001000],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [ASR Rd, Rn, Rm],
  [001001],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
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
  [001010],
  [5 bits],
  [21 bits],
)
