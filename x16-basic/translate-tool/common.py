import blocks

constants = dict()
constants_defined_at = dict()
labels = dict()
symbolchars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','$','%','.']
whitespace = [chr(9), chr(10), chr(13), chr(32), chr(160)]

row = 0
outbuf = ""
radix = 10
block_comment_char = None
org = 0

def num_format(t, index):
    global outbuf
    global radix
    
    if t[index] == "^":
        if t[index+1][0] == "O":
            outbuf += hex(int(t[index+1][1:], 8)).replace("0x", "$")
            return 2
        elif t[index+1][0] == "D":
            outbuf += t[index+1][1:]
            return 2
        else:
            raise Exception("Unsupported number format:" + t[index] + " " + t[index+1])
    elif t[index].isnumeric():
        outbuf += str(int(t[index], radix)) + " "
        return 1
    else:
        outbuf += t[index] + " "
        return 1

def eval_expr(t, index, strict=False):
    global constants
    ew = blocks.endswith.copy() # Make a local copy
    expr = ""
    x = index
    while x < len(t):
        if t[x] == "<":
            expr += "("
            ew.append(")")
            x += 1
        elif t[x] == ">":
            expr += ew.pop()
            x += 1
        elif t[x] == "=":
            x += 1
        elif t[x] == "^":
            if t[x+1][0] == "O":
                expr += str(int(t[x+1][1:], 8))
                x += 2
            else:
                raise Exception("Unsupported number format:" + t[x] + " " + t[x+1])
        elif t[x].isnumeric():
            expr += str(int(t[x], radix))
            x += 1
        elif t[x][0] in [",", ";"]:
            break
        else:
            expr += str(t[x])
            x += 1

    if strict:
        return [eval(expr.replace("/", "//").replace("!", "|"), constants), x-index]
    else:
        try:
            return [eval(expr.replace("/", "//"), constants), x-index]
        except:
            return [expr, x-index]
