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
    [Unused],
  ),
  [LDR Rd, [Rn, Rm]],
  [010000],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
  [STR Rd, [Rn, Rm]],
  [010001],
  [5 bits],
  [5 bits],
  [5 bits],
  [11 bits],
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
  [010010],
  [5 bits],
  [20 bits],
  [1 bit],
)
