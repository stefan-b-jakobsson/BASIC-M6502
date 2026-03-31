;(C) 2021 Stefan Jakobsson, License: 2-clause BSD

rom_bank   = $01
jsrfar3    = $02c4 ; jsrfar: RAM part
jmpfr      = $02df ; jsrfar: core jmp instruction
banked_irq = $038b ; irq handler: RAM part

.segment "KTARGET"

jsr_kernal:
    ;Reserve 1 extra byte on the stack, used to store current ROM bank
    pha
    
    ;Save input values
    php
    pha
    phx

    ;Get stack pointer
    tsx

    ;Set Kernal call address (=return address on stack-2)
    sec
    lda $0105,x
    sbc #2
    sta jmpfr+1
    lda $0106,x
    sbc #0
    sta jmpfr+2

    ;Save current bank on stack in extra byte
    lda rom_bank
    sta $0104,x

    ;Change return address
    lda #<(jsr_kernal_done-1)
    sta $0105,x
    lda #>(jsr_kernal_done-1)
    sta $0106,x

    ;Restore X
    plx

    ;Select Kernal ROM bank
    lda #0

    ;Jump to Kernal function
    jmp jsrfar3

jsr_kernal_done:
    rts

.segment "VECTORS"
    ;fec0-ff7f = 64 entries
    .repeat 64
        jsr jsr_kernal
    .endrepeat

    ;ff80
    .byt 0

    ;ff81-fff8 = 40 entries
    .repeat 40
        jsr jsr_kernal
    .endrepeat

    ;fff9
    .byt 0
