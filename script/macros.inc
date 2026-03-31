; All macro definitions from m6502
; Manually converted to ca65 format

;.macro ROR WD
;    ROR WD
;.endmacro

.macro ACRLF
	.byt 13, 10
.endmacro

.macro SYNCHK Q
	LDA #Q
	JSR	SYNCHR
.endmacro

.macro DT Q
    .byt Q
.endmacro

.macro LDWD	WD
	LDA	WD
	LDY	WD + 1
.endmacro

.macro LDWDI WD
	LDA #<WD
	LDY #>WD
.endmacro

.macro LDWX	WD
	LDA	WD
	LDX	WD+1
.endmacro

.macro LDWXI WD
	LDA #(WD & $ff)
	LDX #(WD >> 8)
.endmacro

.macro LDXY	WD
	LDX	WD
	LDY	WD+1
.endmacro

.macro LDXYI WD
	LDX #(WD) & 255
	LDY #(WD >> 8) & 255
.endmacro

.macro STWD WD
	STA	WD
	STY	WD+1
.endmacro

.macro STWX	WD
	STA	WD
	STX	WD+1
.endmacro

.macro STXY	WD
	STX	WD
	STY	WD+1
.endmacro

.macro CLR WD
	LDA #0
	STA	WD
.endmacro

.macro COM WD
	LDA	WD
	EOR #$ff
	STA	WD
.endmacro

.macro PULWD WD
	PLA
	STA	WD
	PLA
	STA	WD+1
.endmacro

.macro PSHWD WD
	LDA	WD+1
	PHA
	LDA	WD
	PHA
.endmacro

.macro JEQ WD
	BNE	*+5
	JMP	WD
.endmacro

.macro JNE WD
	BEQ	*+5
	JMP	WD
.endmacro

.macro BCCA Q   ;BRANCHES THAT ALWAYS BRANCH
    BCC	Q       ;THESE ARE USED ON THE 6502 BECAUSE
.endmacro       ;THERE IS NO UNCONDITIONAL BRANCH
.macro BCSA Q
    BCS	Q
.endmacro
.macro BEQA Q
    BEQ	Q
.endmacro
.macro BNEA Q
    BNE	Q
.endmacro
.macro BMIA Q
    BMI	Q
.endmacro
.macro BPLA Q
    BPL	Q
.endmacro
.macro BVCA Q
    BVC	Q
.endmacro
.macro BVSA Q
    BVS	Q
.endmacro
.macro INCW R
	INC	R
	BNE	:+
	INC	R+1
:
.endmacro

.macro SKIP1
    .byt $24    ;BIT ZERO PAGE TRICK.
.endmacro

.macro SKIP2
    .byt $2c    ;BIT ABS TRICK.
.endmacro

.macro ADR WD
	.word WD
.endmacro

; - On line 1250, DCE
