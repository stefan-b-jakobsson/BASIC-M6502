import common
import blocks

# All operator handlers must use the following interface:
# Input:
#   - array: Tokenized elements from one source line
#   - int: Index of the current element in that array
# Output:
#   - int: Number of elements consumed by the operators, counting from index

def unsupported(t, index):
    raise Exception("Unsupported pseudo op: " + t[index] + " at line " + str(common.row))
    common.outbuf += t[index] + " "
    return 1

def suppress_block(t, index):
    found_comma = False
    for x in range(index+1,len(t)):
        if t[x] == ",":
            found_comma = True
        if t[x] == "<" and found_comma:
            blocks.push(False, "")
            return x - index + 1
    raise Exception("Code block start not found")

def suppress_line(t, index):
    return len(t)-index

def title(t, index):
    common.outbuf += "; "
    for x in range(index, len(t)):
        common.outbuf += t[x] + " "
    return len(t)-index

def org(t, index):
    common.org = common.eval_expr(t, index+1)[0]

    if t[index+1] == "0":
        common.outbuf += ".ZEROPAGE "
    elif t[index+1] == "255":
        common.outbuf += ".SEGMENT \"PAGE1\" "
    elif t[index+1] == "ROMLOC":
        common.outbuf += ".CODE "
    else:
        raise Exception("Unsupported segment: " + str(t[index+1]))
    return 2

def ife(t, index):
    expr = common.eval_expr(t, index+1, True)

    if expr[0] == 0:
        blocks.push(True, "")
    else:
        blocks.push(False, "")
    
    return expr[1] + 3

def ifn(t, index):
    expr = common.eval_expr(t, index+1, True)

    if expr[0] != 0:
        blocks.push(True, "")
    else:
        blocks.push(False, "")
    
    return expr[1] + 3

def define(t, index):
    for x in range(index+1, len(t)):
        if t[x] == "<":
            blocks.push(False, "")
            return x - index + 1

def radix(t, index):
    # Suppress line, but store radix
    common.radix = int(t[index+1])
    return len(t)-index

def comment(t, index):
    common.block_comment_char = t[index+1]
    common.outbuf += "; "
    return 2

def dci(t, index):
    common.constants["Q"] += 1
    common.outbuf += ".byt " + t[index+1][:-2] + "\", '" + t[index+1][-2] + "'+128"
    return 2

def dce(t, index):
    common.constants["Q"] += 2
    common.outbuf += ".byt " + t[index+1]
    return 2

def if1(t, index):
    found_comma = False
    for x in range(index+1,len(t)):
        if t[x] == ",":
            found_comma = True
        if t[x] == "<" and found_comma:
            blocks.push(True, "")
            return x - index + 1
    raise Exception("Code block start not found")

def printx(t, index):
    common.outbuf += ".out \""
    for x in range(index+1,len(t)):
        if t[x] != ">":
            if x > index + 1:
                common.outbuf += " "
            common.outbuf += t[x]
    common.outbuf += "\" "
    return x-index

def block(t, index):
    common.outbuf += ".res "
    common.outbuf += t[index+1] + " "
    return 2

def exp(t, index):
    # From the MACRO-10 manual:
    #   "EXP Statement: Several numbers and expressions may be entered by using the EXP statement:
    #       EXP X,4,^D65,HALF,B+362-A
    #   which generates one word for each expression; five words were generated for the above
    #   example."
    # This would be equivalent to .byt in ca65. The EXP statement is, however, also used also in
    # uninitialized RAM code, where you would use .res statements in ca65. This handler outputs
    # .res statements if the current segment is in uninitialized RAM (i.e < RAMLOC), otherwise 
    # .byt statements

    if common.org < common.constants["RAMLOC"]:
        common.outbuf += ".res "
        cnt = 0
        for x in range(index+1, len(t)):
            if t[x][0] in [";", ">"]:
                break
            elif t[x] !=",":
                cnt+=1
        common.outbuf += str(cnt) + " "
    
    else:    
        common.outbuf += ".byt "
        for x in range(index+1,len(t)):
            if t[x][0] in [";", ">"]:
                break
            else:
                common.outbuf += t[x]
    
        common.outbuf += " "
    return x-index

def repeat(t, index):
    common.outbuf += ".repeat "
    v = common.eval_expr(t, index+1)
    common.outbuf += str(v[0]) + "\n"

    for x in range(index+v[1], len(t)):
        if t[x] == "<":
            blocks.push(True, "\n.endrepeat\n")
            return x-index+1

    raise Exception("Start of block for repeat not found at line " + str(common.row))

def xwd(t, index):
    if common.org < common.constants["RAMLOC"]:
        raise Exception("XWD instruction in uninitialized memory section at line " + str(common.row))

    common.outbuf += ".byt "
    commafound = False
    for x in range(index+1, len(t)):
        if t[x] == ",":
            return x - index + 1
    raise Exception("XWD instruction without second parameter at line " + str(common.row))

def ifndef(t, index):
    if t[index+1] in common.labels.keys() or t[index+1] in common.constants.keys():
        # Defined, suppress block
        foundcomma = False
        for x in range(index+2, len(t)):
            if t[x] == ",":
                commafound = True
            elif t[x] == "<" and commafound:
                blocks.push(False, "")
                return x - index + 1
        raise Exception("Start of code block not found at line " + str(common.row))

    else:
        # Not found, 
        foundcomma = False
        for x in range(index+2, len(t)):
            if t[x] == ",":
                commafound = True
            elif t[x] == "<" and commafound:
                blocks.push(True, "")
                return x - index + 1
        raise Exception("Start of code block not found at line " + str(common.row))

def dt(t, index):
    common.outbuf += ".byt " + t[index+1] + " "
    return 2

def adr(t, index):
    end = 0

    expr = ""
    for x in range(index+1,len(t)):
        expr += t[x]
        if t[x] == ")":
            end = x
            break
        
    if end == 0:
        raise Exception("Closing parenthesis not found at line " + str(common.row))

    if common.org < common.constants["RAMLOC"]:
        common.outbuf += ".res 2 "
    else:
        common.outbuf += "ADR" + expr + " "
    
    return end - index + 1
        
operators = {
    "ORG": org,
    "ARRAY": unsupported, 
    "ASCII": unsupported,
    "ASCIZ": unsupported,
    "ASUPPRESS": unsupported,
    "BLOCK": block,
    "BYTE": unsupported,
    "COMMENT": comment,
    # "DEC": removed as it's obviously not used for this purpose in the source code
    "DEFINE": define,
    "DEPHRASE": unsupported,
    #"END": unsupported,
    "ENTRY": unsupported,
    "EXP": exp,
    "EXTERN": unsupported,
    "HISEG": unsupported,
    "INTEGER": unsupported,
    "INTERN": unsupported,
    "IOWD": unsupported,
    "IRP": unsupported,
    "IRPC": unsupported,
    "LALL": unsupported,
    #"LIST": unsupported,
    "LIT": unsupported,
    "LOC": unsupported,
    "MLOFF": unsupported,
    "MLON": unsupported,
    "NOSYM": unsupported,
    "OCT": unsupported,
    "OPDEF": unsupported,
    "PAGE": suppress_line,
    "PASS2": unsupported,
    "PHASE": unsupported,
    "POINT": unsupported,
    "PRGEND": unsupported,
    "PRINTX": printx,
    "PURGE": unsupported,
    "RADIX": radix,
    "RADIX50": unsupported,
    "RELOC": unsupported,
    "REMARK": unsupported,
    "REPEAT": repeat,
    "RIM": unsupported,
    "RIM10": unsupported,
    "RIM10B": unsupported,
    "SALL": suppress_line,
    "SEARCH": suppress_line,
    "SIXBIT": unsupported,
    "SQUOZE": unsupported,
    "STOPI": unsupported,
    "SUBTTL": title,
    "SUPPRESS": unsupported,
    "SYN": unsupported,
    "TAPE": unsupported,
    "TITLE": title,
    "TWOSEG": unsupported,
    "UNIVERSAL": unsupported,
    "VAR": unsupported,
    "XALL": unsupported,
    "XLIST": suppress_line,
    "XPURGE": unsupported,
    "XWD": xwd,
    "Z": unsupported,
    ".CREF": unsupported,
    ".XCREF": unsupported,
    ".HWFRMT": unsupported,
    ".MFRMT": unsupported,
    "IF1": if1,
    "IF2": suppress_block,
    "IFB": unsupported,
    "IFDEF": unsupported,
    "IFDIF": unsupported,
    "IFE": ife,
    "IFG": unsupported,
    "IFGE": unsupported,
    "IFIDN": unsupported,
    "IFL": unsupported,
    "IFLE": unsupported,
    "IFN": ifn,
    "IFNB": unsupported,
    "IFNDEF": ifndef,

    # Macros that cannot handled by ca65
    "DCI": dci,
    "DCE": dce,
    "DT": dt,
    "ADR": adr,
}
