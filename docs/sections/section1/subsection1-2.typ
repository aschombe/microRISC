== Opcode Layout and Control Signals
#import "../../rivet-config.typ": schema, config, rivet-config

Every instruction is 32 bits wide. The top 6 bits form the opcode and drive the main control signals. Bit 25 is the I flag, which selects between a register operand and an immediate field for ALU and memory instructions.

#let inst-layout = schema.load(
  (
    structures: (
      main: (
        bits: 32,
        ranges: (
          "31-26": (name: "opcode", description: "Operation code"),
          "25":    (name: "I",      description: "0: use Rm, 1: use Imm"),
          "24-20": (name: "Rd",     description: "Destination register"),
          "19-15": (name: "Rn",     description: "First source / base register"),
          "14-10": (name: "Rm",     description: "Second source / index register when I = 0"),
          "9-0":   (name: "Imm",    description: "Sign-extended immediate when I = 1"),
        ),
      ),
    ),
  )
)

#schema.render(inst-layout, config: rivet-config)
