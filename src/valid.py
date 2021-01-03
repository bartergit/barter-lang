from CONST import types, special, operations
from util import find, rfind

def is_name(token):
    return type(token) == str and token[
        0].isalpha() and token not in types and token not in special and False not in map(
        lambda x: 'A' <= x <= 'z' or x == '_' or x.isdigit(),
        token)


def is_type(token):
    return token in types


def is_int(text):
    return text.isnumeric()


def is_str(text):
    return text[0] == "'" and text[-1] == "'"


def is_bool(text):
    return text == "true" or text == "false"


def is_int_expr(tokens):
    f = True
    if tokens[0] in operations:
        cond = lambda x: x % 2 != 0
    else:
        cond = lambda x: x % 2 == 0
    i1, i2 = find(tokens, "("), rfind(tokens, ")")
    if i1 == -1 and i2 == -1:
        for ind, token in enumerate(tokens):
            f = f and (is_name(token) or is_int(token) if cond(ind) else token in operations)
    elif i1 != -1 and i2 != -1:
        for ind in range(0, i1 - 1):
            token = tokens[ind]
            f = f and (is_name(token) or is_int(token) if cond(ind) else token in operations)
        f = f and tokens[i1 - 1] in operations
        cond = lambda x: x % 2 == 0 if i2 % 2 == 0 else lambda x: x % 2 != 0
        for ind in range(i2 + 1, len(tokens)):
            token = tokens[ind]
            f = f and (is_name(token) or is_int(token) if cond(ind) else token in operations)
        f = f and is_int_expr(tokens[i1 + 1:i2])
    else:
        raise Exception("( and ) mismatch")
    return f


def is_str_expr(tokens):
    return len(tokens) == 1 and is_str(tokens[0])


def is_bool_expr(tokens):
    return len(tokens) == 1 and is_bool(tokens[0])


def is_func(tokens):
    if len(tokens) < 5:
        return False
    if len(tokens) == 5:
        return tokens[0] == "func" and is_name(tokens[1]) and tokens[2] == "(" and tokens[3] == ")" and (
                is_type(tokens[4]) or tokens[4] == "void")
    f = tokens[0] == "func" and is_name(tokens[1]) and tokens[2] == "(" and (
            is_type(tokens[-1]) or tokens[-1] == "void")
    for x in range(0, len(tokens) - 4, 3):
        if x >= len(tokens) - 4 - 3:
            f = f and is_type(tokens[3 + x]) and is_name(tokens[3 + x + 1]) and tokens[3 + x + 2] == ")"
        else:
            f = f and is_type(tokens[3 + x]) and is_name(tokens[3 + x + 1]) and tokens[3 + x + 2] == ","
    return f


def is_dec(tokens):
    if len(tokens) < 4:
        return False
    f = is_type(tokens[0]) and is_name(tokens[1]) and tokens[2] == "="
    if tokens[0] == "int":
        return f and is_int_expr(tokens[3:])
    if tokens[0] == "str":
        return f and is_str_expr(tokens[3:])
    if tokens[0] == "bool":
        return f and is_bool_expr(tokens[3:])


def is_open_bracket(tokens):
    return len(tokens) == 1 and tokens[0] == "{"


def is_closed_bracket(tokens):
    return len(tokens) == 1 and tokens[0] == "}"

