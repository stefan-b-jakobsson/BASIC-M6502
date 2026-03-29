import common
import blocks
import macro10
import op6502
import re

def read_line(f):
    """
    Reads and returns one line of text from the opened file f
    """
    
    l = ""
    while (True):
        c = f.read(1)
        if c == chr(10):
            return l.upper()
        elif c == chr(13):
            pass
        elif not c:
            return l.upper()
        else:
            l += c

def tokenize_line(l):
    """
    Tokenizes one line of code
    """

    start = 0
    quotes = 0
    out = []

    for i in range(0, len(l)):
        if l[i] not in common.symbolchars:
            if start < i and quotes & 1 == 0:
                out.append(l[start:i])
                start = i

            if l[i] == '"':
                quotes += 1
                if quotes & 1 == 0:
                    out.append(l[start:i+1])
                    start = i + 1
                    continue

            if quotes & 1 == 0:
                if l[i] == ';':
                    start = i
                    break
                elif l[i] not in common.whitespace:
                    out.append(l[i])
                    start = i + 1
                else:
                    # Ignore white space
                    start = i + 1

    if start < len(l):
        out.append(l[start:])

    return out

def is_symbol(s):
    if s[0] < 'A' or s[0] > 'Z':
        return False

    for c in s:
        if c not in common.symbolchars:
            return False
    return True

def is_value(s):
    for c in s:
        if c not in common.symbolchars:
            return False
    return True

def parse_line(t):
    common.outbuf = ""
    index = 0

    while (index<len(t)):
        # Multiline comment ?
        if common.block_comment_char != None and t[index] == common.block_comment_char:
            common.block_comment_char = None
            index += 1
            continue

        elif common.block_comment_char:
            if index==0:
                common.outbuf += "; "
            common.outbuf += t[index] + " "
            index += 1
            continue

        # Opening or closing angle brackets ?
        elif t[index] == ">":
            cur = blocks.pop()
            if cur[0]:
                common.outbuf += cur[1] + " "
            index += 1    
            continue
        
        elif t[index] == "<":
            blocks.push(None, ")")
            if blocks.cur() == True:
                common.outbuf += "("
            index +=1
            continue

        # Hidden block ?
        elif blocks.cur() == False:
            index += 1
            continue

        # Inline comment?
        elif t[index][0] == ";":
            common.outbuf += t[index] + " "
            return

        # Numeric expression at start of line => store as byte
        elif ((len(common.outbuf) == 0) or (index > 0 and t[index-1]==":")) and (t[index] == "^" or t[index].isnumeric() or (t[index] in common.constants.keys() and t[index+1] != "=")):
            if common.org < 256:
                common.outbuf += ".res 1"
                index += 2
            else:
                common.outbuf += ".byt "
                index += common.num_format(t, index)

        # Symbol ?
        elif is_symbol(t[index]):
            # Label definition?
            if len(t)>1 and index == 0 and t[1]==":":
                common.labels[t[index]] = common.row
                common.outbuf += t[index] + ": "
                index += 2
            
            # Constant definition ?
            elif len(t)>index+1 and t[index+1] == "=":
                try:
                    common.constants[t[index]] = int(common.eval_expr(t,index+2)[0])
                except:
                    common.constants[t[index]] = common.eval_expr(t,index+2)[0]
                common.constants_defined_at[t[index]] = common.row
                
                # Output constant name, unless it's the special variable "Q"
                if t[index] != "Q":
                    common.outbuf += t[index] + " "
                    index += 1
                else:
                    return
            
            # The special Q variable ?
            elif t[index] == "Q":
                common.outbuf += str(common.constants["Q"])
                index += 1

            # 6502 Opcode ?
            elif t[index] in op6502.operators:
                index += op6502.operators[t[index]](t, index)

            # MACRO-10 operator ?
            elif t[index] in macro10.operators:
                index += macro10.operators[t[index]](t, index)

            else:
                common.outbuf += t[index] + " "
                index += 1

        else:
            if t[index] == "^":
                index += common.num_format(t, index) - 1
            # Kill double equal signs
            elif t[index] == '=' and t[index-1] == '=':
                pass
            # Replace angle brackets
            elif t[index] == "<":
                common.outbuf += "("
            elif t[index] == ">":
                common.outbuf += ")"
            # Trailing comma ?
            elif t[index] == "," and (index == len(t)-1 or t[index+1][0]==";"):
                pass
            # Single char string?
            elif t[index][0] == "\"" and len(t[index])==3:
                common.outbuf += t[index].replace("\"", "'")
            # Number?
            elif t[index].isnumeric():
                index += common.num_format(t,index) - 1
            # Everything else
            else:
                common.outbuf += t[index] + " "
            index += 1

def format_line():
    print (common.outbuf)


# main
f = open("../m6502.asm", "r")
print(".include \"macros.inc\"")
row = 1
for r in range(1,6956):
    common.row = r
    l = read_line(f)
    t = tokenize_line(l)
    parse_line(t)
    if (len(l) > 0 and len(common.outbuf) > 0) or len(l) == 0:
        format_line()
f.close()   
