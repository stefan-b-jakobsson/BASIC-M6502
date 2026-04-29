level = 0
stack = [True, ]
endswith = [None, ]

def push(visible, endstr):
    global level
    global endswith

    if visible == None:
        stack.append(stack[level])
    elif visible == True and stack[level] == True:
        stack.append(True)
    else:
        stack.append(False)
    endswith.append(endstr)
    level += 1

def pop():
    global level
    global endswith

    if level > 0:
        v = stack.pop()
        e = endswith.pop()
        level -= 1
    return [v, e]

def cur():
    global level
    return stack[level]
