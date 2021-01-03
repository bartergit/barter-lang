from valid import is_func, is_dec, is_open_bracket, is_closed_bracket


def create_dec(tokens):
    return {"name": tokens[1], "type": tokens[0], "expr": tokens[3:]}


def create_params(tokens):
    params = []
    for x in range(0, len(tokens), 3):
        params.append({"type": tokens[x], "name": tokens[x + 1]})
    return params


def create_func(tokens):
    return {"name": tokens[1], "return_type": tokens[-1], "params": create_params(tokens[3:-2]), "body": []}


def do_nothing(x):
    return x


corresponding = {is_func: create_func, is_dec: create_dec}
expr_order_valid = {is_func: [is_open_bracket], is_open_bracket: [is_closed_bracket, is_dec],
                    is_dec: [is_closed_bracket, is_dec], is_closed_bracket: [is_func, "END"]}


# func = func name (type name,) type
# func  -> {
# {     -> } | dec
# dec   -> } | dec
# }     -> func | end


def parse(program_text):
    lines = program_text.split("\n")
    expected = [is_func]
    out = []
    for ind, line in enumerate(lines):
        is_valid = False
        if line.strip() == "":
            continue
        for curr in expected:
            if curr(line.split()):
                try:
                    out.append(corresponding.get(curr, do_nothing)(line.split()))
                except TypeError:
                    raise Exception(f"not valid in line {ind}\nline is {line}")
                expected = expr_order_valid[curr]
                is_valid = True
                break
        if not is_valid:
            raise Exception(
                f"not valid in line {ind}\nline is {line}\nexpected one of this: {[x.__name__ for x in expected]}")
    if "END" not in expected:
        raise Exception("Unexpected EOF")
    return combine(out)


def combine(to_combine):
    out = []
    flag = True
    for x in to_combine:
        if x == ["}"]:
            flag = True
            continue
        if x == ["{"]:
            flag = False
            continue
        if flag:
            out.append(x)
        else:
            out[-1]["body"].append(x)
    return out
