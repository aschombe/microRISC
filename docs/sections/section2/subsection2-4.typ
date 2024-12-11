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
  [000000],
  [26 bits],
)

There is also support for single line comments and end of line comments:
```asm
// This is a single line comment
ADD R1, R2, R3 // This is an end of line comment
```
