#import "../../rivet-config.typ": schema, config, rivet-config

== Other

#let misc-layout = schema.load(
  (
    structures: (
      main: (
        bits: 32,
        ranges: (
          "31-26": (name: "opcode", description: "Operation code, see table below"),
          "25":    (name: "I / unused"),
          "24-20": (name: "Rd / unused"),
          "19-15": (name: "Rn"),
          "14-10": (name: "Rm"),
          "9-0":   (name: "Imm / unused"),
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
