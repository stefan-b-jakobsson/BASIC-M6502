; *****************************************************************************
; Copyright 2026 Stefan Jakobsson
;
; Redistribution and use in source and binary forms, with or without 
; modification, are permitted provided that the following conditions are met:
;
; 1. Redistributions of source code must retain the above copyright notice, 
;    this list of conditions and the following disclaimer.
;
; 2. Redistributions in binary form must reproduce the above copyright notice, 
;    this list of conditions and the following disclaimer in the documentation 
;    and/or other materials provided with the distribution.
;
; THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
; AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
; IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
; ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
; LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
; CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
; SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
; INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
; CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
; ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
; POSSIBILITY OF SUCH DAMAGE.
; *****************************************************************************

rom_bank   = $01
jsrfar3    = $0307 ; jsrfar: RAM part
jmpfr      = $0322 ; jsrfar: core jmp instruction

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
