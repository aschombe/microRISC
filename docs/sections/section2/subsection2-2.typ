#import "../../rivet-config.typ": schema, config, rivet-config

== Memory

Load and store instructions use either a register index or an immediate offset from a base register. The I flag selects between the two.

#let mem-layout = schema.load(
  (
    structures: (
      main: (
        bits: 32,
        ranges: (
          "31-26": (name: "opcode", description: "010000=LDR, 010001=STR"),
          "25":    (name: "I",      description: "0: use Rm, 1: use Imm"),
          "24-20": (name: "Rd",     description: "Destination / source register"),
          "19-15": (name: "Rn",     description: "Base register"),
          "14-10": (name: "Rm",     description: "Index register when I = 0"),
          "9-0":   (name: "Imm",    description: "Offset when I = 1 (10-bit unsigned)"),
        ),
      ),
    ),
  )
)

#schema.render(mem-layout, config: rivet-config)

#table(
  columns: 4,
  table.header([Syntax], [Opcode], [I], [Notes]),
  [LDR Rd, Rn, Rm / Imm], [010000], [0 or 1], [Load word from Rn + Rm or Imm into Rd],
  [STR Rd, Rn, Rm / Imm], [010001], [0 or 1], [Store word from Rd to Rn + Rm or Imm],
)

#par[
ADR uses the same opcode group as the memory instructions but follows the control-flow layout with a 20-bit signed PC-relative offset, as shown in the Branching section.
]

#table(
  columns: 3,
  table.header([Syntax], [Opcode], [Notes]),
  [ADR Rd, Label], [010010], [PC-relative address of label in 20-bit Offset field],
)
