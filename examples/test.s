<data>
foo:  0
bar:  1

<text>
// Entry point
start:
    NOP                 // literally does nothing
    MOV  R1, 0          // R1 := 0
    MOV  R2, 1          // R2 := 1
    ADD  R3, R1, R2     // R3 := 1

    // Load from data and store back
    ADR  R4, foo        // R4 := address of foo
    LDR  R5, R4, 0      // R5 := mem[foo]
    STR  R5, R4, 0      // mem[foo] := R5 (no change)

    // Simple compare and branch that falls through
    CMP  R1, R1         // set CMP = equal
    BEQ  done           // always taken here

    NOP                 // skipped

done:
    RET                 // return to LR (or end of program)
