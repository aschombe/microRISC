package ast

// OperandNode represents a single operand in an instruction (either a register or a literal value).
type OperandNode struct {
	Type  string // "register", "immediate", or "label"
	Value string
}

// InstructionNode represents an instruction in the AST.
type InstructionNode struct {
	Instruction string
	Operands    []*OperandNode
}

// LabelNode represents a label in the code.
type LabelNode struct {
	Label string
}
