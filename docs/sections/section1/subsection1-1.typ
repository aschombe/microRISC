== Registers

=== General Purpose Registers

The general purpose registers are used to store data and perform arithmetic operations. They are named R0-R29 and are 32 bits wide.

// #table(
//   columns: 2,
//   table.header(
//     [Register],
//     [Binary Representation],
//   ),
//   [R0],
//   [00000],
//   [R1],
//   [00001],
//   [R2],
//   [00010],
//   [R3],
//   [00011],
//   [R4],
//   [00100],
//   [R5],
//   [00101],
//   [R6],
//   [00110],
//   [R7],
//   [00111],
//   [R8],
//   [01000],
//   [R9],
//   [01001],
//   [R10],
//   [01010],
//   [R11],
//   [01011],
//   [R12],
//   [01100],
//   [R13],
//   [01101],
//   [R14],
//   [01110],
//   [R15],
//   [01111],
//   [R16],
//   [10000],
//   [R17],
//   [10001],
//   [R18],
//   [10010],
//   [R19],
//   [10011],
//   [R20],
//   [10100],
//   [R21],
//   [10101],
//   [R22],
//   [10110],
//   [R23],
//   [10111],
//   [R24],
//   [11000],
//   [R25],
//   [11001],
//   [R26],
//   [11010],
//   [R27],
//   [11011],
//   [R28],
//   [11100],
//   [R29],
//   [11101],
// )
// split the above table into two tables, next to each other, 15 registers each
// not literally, but emulate it by making the table like this:
// Register | Binary Representation | Register | Binary Representation
#table(
  columns: 4,
  table.header(
    [Register],
    [Binary Representation],
    [Register],
    [Binary Representation],
  ),
  [R0],
  [00000],
  [R1],
  [00001],
  [R2],
  [00010],
  [R3],
  [00011],
  [R4],
  [00100],
  [R5],
  [00101],
  [R6],
  [00110],
  [R7],
  [00111],
  [R8],
  [01000],
  [R9],
  [01001],
  [R10],
  [01010],
  [R11],
  [01011],
  [R12],
  [01100],
  [R13],
  [01101],
  [R14],
  [01110],
  [R15],
  [01111],
  [R16],
  [10000],
  [R17],
  [10001],
  [R18],
  [10010],
  [R19],
  [10011],
  [R20],
  [10100],
  [R21],
  [10101],
  [R22],
  [10110],
  [R23],
  [10111],
  [R24],
  [11000],
  [R25],
  [11001],
  [R26],
  [11010],
  [R27],
  [11011],
  [R28],
  [11100],
  [R29],
  [11101],
)

=== Program Counter (PC)

The program counter register keeps track of the current instruction being executed. It is automatically incremented after each instruction is executed. It can not be directly accessed or modified by the programmer.

=== CMP Register

The CMP register is used to store the result of a comparison operation. It is set by the CMP instruction, which subtracts the second operand from the first operand and sets the CMP register based on the result. Reference it using the CMP keyword (its an operation and a register).

#table(
  columns: 2,
  table.header(
    [Register],
    [Binary Representation],
  ),
  [CMP],
  [11110],
)

=== Stack Pointer (SP)

The stack pointer register is used to keep track of the top of the stack. Similarly to ARM, you must manually manage the stack pointer. Reference it using the SP keyword.

#table(
  columns: 2,
  table.header(
    [Register],
    [Binary Representation],
  ),
  [SP],
  [11111],
)
