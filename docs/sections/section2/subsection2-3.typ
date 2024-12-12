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
  [100000],
  [24 bits],
  [2 bits],
  // [BL Label],
  // [100001],
  // [24 bits],
  // [2 bits],
  [BEQ Label],
  [100010],
  [24 bits],
  [2 bits],
  [BNE Label],
  [100011],
  [24 bits],
  [2 bits],
  [BGT Label],
  [100100],
  [24 bits],
  [2 bits],
  [BLT Label],
  [100101],
  [24 bits],
  [2 bits],
  [BGE Label],
  [100110],
  [24 bits],
  [2 bits],
  [BLE Label],
  [100111],
  [24 bits],
  [2 bits],
)
