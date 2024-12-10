# microRISC
microRISC is a simple, and extensive CPU architecture implemented in Logisim.

## Features
- Detailed Manual [here](docs/main.pdf)
- 32 General Purpose Registers
- CMP Register (results of comparison)
- 32-bit Instructions
- Multitude of operations (check manual for specifics):
  - Arithmetic
  - Logical
  - Memory
  - Control Flow
- Simple Instruction Set and Assembly Language

## Usage
1. Clone the [repository](https://github.com/aschombe/microRISC)
2. Open a terminal and navigate to the root of the repository
3. Run the assembler with the following command:
```bash
python3 assembler.py <input_file_name> [-o] <output_file_name>
```
4. Open Logisim and load the `microRISC.circ` file
5. Load instructions.o into the Instruction Memory, data.o into the Data Memory
6. Run the simulation

## TODO List
- [ ] Manual
- [ ] Design the architecture/spec
- [ ] Define the instruction set
- [ ] Implement the architecture in Logisim
- [ ] Write an assembler

## Notes (until I make the manual)
- Instructions (32-bit):
  | Syntax            | Opcode            | Rd                | Rn                | Rm              |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | ADD Rd, Rn, Rm    | Item2.1           | Item3.1           | Item4.1           | Item5.1         |
  | SUB Rd, Rn, Rm    | Item2.2           | Item3.2           | Item4.2           | Item5.2         |
  | MUL Rd, Rn, Rm    | Item2.3           | Item3.3           | Item4.3           | Item5.3         |
  | SDIV Rd, Rn, Rm    | Item2.4           | Item3.4           | Item4.4           | Item5.4         |
  | UDIV Rd, Rn, Rm    | Item2.5           | Item3.5           | Item4.5           | Item5.5         |
  | LDR Rd, [Rn, Rm]  | Item2.5           | Item3.5           | Item4.5           | Item5.5         |
  | STR Rd, [Rn, Rm]  | Item2.6           | Item3.6           | Item4.6           | Item5.6         |
  | AND Rd, Rn, Rm    | Item2.7           | Item3.7           | Item4.7           | Item5.7         |
  | ORR Rd, Rn, Rm    | Item2.8           | Item3.8           | Item4.8           | Item5.8         |
  | XOR Rd, Rn, Rm    | Item2.9           | Item3.9           | Item4.9           | Item5.9         |
  | LSL Rd, Rn, Rm    | Item2.10          | Item3.10          | Item4.10          | Item5.10        |
  | LSR Rd, Rn, Rm    | Item2.11          | Item3.11          | Item4.11          | Item5.11        |
  | ASR Rd, Rn, Rm    | Item2.12          | Item3.12          | Item4.12          | Item5.12        |

  | Syntax            | Opcode            | Rd                | Rn                | Imm             |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | ADDI Rd, Rn, Imm  | Item2.9           | Item3.9           | Item4.9           | Item5.9         |
  | SUBI Rd, Rn, Imm  | Item2.10          | Item3.10          | Item4.10          | Item5.10        |
  | MULI Rd, Rn, Imm  | Item2.11          | Item3.11          | Item4.11          | Item5.11        |
  | SDIVI Rd, Rn, Imm  | Item2.12          | Item3.12          | Item4.12          | Item5.12        |
  | UDIVI Rd, Rn, Imm  | Item2.13          | Item3.13          | Item4.13          | Item5.13        |
  | LDR Rd, [Rn, Imm] | Item2.13          | Item3.13          | Item4.13          | Item5.13        |
  | STR Rd, [Rn, Imm] | Item2.14          | Item3.14          | Item4.14          | Item5.14        |
  | AND Rd, Rn, Imm   | Item2.15          | Item3.15          | Item4.15          | Item5.15        |
  | ORR Rd, Rn, Imm   | Item2.16          | Item3.16          | Item4.16          | Item5.16        |
  | XOR Rd, Rn, Imm   | Item2.17          | Item3.17          | Item4.17          | Item5.17        |
  | LSL Rd, Rn, Imm   | Item2.18          | Item3.18          | Item4.18          | Item5.18        |
  | LSR Rd, Rn, Imm   | Item2.19          | Item3.19          | Item4.19          | Item5.19        |
  | ASR Rd, Rn, Imm   | Item2.20          | Item3.20          | Item4.20          | Item5.20        |

  | Syntax            | Opcode            | Rd                | Imm               | Imm             |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | ADDI Rd, Imm, Imm | Item2.17          | Item3.17          | Item4.17          | Item5.17        |
  | SUBI Rd, Imm, Imm | Item2.18          | Item3.18          | Item4.18          | Item5.18        |
  | MULI Rd, Imm, Imm | Item2.19          | Item3.19          | Item4.19          | Item5.19        |
  | SDIVI Rd, Imm, Imm | Item2.20          | Item3.20          | Item4.20          | Item5.20        |
  | UDIVI Rd, Imm, Imm | Item2.21          | Item3.21          | Item4.21          | Item5.21        |
  | LDR Rd, [Imm, Imm]| Item2.21          | Item3.21          | Item4.21          | Item5.21        |
  | STR Rd, [Imm, Imm]| Item2.22          | Item3.22          | Item4.22          | Item5.22        |
  | AND Rd, Imm, Imm  | Item2.23          | Item3.23          | Item4.23          | Item5.23        |
  | ORR Rd, Imm, Imm  | Item2.24          | Item3.24          | Item4.24          | Item5.24        |
  | XOR Rd, Imm, Imm  | Item2.25          | Item3.25          | Item4.25          | Item5.25        |
  | LSL Rd, Imm, Imm  | Item2.26          | Item3.26          | Item4.26          | Item5.26        |
  | LSR Rd, Imm, Imm  | Item2.27          | Item3.27          | Item4.27          | Item5.27        |
  | ASR Rd, Imm, Imm  | Item2.28          | Item3.28          | Item4.28          | Item5.28        |

  | Syntax            | Opcode            | Rd                | Rn                |                 |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | CMP Rd, Rn        | Item2.25          | Item3.25          | Item4.25          | Item5.25        |
  | MOV Rd, Rn        | Item2.26          | Item3.26          | Item4.26          | Item5.26        |

  | Syntax            | Opcode            | Rd                | Imm               |                 |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | CMP Rd, Imm       | Item2.27          | Item3.27          | Item4.27          | Item5.27        |
  | MOV Rd, Imm       | Item2.28          | Item3.28          | Item4.28          | Item5.28        |

  | Syntax            | Opcode            | Rd                | Label             |                 |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | ADR Rd, Label     | Item2.26          | Item3.26          | Item4.26          | Item5.26        |
  | CBZ Rd, Label     | Item2.27          | Item3.27          | Item4.27          | Item5.27        |
  | CBNZ Rd, Label    | Item2.28          | Item3.28          | Item4.28          | Item5.28        |

  | Syntax            | Opcode            | Label             |                   |                 |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | B Label           | Item2.27          | Item3.27          | Item4.27          | Item5.27        |
  | BL  Label         | Item2.25          | Item3.25          | Item4.25          | Item5.25        |
  | BEQ Label         | Item2.26          | Item3.26          | Item4.26          | Item5.26        |
  | BNE Label         | Item2.27          | Item3.27          | Item4.27          | Item5.27        |
  | BGT Label         | Item2.28          | Item3.28          | Item4.28          | Item5.28        |
  | BLT Label         | Item2.29          | Item3.29          | Item4.29          | Item5.29        |
  | BGE Label         | Item2.30          | Item3.30          | Item4.30          | Item5.30        |
  | BLE Label         | Item2.31          | Item3.31          | Item4.31          | Item5.31        |

  | Syntax            | Opcode            | Rd                |                   |                 |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | NEG Rd            | Item2.29          | Item3.29          | Item4.29          | Item5.29        |

  | Syntax            | Opcode            |                   |                   |                 |
  | ---------------   | ---------------   | ---------------   | ---------------   | --------------- |
  | NOP               | Item2.32          | Item3.32          | Item4.32          | Item5.32        |
  | RET               | Item2.33          | Item3.33          | Item4.33          | Item5.33        |
