import yaml
from src.parse_program import create_program
from help import print_as_yaml, load_from_yaml

def log(data, filename="out/log.txt"):
    with open(filename, "a") as file:
        file.write(data)
        file.write("\n")

built_in = {'log': log,
            'print': print,
            'add': lambda x, y: x + y,
            'sub': lambda x, y: x - y,
            'mult': lambda x, y: x * y,
            'div': lambda x, y: x // y,
            'concat': lambda x, y: x + y,
            'lt': lambda x, y: x < y,
            'gt': lambda x, y: x > y,
            'eq': lambda x, y: x == y,
            'and': lambda x, y: x == "true" and y == "true",
            'or': lambda x, y: x == "true" or y == "true",
            'to_str': lambda x: str(x),
            'not': lambda x: x != "true"}


def execute_expression(expr, functions, variables):
    expr_val = expr["value"]
    if expr_val["TAG"] == "VARIABLE":
        return variables[expr_val["name"]]["value"]
    if expr_val["TAG"] == "VALUE":
        if expr_val["type"] == "int":
            return int(expr_val["expr"])
        if expr_val["type"] == "str":
            return expr_val["expr"][1:-1]
        if expr_val["type"] == "bool":
            return expr_val["expr"]
    if expr_val["TAG"] == "FUNCTION_CALL":
        function_name = expr_val["function_name"]
        if function_name in built_in:
            return built_in[function_name](
                *[execute_expression(expr, functions, variables) for expr in expr_val["args"]])
        else:
            return execute_function(functions.get(function_name), functions,
                                    args=[execute_expression(expr, functions, variables) for expr in expr_val["args"]])

def execute_body_part(line, functions, variables):
    if line["TAG"] == "DECLARATION":
        variables[line["name"]] = {"type": line["type"],
                                   "value": execute_expression(line["expr"], functions, variables)}
    if line["TAG"] == "EXPRESSION":
        execute_expression(line, functions, variables)
    if line["TAG"] == "IF":
        yes = execute_expression(line["expr"], functions, variables)
        if yes:
            for expr in line["if_true"]:
                to_return = execute_body_part(expr, functions, variables)
                if to_return is not None:
                    return to_return
    if line["TAG"] == "RETURN":
        return execute_expression(line["expr"], functions, variables)

def execute_function(function, functions, args):
    variables = {}
    for ind, arg in enumerate(args):
        name = function["args"][ind]["name"]
        type = function["args"][ind]["type"]
        variables[name] = {"name": name, "type": type, "value": arg}
    for line in function["body"]:
        to_return = execute_body_part(line, functions, variables)
        if to_return is not None:
            return to_return
    if function["name"] == "main":
        return variables


def execute(functions):
    main_function = functions.get("main")
    if main_function is None:
        raise Exception("no main function")
    return execute_function(main_function, functions, [])


if __name__ == '__main__':
    functions = load_from_yaml("main.yaml")
    execute(functions)
