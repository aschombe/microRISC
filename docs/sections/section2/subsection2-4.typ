#import "../../rivet-config.typ": schema, config, rivet-config

== Other

#let misc-layout = schema.load(
  (
    structures: (
      main: (
        bits: 32,
        ranges: (
          "31-26": (name: "op", description: "Operation code, see table below"),
          "25":    (name: "I", description: "Immediate flag, selects between Rm and Imm for MOV and CMP; ignored for NOP, RET"),
          "24-20": (name: "Rd", description: "Destination register for MOV; ignored for CMP, NOP, RET"),
          "19-15": (name: "Rn", description: "First source register for CMP; ignored for MOV, NOP, RET"),
          "14-10": (name: "Rm", description: "Second source register for CMP when I = 0; ignored for MOV, NOP, RET"),
          "9-0":   (name: "Imm", description: "Immediate operand for MOV and CMP when I = 1; ignored for NOP, RET"),
        ),
      ),
    ),
  )
)

#schema.render(misc-layout, config: rivet-config)

#table(
  columns: 3,
  table.header([Syntax], [Opcode], [Notes]),
  [NOP], [110000], [No operation],
  [RET], [110001], [Return to address in LR],
)

#table(
  columns: 3,
  table.header([Syntax], [Opcode], [Notes]),
  [MOV Rd, Rn / Imm], [110010], [Move register or immediate value into Rd],
  [CMP Rn, Rm / Imm], [110100], [Subtract Rm or Imm from Rn and update CMP register],
)
