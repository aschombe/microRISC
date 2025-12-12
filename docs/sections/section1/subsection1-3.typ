== Memory Layout

The microRISC architecture uses separate instruction and data memories. Both memories are word-addressed and store 32-bit words.

=== Instruction Memory

#table(
  columns: 3,
  table.header([Property], [Value], [Notes]),
  [Address width], [24 bits], [Word-addressed; one word per address],
  [Word width], [32 bits], [Each instruction is 32 bits],
)

=== Data Memory

#table(
  columns: 3,
  table.header([Property], [Value], [Notes]),
  [Address width], [24 bits], [Word-addressed; one word per address],
  [Word width], [32 bits], [Matches general-purpose register size],
)

The LDR and STR instructions operate on 32-bit words and use a base register plus an optional register or immediate offset to form the 24-bit data address.
