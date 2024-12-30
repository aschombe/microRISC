package parser

import (
	"fmt"
	"microRISC/toolchain/tokenizer"
)

// InstructionNode represents an instruction in the program
type InstructionNode struct {
	Opcode   string   // The opcode (e.g., ADD, MOV, etc.)
	Operands []string // The operands (e.g., registers, immediates)
	Label    string   // Optional label associated with the instruction
}

// DataNode represents a label and its associated data values
type DataNode struct {
	Label  string   // The label (e.g., "age")
	Values []string // The values (e.g., "21", "90", "85")
}

// ProgramNode is the root of the AST that holds the instructions and data
type ProgramNode struct {
	Instructions []InstructionNode // A list of instructions
	Data         []DataNode        // A list of data labels and their values
}

// transform the tokens into an AST
func ParseTokens(instructions []tokenizer.Instruction, data map[string][]string) (ProgramNode, error) {
	var program ProgramNode

	for _, instr := range instructions {
		program.Instructions = append(program.Instructions, InstructionNode{
			Opcode:   instr.Opcode,
			Operands: instr.Operands,
			Label:    instr.Label,
		})
	}

	for label, values := range data {
		program.Data = append(program.Data, DataNode{
			Label:  label,
			Values: values,
		})
	}

	return program, nil
}

func PrintAST(program ProgramNode) {
	fmt.Println("Instructions:")
	for _, instr := range program.Instructions {
		fmt.Printf("Opcode: %s, Operands: %v, Label: %s\n", instr.Opcode, instr.Operands, instr.Label)
	}

	fmt.Println("\nData:")
	for _, data := range program.Data {
		fmt.Printf("Label: %s, Values: %v\n", data.Label, data.Values)
	}
}
