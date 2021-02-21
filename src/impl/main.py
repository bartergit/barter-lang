def find(seq, el, start=0):
    try:
        return seq.index(el, start)
    except ValueError:
        return -1


def minimal_but_not_negative(*args):
    return min(filter(lambda x: x > 0, args))


def create_func_call(line, context):
    func_name, sec = line[:line.index("(")].strip(), line[line.index("(") + 1:]
    assert sec[-1] == ")", line
    args = []
    if sec.strip() != ")":
        brackets_control = 1
        i = 0
        temp = 0
        while brackets_control != 0:
            i1, i2, i3 = find(sec, ",", i), find(sec, "(", i), find(sec, ")", i)
            minimum = minimal_but_not_negative(i1, i2, i3)
            if minimum == i1 and brackets_control == 1:
                args.append(sec[temp:i1])
                temp = i1 + 1
            elif minimum == i2:
                brackets_control += 1
            elif minimum == i3:
                brackets_control -= 1
            i = minimum + 1
        assert i1 == -1 and i2 == -1 and find(sec, ")", i) == -1, f"() mismatch {sec}"
        args.append(sec[temp:-1])
    for function in context["functions"][func_name]:
        if function["arg_number"] == len(args):
            print(func_name, args)
            return
    raise Exception("wrong function signature", func_name)



def divide(program):
    lines = []
    start = 0
    while True:
        brackets_control = 1
        i = find(program, "(", start) + 1
        if i == 0:
            assert sum([len(x) for x in lines]) == len(program)
            return lines
        while brackets_control != 0:
            i1, i2 = find(program, "(", i), find(program, ")", i)
            minimum = minimal_but_not_negative(i1, i2)
            if minimum == i1:
                brackets_control += 1
            elif minimum == i2:
                brackets_control -= 1
            i = minimum + 1
        lines.append(program[start:i])
        start = i


if __name__ == '__main__':
    context = {"functions": {
        "print": [{"arg_number": 1}],
        "sum": [{"arg_number": 2}]}
    }
    lines = divide("print('Hello world') sum(1,3) log(sum(sub(3,2),mult(1,3)))")
    print(lines)
    for line in lines:
        create_func_call(line, context)
    # create_func_call("log(sum(sub(3,2),mult(1,3)))")
    # create_func_call("sum(sub(3,2),mult(1,3))")
    pass
