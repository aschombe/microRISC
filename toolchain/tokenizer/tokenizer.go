package tokenizer

import (
	"fmt"
	"regexp"
	"strings"
)

// instruction struct to hold the opcode, operands, and label
type Instruction struct {
	Opcode   string
	Operands []string
	Label    string
}

// check if the line is a section header (.data, .text)
func isSectionHeader(line string) (string, bool) {
	line = strings.TrimSpace(line)
	if strings.HasPrefix(line, ".data") {
		return ".data", true
	} else if strings.HasPrefix(line, ".text") {
		return ".text", true
	}
	return "", false
}

// tokenize the source code into instructions and data
func TokenizeSource(source string) ([]Instruction, map[string][]string, error) {
	var instructions []Instruction
	data := make(map[string][]string)

	// split the source code into lines
	lines := strings.Split(source, "\n")

	currentSection := ""
	var currentLabel string

	// iterate over the lines
	for _, line := range lines {
		line = strings.TrimSpace(line)

		// skip empty lines
		if len(line) == 0 {
			continue
		}

		// check if the line is a section header
		if section, isSection := isSectionHeader(line); isSection {
			currentSection = section
			continue
		}

		// tokenize based on the current section
		if currentSection == ".text" {
			instr, err := tokenizeInstruction(line)
			if err != nil {
				return nil, nil, err
			}
			if instr.Label != "" {
				currentLabel = instr.Label
			} else {
				if currentLabel != "" {
					instr.Label = currentLabel
					currentLabel = ""
				}
				instructions = append(instructions, instr)
			}
		} else if currentSection == ".data" {
			label, values, err := tokenizeData(line)
			if err != nil {
				return nil, nil, err
			}
			if label != "" {
				data[label] = values
			}
		}
	}

	return instructions, data, nil
}

// tokenize the instruction line
func tokenizeInstruction(line string) (Instruction, error) {
	line = strings.TrimSpace(line)

	// Convert the instruction to uppercase for case-insensitive matching
	line = strings.ToUpper(line)

	// check if the line has a label
	if strings.Contains(line, ":") {
		labelParts := strings.SplitN(line, ":", 2)
		if len(labelParts) == 2 {
			label := labelParts[0]
			line = strings.TrimSpace(labelParts[1])

			// If the line is empty after removing the label, return the label
			if line == "" {
				return Instruction{Label: label}, nil
			} else {
				return Instruction{}, fmt.Errorf("invalid label format: %s", line)
			}
		}
	}

	// regex patterns for different instruction types
	threeRegPattern := `^(ADD|SUB|MUL|DIV|AND|ORR|XOR|LSL|LSR|ASR) R\d{1,2}, R\d{1,2}, R\d{1,2}$`
	oneRegPattern := `^(NEG) R\d{1,2}$`
	twoRegImmPattern := `^(ADDI|SUBI|MULI|DIVI) R\d{1,2}, R\d{1,2}, \d+$`
	threeRegMemPattern := `^(LDR|STR) R\d{1,2}, \[R\d{1,2}, R\d{1,2}\]$`
	regLabelPattern := `^(ADR|CBZ|CBNZ) R\d{1,2}, [a-zA-Z_][a-zA-Z0-9_]*$`
	labelPattern := `^(B|BEQ|BNE|BGT|BLT|BGE|BLE) [a-zA-Z_][a-zA-Z0-9_]*$`
	nopPattern := `^(NOP)$`
	movPattern := `^(MOV) R\d{1,2}, R\d{1,2}$`
	moviPattern := `^(MOVI) R\d{1,2}, \d+$`

	// map of instruction types to regex patterns
	patterns := map[string]*regexp.Regexp{
		"three_reg":     regexp.MustCompile(threeRegPattern),
		"one_reg":       regexp.MustCompile(oneRegPattern),
		"two_reg_imm":   regexp.MustCompile(twoRegImmPattern),
		"three_reg_mem": regexp.MustCompile(threeRegMemPattern),
		"reg_label":     regexp.MustCompile(regLabelPattern),
		"label":         regexp.MustCompile(labelPattern),
		"nop":           regexp.MustCompile(nopPattern),
		"mov":           regexp.MustCompile(movPattern),
		"movi":          regexp.MustCompile(moviPattern),
	}

	// match the line with the regex patterns
	for instrType, pattern := range patterns {
		if pattern.MatchString(line) {
			// split by spaces, commas, or brackets and clean up
			tokens := regexp.MustCompile(`\s|,|\[|\]`).Split(line, -1)
			tokens = filterEmptyTokens(tokens)

			var instr Instruction

			switch instrType {
			case "three_reg", "three_reg_mem":
				instr.Opcode = tokens[0]
				instr.Operands = tokens[1:]
			case "two_reg_imm":
				instr.Opcode = tokens[0]
				instr.Operands = tokens[1:]
			case "one_reg":
				instr.Opcode = tokens[0]
				instr.Operands = tokens[1:]
			case "reg_label":
				instr.Opcode = tokens[0]
				instr.Operands = tokens[1:]
			case "label":
				instr.Label = tokens[0][:len(tokens[0])-1] // Remove the colon at the end
			case "nop":
				instr.Opcode = tokens[0]
			case "mov", "movi":
				instr.Opcode = tokens[0]
				instr.Operands = tokens[1:]
			}

			if instr.Label != "" {
				return instr, nil
			}

			return instr, nil
		}
	}

	return Instruction{}, fmt.Errorf("invalid instruction format: %s", line)
}

// tokenize the data line
func tokenizeData(line string) (string, []string, error) {
	line = strings.TrimSpace(line)
	tokens := strings.Split(line, ":")

	if len(tokens) > 2 {
		return "", nil, fmt.Errorf("invalid label format: %s", line)
	}

	if len(tokens) == 2 {
		label := tokens[0]
		values := strings.Split(tokens[1], ",")
		for i := range values {
			values[i] = strings.TrimSpace(values[i])
		}
		return label, values, nil
	}

	return "", nil, fmt.Errorf("invalid data line: %s", line)
}

func filterEmptyTokens(tokens []string) []string {
	var filteredTokens []string
	for _, token := range tokens {
		if token != "" {
			filteredTokens = append(filteredTokens, token)
		}
	}
	return filteredTokens
}
