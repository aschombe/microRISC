== Memory Layout

Data memory: 24-bit wide addresses, 32-bit wide data.

// Cache Design Specifications

//     24-bit Address.
//     Cache Size: 1 KB = 256 lines (1 word per line).
//     Tag Size: 16 bits.
//     Index Size: 8 bits.
//     Word Size: 32 bits.
//     Valid Bit: 1 bit per line.
Direct-Mapped Cache: 1 KB (256 lines, 1 word per line, 4 bytes or 32 bits per word), 24-bit address:

#table(
  columns: 4,
  table.header(
    [Tag],
    [Index],
    [Offset],
    [Valid Bit],
  ),
  [16 bits],
  [8 bits],
  [0 bits],
  [1 bit],
)

// #table(
//   columns: 6,
//   table.header(
//     [Bit 0],
//     [Bit 1],
//     [Bit 2],
//     [Bit 3],
//     [Bit 4],
//     [Bit 5],
//   ),
//   [Control Signal 0],
//   [Control Signal 1],
//   [Control Signal 2],
//   [Control Signal 3],
//   [Control Signal 4],
//   [Control Signal 5],
// )