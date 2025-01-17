# microRISC
microRISC is a easy to understand CPU architecture implemented in Logisim.

## Features
- Detailed Manual [here](docs/manual.pdf)
- 32 32-bit General Purpose Registers
- CMP Register (results of comparison)
- LR Register (Link Register)
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
python3 assembler/main.py <input_file_name>
```
This will generate two files in the directory of where you ran the command:
- `instructions.hex` which contains the machine code of the program
- `ram.hex` which contains the data section of the program (if you declared one)

4. Open Logisim and load the `microRISC.circ` file
5. Load `instructions.hex` into the Instruction Memory, `ram.hex` into the Data Memory (if you declared a data section)
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
