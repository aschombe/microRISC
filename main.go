package main

import (
	"fmt"
	"os"
	"strings"

	"microRISC/toolchain/assembler"
	"microRISC/toolchain/parser"
	"microRISC/toolchain/tokenizer"
)

func read_file(filename string) (string, error) {
	// open the file
	file, err := os.Open(filename)
	if err != nil {
		return "", err
	}
	defer file.Close()

	// read the file
	data := make([]byte, 1024)
	count, err := file.Read(data)
	if err != nil {
		return "", err
	}

	// convert the data to a string
	return string(data[:count]), nil
}

// reads the file, tokenize it, parses it, assembles it
func process_file(filename string, output string) error {
	// read the file
	source, err := read_file(filename)
	if err != nil {
		fmt.Println("Error:", err)
		return err
	}

	// tokenize the source code using the tokenizer package
	instructions, data, err := tokenizer.TokenizeSource(source)
	if err != nil {
		fmt.Println("Error:", err)
		return err
	}

	// parse the tokens into an AST using the parser package
	program, err := parser.ParseTokens(instructions, data)
	if err != nil {
		fmt.Println("Error:", err)
		return err
	}

	// assemble the program using the assembler package
	err = assembler.Assemble(program, output)
	if err != nil {
		fmt.Println("Error:", err)
		return err
	}

	return nil
}

func main() {
	help := `Usage: ./as <input>.s [-oh] <output>
    Options:
    -o <output>     Specify the output file (optional, default output is <input_filename>.hex)
    -h              Display this help message

    Examples:
    ./as -h                     // displays this help message
    ./as input.s -o output.bin  // assembles input.s to output.bin
    ./as input.s                // assembles input.s to input.hex
	`

	// get the arguments (excluding the program name)
	args := os.Args[1:]

	// if there are no arguments, print the help message
	if len(args) == 0 {
		fmt.Println(help)
		return
	}

	// if there are more than 3 arguments, print an error message
	if len(args) > 3 {
		fmt.Println("Error: too many arguments")
		fmt.Println(help)
		return
	}

	// if the first argument is -h, print the help message
	if args[0] == "-h" {
		fmt.Println(help)
		return
	}

	// if the first argument is not a file, print an error message
	if _, err := os.Stat(args[0]); os.IsNotExist(err) {
		fmt.Println("Error: file does not exist")
		return
	}

	// check if the file has the .s extension
	// if it doesn't, print an error message
	if !strings.HasSuffix(args[0], ".s") {
		fmt.Println("Error: file must have the .s extension")
		return
	}

	// switch on the number of arguments
	switch len(args) {
	case 3:
		if args[1] != "-o" {
			fmt.Println("Error: invalid flag " + args[1])
			fmt.Println(help)
			return
		}

		err := process_file(args[0], args[2])
		if err != nil {
			fmt.Println("Error:", err)
			return
		}

	case 2:
		fmt.Println("Error: missing output file")
		fmt.Println(help)
		return
	case 1:
		err := process_file(args[0], strings.TrimSuffix(args[0], ".s")+".hex")
		if err != nil {
			fmt.Println("Error:", err)
			return
		}
	}

	return
}
