== Opcode Layout and Control Signals

Every instruction is 32 bits wide. The top 6 bits form the opcode and drive the main control signals. Bit 25 is the I flag, which selects between a register operand and an immediate field for ALU and memory instructions.

#table(
  columns: 4,
  table.header(
    [Bits], [Name], [Description], [Used by],
  ),
  [31–26], [opcode], [Primary operation and type], [All instructions],
  [25], [I], [0 = use Rm; 1 = use Imm], [ALU, LDR, STR, MOV, CMP],
  [24–20], [Rd], [Destination register], [ALU, LDR, ADR, MOV],
  [19–15], [Rn], [First source or base register], [ALU, LDR, STR, CBZ, CBNZ],
  [14–10], [Rm], [Second source/index register when I = 0], [ALU, LDR, STR],
  [14–0], [Imm], [Sign-extended immediate when I = 1], [ALU, LDR, STR, ADR, branches],
)
