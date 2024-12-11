== Branching

Labels are resolved to 24-bit addresses from the start of the program.
The following branching instructions are supported:

#table(
  columns: 4,
  table.header(
    [Syntax],
    [Opcode],
    [Label],
    [Unused],
  ),
  [B Label],
  [000100],
  [24 bits],
  [2 bits],
  [BL Label],
  [001100],
  [24 bits],
  [2 bits],
  [BEQ Label],
  [010100],
  [24 bits],
  [2 bits],
  [BNE Label],
  [011100],
  [24 bits],
  [2 bits],
  [BGT Label],
  [100100],
  [24 bits],
  [2 bits],
  [BLT Label],
  [101100],
  [24 bits],
  [2 bits],
  [BGE Label],
  [110100],
  [24 bits],
  [2 bits],
  [BLE Label],
  [111100],
  [24 bits],
  [2 bits],
)

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Rn],
    [Unused],
  ),
  [CMP Rd, Rn],
  [100000],
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
    [Label],
    [Unused],
  ),
  [CBZ Rd, Label],
  [110000],
  [5 bits],
  [20 bits],
  [1 bit],
  [CBNZ Rd, Label],
  [101000],
  [5 bits],
  [20 bits],
  [1 bit],
)

#table(
  columns: 3,
  table.header(
    [Syntax],
    [Opcode],
    [Unused],
  ),
  [RET],
  [111000],
  [26 bits],
)
