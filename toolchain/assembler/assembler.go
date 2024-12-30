package assembler

import (
	"fmt"
	"os"
	"strconv"

	"microRISC/toolchain/parser"
)

// Instruction set with opcodes and expected token counts
var instructionSet = map[string]map[string]string{
	"ADD":  {"opcode": "000000", "type": "three_reg", "expected_count": "4"},
	"SUB":  {"opcode": "000001", "type": "three_reg", "expected_count": "4"},
	"MUL":  {"opcode": "000010", "type": "three_reg", "expected_count": "4"},
	"DIV":  {"opcode": "000011", "type": "three_reg", "expected_count": "4"},
	"AND":  {"opcode": "000100", "type": "three_reg", "expected_count": "4"},
	"ORR":  {"opcode": "000101", "type": "three_reg", "expected_count": "4"},
	"XOR":  {"opcode": "000110", "type": "three_reg", "expected_count": "4"},
	"LSL":  {"opcode": "000111", "type": "three_reg", "expected_count": "4"},
	"LSR":  {"opcode": "001000", "type": "three_reg", "expected_count": "4"},
	"ASR":  {"opcode": "001001", "type": "three_reg", "expected_count": "4"},
	"NEG":  {"opcode": "001010", "type": "one_reg", "expected_count": "2"},
	"ADDI": {"opcode": "001011", "type": "two_reg", "expected_count": "4"},
	"SUBI": {"opcode": "001100", "type": "two_reg", "expected_count": "4"},
	"MULI": {"opcode": "001101", "type": "two_reg", "expected_count": "4"},
	"DIVI": {"opcode": "001110", "type": "two_reg", "expected_count": "4"},
	"LDR":  {"opcode": "010000", "type": "three_reg", "expected_count": "4"},
	"STR":  {"opcode": "010001", "type": "three_reg", "expected_count": "4"},
	"ADR":  {"opcode": "010010", "type": "reg_label", "expected_count": "3"},
	"B":    {"opcode": "100000", "type": "label", "expected_count": "2"},
	"BL":   {"opcode": "100001", "type": "label", "expected_count": "2"},
	"BEQ":  {"opcode": "100010", "type": "label", "expected_count": "2"},
	"BNE":  {"opcode": "100011", "type": "label", "expected_count": "2"},
	"BGT":  {"opcode": "100100", "type": "label", "expected_count": "2"},
	"BLT":  {"opcode": "100101", "type": "label", "expected_count": "2"},
	"BGE":  {"opcode": "100110", "type": "label", "expected_count": "2"},
	"BLE":  {"opcode": "100111", "type": "label", "expected_count": "2"},
	"NOP":  {"opcode": "110000", "type": "no_op", "expected_count": "1"},
	"RET":  {"opcode": "110001", "type": "no_op", "expected_count": "1"},
	"MOV":  {"opcode": "110010", "type": "dynamic", "expected_count": "0"},
	"MOVI": {"opcode": "110011", "type": "dynamic", "expected_count": "0"},
	"CMP":  {"opcode": "110100", "type": "two_reg", "expected_count": "3"},
	"CBZ":  {"opcode": "110101", "type": "reg_label", "expected_count": "3"},
	"CBNZ": {"opcode": "110110", "type": "reg_label", "expected_count": "3"},
}

// Register map (mapping R0-R31 to binary equivalents)
var registerMap = map[string]string{
	"R0": "00000", "R1": "00001", "R2": "00010", "R3": "00011", "R4": "00100", "R5": "00101",
	"R6": "00110", "R7": "00111", "R8": "01000", "R9": "01001", "R10": "01010", "R11": "01011",
	"R12": "01100", "R13": "01101", "R14": "01110", "R15": "01111", "R16": "10000", "R17": "10001",
	"R18": "10010", "R19": "10011", "R20": "10100", "R21": "10101", "R22": "10110", "R23": "10111",
	"R24": "11000", "R25": "11001", "R26": "11010", "R27": "11011", "R28": "11100", "R29": "11101",
	"R30": "11110", "R31": "11111",
}

// Convert binary string to integer
func binaryToInt(binaryStr string) (int64, error) {
	return strconv.ParseInt(binaryStr, 2, 32)
}

// Convert instruction to machine code (binary)
func assembleInstruction(instruction string, tokens []string) (string, error) {
	// Lookup the instruction in the instruction set
	instr, ok := instructionSet[instruction]
	if !ok {
		return "", fmt.Errorf("unknown instruction: %s", instruction)
	}

	// Get the opcode for the instruction
	opcode := instr["opcode"]
	typ := instr["type"]

	// Handle different instruction types
	switch typ {
	case "three_reg":
		if len(tokens) != 4 {
			return "", fmt.Errorf("instruction %s requires 4 tokens", instruction)
		}
		// Format: opcode + reg1 + reg2 + reg3
		reg1 := registerMap[tokens[1]]
		reg2 := registerMap[tokens[2]]
		reg3 := registerMap[tokens[3]]
		return opcode + reg1 + reg2 + reg3, nil

	case "two_reg":
		if len(tokens) != 4 {
			return "", fmt.Errorf("instruction %s requires 4 tokens", instruction)
		}
		// Format: opcode + reg1 + immediate
		reg1 := registerMap[tokens[1]]
		immediate := tokens[2] // Assuming immediate is already a binary string
		return opcode + reg1 + immediate, nil

	case "one_reg":
		if len(tokens) != 2 {
			return "", fmt.Errorf("instruction %s requires 2 tokens", instruction)
		}
		// Format: opcode + reg1
		reg1 := registerMap[tokens[1]]
		return opcode + reg1, nil

	case "label":
		if len(tokens) != 2 {
			return "", fmt.Errorf("instruction %s requires 2 tokens", instruction)
		}
		// For label-based instructions, we will handle label resolution elsewhere
		label := tokens[1]
		return opcode + label, nil

	case "reg_label":
		if len(tokens) != 3 {
			return "", fmt.Errorf("instruction %s requires 3 tokens", instruction)
		}
		// Format: opcode + reg1 + label
		reg1 := registerMap[tokens[1]]
		label := tokens[2]
		return opcode + reg1 + label, nil

	case "no_op":
		if len(tokens) != 1 {
			return "", fmt.Errorf("instruction %s requires 1 token", instruction)
		}
		// No operands for this instruction
		return opcode, nil
	default:
		return "", fmt.Errorf("unsupported instruction type: %s", typ)
	}
}

// Write machine code to file
func writeMachineCodeToFile(machineCode []string, filename string) error {
	// Create file
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	// Write header for hex format
	file.WriteString("v3.0 hex words addressed\n")

	// Write each instruction as hex
	for i, code := range machineCode {
		hexCode, err := binaryToInt(code)
		if err != nil {
			return fmt.Errorf("error converting binary to int: %v", err)
		}
		file.WriteString(fmt.Sprintf("%02x: %08x\n", i, hexCode))
	}
	return nil
}

func Assemble(program parser.ProgramNode, output string) error {
	var machineCode []string
	for _, instr := range program.Instructions {
		binaryCode, err := assembleInstruction(instr.Opcode, instr.Operands)
		if err != nil {
			return err
		}
		machineCode = append(machineCode, binaryCode)
	}

	// Write machine code to file
	err := writeMachineCodeToFile(machineCode, output)
	if err != nil {
		return err
	}

	return nil
}
