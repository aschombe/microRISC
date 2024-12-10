== Opcode Layout and Control Signals

Every opcode is 6 bits wide. Each bit will be a dedicated control signal:

#table(
  columns: 6,
  table.header(
    [Bit 0],
    [Bit 1],
    [Bit 2],
    [Bit 3],
    [Bit 4],
    [Bit 5],
  ),
  [Control Signal 0],
  [Control Signal 1],
  [Control Signal 2],
  [Control Signal 3],
  [Control Signal 4],
  [Control Signal 5],
)

There are also other control signals that are not part of the opcode. These are:
