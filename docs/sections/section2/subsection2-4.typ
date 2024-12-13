== Other

These are other instructions that don't fit under the existing categories:

#table(
  columns: 3,
  table.header(
    [Syntax],
    [Opcode],
    [Unused],
  ),
  [NOP],
  [110000],
  [26 bits],
  // [RET],
  // [110001],
  // [26 bits],
)

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Rn],
    [Unused],
  ),
  [MOV Rd, Rn],
  [110010],
  [5 bits],
  [5 bits],
  [16 bits],
)

#table(
  columns: 4,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Imm],
    [Unused],
  ),
  [MOV Rd, Imm],
  [110010],
  [5 bits],
  [21 bits],
  [0 bits],
)

#table(
  columns: 5,
  table.header(
    [Syntax],
    [Opcode],
    [Rd],
    [Rn],
    [Unused],
  ),
  [CMP Rd, Rn],
  [110011],
  [5 bits],
  [5 bits],
  [16 bits],
)

#table(
  columns: 4,
  table.header(
    [Syntax],
    [Opcode],
    [Rn],
    [Label],
    [Unused],
  ),
  [CBZ Rn, Label],
  [110100],
  [5 bits],
  [21 bits],
  [0 bits],
  [CBNZ Rn, Label],
  [110101],
  [5 bits],
  [21 bits],
  [0 bits],
)

There is also support for single line comments and end of line comments:
```asm
// This is a single line comment
ADD R1, R2, R3 // This is an end of line comment
```
