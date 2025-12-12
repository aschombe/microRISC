#import "../../rivet-config.typ": schema, config, rivet-config

== Arithmetic and Logical

The ALU instructions share one encoding each. The I flag selects whether the second operand comes from a register Rm or from an immediate value Imm.

#let alu-layout = schema.load(
  (
    structures: (
      main: (
        bits: 32,
        ranges: (
          "31-26": (name: "opcode", description: "Operation code, see table below"),
          "25":    (name: "I",      description: "0: use Rm, 1: use Imm"),
          "24-20": (name: "Rd",     description: "Destination register"),
          "19-15": (name: "Rn",     description: "First source register"),
          "14-10": (name: "Rm",     description: "Second source when I = 0"),
          "9-0":   (name: "Imm",    description: "Immediate when I = 1"),
        ),
      ),
    ),
  )
)

#schema.render(alu-layout, config: rivet-config)

#table(
  columns: 4,
  table.header([Syntax], [Opcode], [I], [Notes]),
  [ADD Rd, Rn, Rm / Imm], [000000], [0 or 1], [Add Rn and Rm or Imm into Rd],
  [SUB Rd, Rn, Rm / Imm], [000001], [0 or 1], [Subtract Rm or Imm from Rn into Rd],
  [MUL Rd, Rn, Rm / Imm], [000010], [0 or 1], [Multiply Rn by Rm or Imm into Rd],
  [DIV Rd, Rn, Rm / Imm], [000011], [0 or 1], [Divide Rn by Rm or Imm into Rd],
  [AND Rd, Rn, Rm / Imm], [000100], [0 or 1], [Bitwise AND of Rn and Rm or Imm],
  [ORR Rd, Rn, Rm / Imm], [000101], [0 or 1], [Bitwise OR of Rn and Rm or Imm],
  [XOR Rd, Rn, Rm / Imm], [000110], [0 or 1], [Bitwise XOR of Rn and Rm or Imm],
  [LSL Rd, Rn, Rm / Imm], [000111], [0 or 1], [Logical shift left Rn by Rm or Imm],
  [LSR Rd, Rn, Rm / Imm], [001000], [0 or 1], [Logical shift right Rn by Rm or Imm],
  [ASR Rd, Rn, Rm / Imm], [001001], [0 or 1], [Arithmetic shift right Rn by Rm or Imm],
)

#table(
  columns: 3,
  table.header([Syntax], [Opcode], [Notes]),
  [NEG Rd], [001010], [Unary negate; encoded as an ALU op using the Rn field internally],
)
