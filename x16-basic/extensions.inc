SETNAM = $ffbd
SETLFS = $ffba
LOAD = $ffd5
SAVE = $ffd8

; *****************************************************************************
; Purpose...............: SYS command handler 
; Input.................: None
; Output................: None
; Preparatory rutines...: None
; Errors................: None
; Registers affected....: .A, .X, .Y
; Credits...............: New implementation, not based on previous work
.proc sys_command
    jsr FRMNUM ; evaluate expression
    jsr GETADR ; get address
    jmp (POKER) ; jump to that address
.endproc

; *****************************************************************************
; Purpose...............: LOAD command handler 
; Input.................: None
; Output................: None
; Preparatory rutines...: None
; Errors................: None
; Registers affected....: .A, .X, .Y
; Credits...............: New implementation, not based on previous work
.proc load_command
    ; Get file name from command
    jsr FRMEVL ; evaluate
    jsr CHKSTR ; make sure it's a string
    jsr FREFAC ; fetch string length into A, and string pointer into INDEX

    ; Setup file name
    ldx INDEX
    ldy INDEX+1
    jsr SETNAM

    ; Device number
    ldx #8 ; default device, SD card
    ldy #0 ; default option, ignore target address in file header

    jsr CHRGOT ; peek next char
    cmp #','
    bne :+ ; next char not a comma, we're done parsing
    jsr CHRGET ; consume comma
    jsr GETBYT ; fetch byte value into X

    ; Target address
    ldy #0 ; default option, ignore target address in file header
    jsr CHRGOT ; peek next char
    cmp #','
    bne :+ ; next char not a comma, we're done parsing
    jsr CHRGET ; consume comma
    phx ; store device number on stack
    jsr GETBYT ; fetch byte value into X
    txa
    tay ; move byte value into Y
    plx ; fetch device from stack

    ; Setup file options, file number not used by Kernal's load function
:   jsr SETLFS ; X = device, Y = ignore (0) or use (>0) target address in file header

    ; Finally, go ahead and load that file
    lda #0 ; load command
    ldx #<(RAMLOC+1)
    ldy #>(RAMLOC+1)
    jsr LOAD
    bcs exit ; exit if load command failed

    ; Else update pointer
    stx VARTAB
    sty VARTAB+1

exit:
    rts
.endproc

; *****************************************************************************
; Purpose...............: SAVE command handler 
; Input.................: None
; Output................: None
; Preparatory rutines...: None
; Errors................: None
; Registers affected....: .A, .X, .Y
; Credits...............: New implementation, not based on previous work
.proc save_command
    ; Get file name from command
    jsr FRMEVL ; evaluate
    jsr CHKSTR ; make sure it's a string
    jsr FREFAC ; fetch string length into A, and string pointer into INDEX

    ; Setup file name
    ldx INDEX
    ldy INDEX+1
    jsr SETNAM

    ; Device number
    ldx #8 ; default device, SD card
    jsr CHRGOT ; peek next char
    cmp #','
    bne :+ ; next char not a comma, we're done parsing
    jsr CHRGET ; consume comma
    jsr GETBYT ; fetch byte value into X

    ; Setup file options
:   jsr SETLFS ; X = device

    ; Save start address in FACMO/FACLO
    lda #<(RAMLOC+1)
    sta FACMO
    lda #>(RAMLOC+1)
    sta FACLO

    ; Go ahead, save that file
    lda #FACMO
    ldx VARTAB
    ldy VARTAB+1
    jsr SAVE
    
exit:
    rts
.endproc
