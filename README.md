# microRISC
microRISC is a easy to understand CPU architecture implemented in Logisim.

## Features
- Detailed Manual [here](docs/main.pdf)
- 30 32-bit General Purpose Registers
- CMP Register (results of comparison)
- Hardware Stack and Stack Pointer (SP is a register)
- 32-bit Instructions
- Multitude of operations (check manual for specifics):
  - Arithmetic
  - Logical
  - Memory
  - Control Flow
- Simple Instruction Set and Assembly Language
- Easy to use Assembler

## Usage
1. Clone the [repository](https://github.com/aschombe/microRISC)
2. Open a terminal and navigate to the root of the repository
3. Run the assembler with the following command:
```bash
python3 as.py <input_file_name>
```
4. Open Logisim and load the `microRISC.circ` file
5. Load instructions.o into the Instruction Memory, data.o into the Data Memory
6. Run the simulation

## TODO List
- [ ] Manual
- [ ] Design the architecture/spec
    - [ ] Outline memory layouts
    - [ ] Decide how stack will work
- [x] Define the instruction set
- [ ] Implement the architecture in Logisim
    - [x] PC
    - [ ] RegFile
    - [ ] ALU
    - [ ] Control Unit
    - [ ] Memory Unit
- [ ] Write an assembler
    - [ ] Maybe add line, column and snippet information to error output
    - [ ] Decide how to handle data section
