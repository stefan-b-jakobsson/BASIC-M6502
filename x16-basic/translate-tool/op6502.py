import common

# All handlers must use the following interface:
# Input:
#   - array: Tokenized elements from one source line
#   - int: Index of the current element in that array
# Output:
#   - int: Number of elements consumed by the operators, counting from index

def implicit(t, index):
    common.outbuf += t[index] + " "
    return 1

def immediate(t, index):
    common.outbuf += t[index][0:3] + " #"
    if t[index+1][0] == "\"":
        common.outbuf += t[index+1].replace("\"", "'")
        return 2
    return 1

def absolute(t, index):
    common.outbuf += t[index] + " "
    return 1

def relative(t, index):
    common.outbuf += t[index] + " "
    return 1

def indirect_indexed(t, index):
    common.outbuf += t[index][0:3] + " ("
    for x in range(index+1, len(t)):
        if t[x][0] not in [';', ',']:
            common.num_format(t,x)
        else:
            common.outbuf += "),Y "
            return x-index
    common.outbuf += "),Y "
    return len(t)-index

def indirect(t, index):
    common.outbuf += t[index][0:3] + " ("
    for x in range(index+1, len(t)):
        if t[x][0] not in [';', ',']:
            common.num_format(t,x)
        else:
            common.outbuf += ")"
            return x-index
    common.outbuf += ") "
    return len(t)-index

operators = {
    'LDAI': immediate,
    'BCC': relative,
    'LSR': absolute,
    'ORA': absolute,
    'STA': absolute,
    'JSR': absolute,
    'LDA': absolute,
    'LDY': absolute,
    'LDYI': immediate,
    'LDX': absolute,
    'LDXI': immediate,
    'STY': absolute,
    'STX': absolute,
    'EORI': immediate,
    'PLA': implicit,
    'PHA': implicit,
    'BNE': relative,
    'JMP': absolute,
    'BEQ': relative,
    'BCS': relative,
    'BMI': relative,
    'BPL': relative,
    'BVC': relative,
    'BVS': relative,
    'INC': absolute,
    'CMPI': immediate,
    'SEC': implicit,
    'SBCI': immediate,
    'RTS': implicit,
    'TSX': implicit,
    'INX': implicit,
    'CMP': absolute,
    'TXA': implicit,
    'CLC': implicit,
    'ADCI': immediate,
    'TAX': implicit,
    'SBC': absolute,
    'TAY': implicit,
    'TYA': implicit,
    'DEC': absolute,
    'LDADY': indirect_indexed,
    'STADY': indirect_indexed,
    'DEY': implicit,
    'DEX': implicit,
    'ASL': absolute,
    'CPX': absolute,
    'CPY': absolute,
    'ANDI': immediate,
    'INY': implicit,
    'SBCDY': indirect_indexed,
    'ADC': absolute,
    'CPXI': immediate,
    'NOP': implicit,
    'BIT': absolute,
    'CMPDY': indirect_indexed,
    'TXS': implicit,
    'ORAI': immediate,
    'AND': absolute,
    'CPYI': immediate,
    'ROL': absolute,
    'SEI': implicit,
    'CLI': implicit,
    'PHP': implicit,
    'PLP': implicit,
    'EOR': absolute,
    'JMPD': indirect,
    'ADCDY': indirect_indexed,
}
