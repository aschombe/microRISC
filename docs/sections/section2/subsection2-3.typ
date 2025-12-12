== Branching

Branches use a 20-bit signed offset from the current PC. For conditional branches based on the CMP register, the CMP register is set by the CMP instruction. CBZ and CBNZ test a general-purpose register directly.

#table(
  columns: 4,
  table.header(
    [Syntax], [Opcode], [Rn], [Offset/Label],
  ),
  [B Label],   [100000], [unused], [20 bits],
  [BL Label],  [100001], [unused], [20 bits],
  [BEQ Label], [100010], [unused], [20 bits],
  [BNE Label], [100011], [unused], [20 bits],
  [BGT Label], [100100], [unused], [20 bits],
  [BLT Label], [100101], [unused], [20 bits],
  [BGE Label], [100110], [unused], [20 bits],
  [BLE Label], [100111], [unused], [20 bits],
)

#table(
  columns: 4,
  table.header(
    [Syntax], [Opcode], [Rn], [Offset/Label],
  ),
  [CBZ Rn, Label],  [110101], [5 bits], [20 bits],
  [CBNZ Rn, Label], [110110], [5 bits], [20 bits],
)
