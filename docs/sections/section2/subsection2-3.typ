== Branching

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
  [20 bits],
  [5 bits],
  [BL Label],
  [001100],
  [20 bits],
  [5 bits],
  [BEQ Label],
  [010100],
  [20 bits],
  [5 bits],
  [BNE Label],
  [011100],
  [20 bits],
  [5 bits],
  [BGT Label],
  [100100],
  [20 bits],
  [5 bits],
  [BLT Label],
  [101100],
  [20 bits],
  [5 bits],
  [BGE Label],
  [110100],
  [20 bits],
  [5 bits],
  [BLE Label],
  [111100],
  [20 bits],
  [5 bits],
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
