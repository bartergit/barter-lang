import yaml
from src.help import load_from_yaml, minimal_but_not_negative, find

types = ["int", "str", "bool"]
special = ["for", "void", "while", "true", "false"]


def define_type(line):
    split_line = line.split()
    if len(split_line) == 1 and split_line[0] == "}":
        return "CLOSED_BRACKET"
    if len(split_line) < 2:
        return "EXPRESSION"
    if split_line[0] == "return":
        return "RETURN"
    if split_line[0] in types:
        return "DECLARATION"
    if split_line[1] == "=":
        return "ASSIGMENT"
    if split_line[0] == "if":
        return "IF"
    return "EXPRESSION"


def create_function(line):
    function = {"name": "", "return_type": "", "args": [], "body": []}
    i1, i2 = line.index("("), line.index(")")
    func, function["name"] = line[:i1].split()
    assert func == "func"
    empty, non_empty = line[i2 + 1:-1].split("->")
    function["return_type"] = non_empty.strip()
    assert function["return_type"] in types or function["return_type"] == "void"
    assert empty.strip() == ""
    args = line[i1 + 1:i2].split(",")
    if args != [""]:
        for arg in args:
            arg = arg.split()
            assert len(arg) == 2
            assert arg[0] in types
            function["args"].append({"type": arg[0], "name": arg[1]})
    return function


def create_declaration(line, variables, functions):
    declaration = {"TAG": "DECLARATION"}
    before, declaration["expr"] = line.split("=")
    declaration["type"], declaration["name"] = before.split()
    declaration["expr"] = create_expr(declaration["expr"], variables, functions)
    if declaration["type"] != declaration["expr"]["type"]:
        raise Exception(f'{declaration["type"]} != {declaration["expr"]["type"]}')
    variables[declaration["name"]] = {"name": declaration["name"], "type": declaration["type"]}
    return declaration


def create_assigment(line, variables, functions):
    assigment = {"TAG": "ASSIGMENT"}
    assigment["name"], assigment["expr"] = line.split("=")
    assigment["expr"] = create_expr(assigment["expr"], variables, functions)
    return assigment


def create_return(line, variables, functions):
    # check type
    return {"TAG": "RETURN", "expr": create_expr(line[len("return"):], variables, functions)}


def create_func_call(line, variables, functions):
    func_name, sec = line[:line.index("(")], line[line.index("(") + 1:]
    assert sec[-1] == ")", line
    function = functions.get(func_name.strip(), None)
    if function is None:
        raise Exception("this function does not exist", func_name)
    function_call = {"TAG": "FUNCTION_CALL", "function_name": function["name"], "args": []}
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
    expected_args = function["args"]
    for ind, arg in enumerate(args):
        arg = create_expr(arg, variables, functions)
        if arg["type"] != expected_args[ind]["type"]:
            raise Exception(f"unexpected argument of type {arg}. expected {expected_args[ind]['type']}")
        function_call["args"].append(arg)
    return function_call


def create_value(text, variables, functions):
    # text = text.strip()
    if text.isnumeric():
        return {"TAG": "VALUE", "expr": text, "type": "int"}
    if text[0] == "'" and text[-1] == "'":
        return {"TAG": "VALUE", "expr": text, "type": "str"}
    if text == "true" or text == "false":
        return {"TAG": "VALUE", "expr": text, "type": "bool"}
    raise Exception("non existed value", text, variables, text in variables)


def create_expr(line, variables, functions):
    line = line.strip()
    if "(" in line:
        expr = create_func_call(line, variables, functions)
        type = functions[expr["function_name"]]["return_type"]
    elif line in variables:
        expr = variables.get(line)
        expr["TAG"] = "VARIABLE"
        type = expr["type"]
    else:
        expr = create_value(line, variables, functions)
        type = expr["type"]
    return {"TAG": "EXPRESSION", "value": expr, "type": type}

def create_if(line, variables, functions):
    line = line.strip()
    assert line[:2] == "if", line[:2]
    assert line[-1] == "{"
    expr = create_expr(line[2:-1], variables, functions)
    assert expr["type"] == "bool"
    return {"TAG": "IF", "expr": expr, "if_true": []}

create_of_type = {"RETURN": create_return, "DECLARATION": create_declaration, "ASSIGMENT": create_assigment,
                  "EXPRESSION": create_expr, "IF": create_if}


def create_program(program, variables, functions):
    bracket_control = None
    new_function_flag = True
    current_function = None
    for line in program.split("\n"):
        line = line.split("//")[0]
        line = line.strip()
        if line == "":
            continue
        if new_function_flag:
            current_function = create_function(line)
            functions[current_function["name"]] = current_function
            bracket_control = 1
            new_function_flag = False
        else:
            if line[-1] == "{":
                bracket_control += 1
            if line == "}":
                bracket_control -= 1
            if bracket_control == 0:
                new_function_flag = True
            else:
                current_function["body"].append(line)
    for name in functions:
        function = functions[name]
        for arg in function["args"]:
            variables[arg["name"]] = arg
        # if name == "return_self":
        #     print(variables)
        if_expr = []
        j = 0
        while j < len(function["body"]):
            line = function["body"][j]
            if define_type(line) == "CLOSED_BRACKET":
                if_expr.pop()
                function["body"].pop(j)
                continue
            if if_expr:
                if_expr[-1]["if_true"].append(create_of_type[define_type(line)](line, variables, functions))
                function["body"].pop(j)
                j-=1
            else:
                function["body"][j] = create_of_type[define_type(line)](line, variables, functions)
                if define_type(line) == "IF":
                    if_expr.append(function["body"][j])
                    # del function["body"][j]
            j += 1
    return functions


if __name__ == '__main__':
    pass
    # for x in functions:
    #     print(yaml.dump(functions[x], ))
