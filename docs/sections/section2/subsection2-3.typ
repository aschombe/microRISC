#import "../../rivet-config.typ": schema, config, rivet-config

== Branching

Branches use a 20-bit signed offset from the current PC. For conditional branches based on the CMP register, the CMP register is set by the CMP instruction. CBZ and CBNZ test a general-purpose register directly.

#let branch-layout = schema.load(
  (
    structures: (
      main: (
        bits: 32,
        ranges: (
          "31-26": (name: "opcode", description: "Operation code, see table below"),
          "25":    (name: "unused / I"),
          "24-20": (name: "unused"),
          "19-15": (name: "Rn", description: "Used by CBZ/CBNZ; unused by B/BL/cond branches"),
          "19-0":  (name: "Offset", description: "20-bit signed offset or label"),
        ),
      ),
    ),
  )
)

#schema.render(branch-layout, config: rivet-config)

#table(
  columns: 3,
  table.header([Syntax], [Opcode], [Notes]),
  [B Label],   [100000], [Unconditional branch with 20-bit signed offset],
  [BL Label],  [100001], [Branch with link; LR gets return address],
  [BEQ Label], [100010], [Branch if CMP indicates equal],
  [BNE Label], [100011], [Branch if CMP indicates not equal],
  [BGT Label], [100100], [Branch if greater than],
  [BLT Label], [100101], [Branch if less than],
  [BGE Label], [100110], [Branch if greater or equal],
  [BLE Label], [100111], [Branch if less or equal],
)

#table(
  columns: 3,
  table.header([Syntax], [Opcode], [Notes]),
  [CBZ Rn, Label],  [110101], [Branch if Rn == 0],
  [CBNZ Rn, Label], [110110], [Branch if Rn != 0],
)
