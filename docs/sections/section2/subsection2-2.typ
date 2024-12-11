== Memory
The following memory instructions are supported:

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Rn],
    [Rm],
  ),
  [LDR Rd, [Rn, Rm]],
  [000010],
  [5 bits],
  [5 bits],
  [5 bits],
  [STR Rd, [Rn, Rm]],
  [000110],
  [5 bits],
  [5 bits],
  [5 bits],
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
  [001010],
  [5 bits],
  [20 bits],
  [1 bit],
)
