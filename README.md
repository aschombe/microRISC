# microRISC
microRISC is a easy to understand CPU architecture implemented in Logisim.

## Features
- Detailed Manual [here](docs/manual.pdf)
- 30 32-bit General Purpose Registers
- CMP Register (results of comparison)
- Cache (planned)
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
    - [ ] Introduction
    - [ ] Architecture
    - [ ] Instruction Set
    - [ ] Assembly Language
    - [ ] Assembler
    - [ ] Examples
- [x] Design the architecture/spec
- [x] Define the instruction set
- [ ] Implement the architecture in Logisim
    - [x] PC
    - [x] RegFile
    - [ ] ALU
    - [ ] Control Unit
    - [ ] Memory Unit
    - [ ] Cache
- [x] Write an assembler
