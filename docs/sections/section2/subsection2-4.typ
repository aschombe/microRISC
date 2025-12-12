== Other

#table(
  columns: 3,
  table.header(
    [Syntax], [Opcode], [Unused],
  ),
  [NOP], [110000], [26 bits],
  [RET], [110001], [26 bits],
)

#table(
  columns: 6,
  table.header(
    [Syntax], [Opcode], [I], [Rd], [Rn], [Rm / Imm],
  ),
  [MOV Rd, Rn/Imm], [110010], [0/1], [5 bits], [5 bits], [Rm (5 bits) or Imm (15 bits)],
  [CMP Rn, Rm/Imm], [110100], [0/1], [ignored], [5 bits], [Rm (5 bits) or Imm (15 bits)],
)
