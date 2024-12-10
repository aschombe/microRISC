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
  [Item2.27],
  [20 bits],
  [5 bits],
  [BL Label],
  [Item2.28],
  [20 bits],
  [5 bits],
  [BEQ Label],
  [Item2.29],
  [20 bits],
  [5 bits],
  [BNE Label],
  [Item2.30],
  [20 bits],
  [5 bits],
  [BGT Label],
  [Item2.31],
  [20 bits],
  [5 bits],
  [BLT Label],
  [Item2.32],
  [20 bits],
  [5 bits],
  [BGE Label],
  [Item2.33],
  [20 bits],
  [5 bits],
  [BLE Label],
  [Item2.34],
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
    [Label],
    [Unused],
  ),
  [CBZ Rd, Label],
  [Item2.35],
  [5 bits],
  [20 bits],
  [1 bit],
  [CBNZ Rd, Label],
  [Item2.36],
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
  [Item2.37],
  [26 bits],
)
