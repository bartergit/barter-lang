import yaml

types = ["int", "str", "bool"]
special = ["for", "void", "while", "true", "false"]
vars = {}
functions = {}

def define_type(line):
    split_line = line.split()
    if len(split_line) < 2:
        return "EXPRESSION"
    if split_line[0] == "return":
        return "RETURN"
    if split_line[0] in types:
        return "DECLARATION"
    if split_line[1]:
        return "ASSIGMENT"
    return "EXPRESSION"


def create_function(line):
    function = {"args": [], "body": []}
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


def create_declaration(line):
    declaration = {"TAG": "DECLARATION"}
    before, declaration["expr"] = line.split("=")
    declaration["type"], declaration["name"] = before.split()
    declaration["expr"] = create_expr(declaration["expr"])
    if declaration["type"] != declaration["expr"]["type"]:
        raise Exception(f'{declaration["type"]} != {declaration["expr"]["type"]}')
    vars[declaration["name"]] = {"name": declaration["name"], "type": declaration["type"]}
    return declaration


def create_assigment(line):
    assigment = {"TAG": "ASSIGMENT"}
    assigment["name"], assigment["expr"] = line.split("=")
    assigment["expr"] = create_expr(assigment["expr"])
    return assigment


def create_return(line):
    # check type
    return {"TAG": "RETURN", "expr": create_expr(line[len("return"):])}


def create_func_call(line):
    func_name, sec = line[:line.index("(")], line[line.index("(") + 1:]
    assert sec[-1] == ")"
    function_call = {"TAG": "FUNCTION_CALL", "function": functions.get(func_name), "args": []}
    args = sec[:-1].split(",")
    expected_args = function_call["function"]["args"]
    if args != [""]:
        for ind, arg in enumerate(args):
            arg = create_expr(arg)
            if arg["type"] != expected_args[ind]["type"]:
                raise Exception(f"unexpected argument of type {arg}. expected {expected_args[ind]['type']}")
            function_call["args"].append(arg)
    return function_call


def create_value(text):
    text = text.strip()
    if text.isnumeric():
        return {"TAG": "VALUE", "expr": text, "type": "int"}
    if text[0] == "'" and text[-1] == "'":
        return {"TAG": "VALUE", "expr": text, "type": "str"}
    if text == "true" or text == "false":
        return {"TAG": "VALUE", "expr": text, "type": "bool"}
    raise Exception("nonexisting value", text)


def create_expr(line):
    if "(" in line:
        expr = create_func_call(line)
        type = expr["function"]["return_type"]
    elif line in vars:
        expr = vars.get(line)
        type = expr["type"]
    else:
        expr = create_value(line)
        type = expr["type"]
    return {"TAG": "EXPRESSION", "value": expr, "type": type}


create_of_type = {"RETURN": create_return, "DECLARATION": create_declaration, "ASSIGMENT": create_assigment,
                  "EXPRESSION": create_expr}


def create_program(program):
    bracket_control = None
    new_function_flag = True
    current_function = None
    for line in program.split("\n"):
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
        for j, line in enumerate(function["body"]):
            function["body"][j] = create_of_type[define_type(line)](line)
    return functions


if __name__ == '__main__':
    create_program("""
    func print(int a) -> void{
    }
    func print(str a) -> void{
    }
    func print(bool a) -> void{
    }
    func add(int a, int b) -> int{
    }
    func sub(int a, int b) -> int{
    }
    func mult(int a, int b) -> int{
    }
    func div(int a, int b) -> int{
    }
    func concat(str a, str b) -> str{
    }
    func lt(int a, int b) -> bool{
    }
    func gt(int a, int b) -> bool{
    }
    func eq(int a, int b) -> bool{
    }
    func and(bool a, bool b) -> bool{
    }
    func or(bool a, bool b) -> bool{
    }
    func main()->void{
        str a = 'something'
    }
    """)
    yaml.Dumper.ignore_aliases = lambda *args: True
    for x in functions:
        print(yaml.dump(functions[x], sort_keys=False))