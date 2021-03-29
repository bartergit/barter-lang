from util import *

from complex_expression import parse_expr as parse_complex_expr

stack = []

def parse_expr(statement, parent):
    node = parse_complex_expr(statement)
    node.parent = parent


def parse_func(string):
    function_decl, arguments = split(string, "(")
    func, function_name = split(function_decl, " ")
    assert func == "func"
    assert is_correct_var_name(function_name)
    arguments, return_type = split(arguments, ")")
    assert return_type[-1] == "{"
    return_type = return_type[:-1].strip()
    assert return_type in types or return_type == "void"
    func_node = Node(declare_func(function_name, return_type), parent=stack[-1])
    args_node = Node("arguments", parent=func_node)
    arguments = split(arguments, ",")
    if arguments != [""]:
        for arg in arguments:
            typeof, arg_name = split(arg, " ")
            assert typeof in types, typeof
            Node(var_declare(typeof, arg_name), parent=args_node)
    stack.append(Node("func_body", parent=func_node))


def parse_while(string):
    assert string[:len("while")] == "while"
    assert string[-1] == "{"
    statement = string[len("while"):-1].strip()
    while_statement = Node("while", parent=stack[-1])
    parse_expr(statement, while_statement)
    while_body = Node("while_body", parent=while_statement)
    stack.append(while_body)


def parse_if(string):
    assert string[:len("if")] == "if"
    assert string[-1] == "{"
    statement = string[len("if"):-1].strip()
    if_statement = Node("if", parent=stack[-1])
    parse_expr(statement, if_statement)
    if_body = Node("if_body", parent=if_statement)
    stack.append(if_body)


def parse_assign(string):
    var_name, expr = split(string, "=")
    assert is_correct_var_name(var_name), f"variable name '{var_name}' is not correct"
    assign_node = Node(assign(var_name), parent=stack[-1])
    parse_expr(expr, assign_node)


def parse_declaration(string):
    if "=" in string:
        ind = string.find("=")
        first, expr = string[:ind].strip(), string[ind + 1:].strip()
        # split(string, "=")
        typeof, var_name = split(first, " ")
        assert is_correct_var_name(var_name), f"variable name '{var_name}' is not correct"
        declare_node = Node(var_declare(typeof, var_name), parent=stack[-1])
        parse_expr(expr, declare_node)
    else:
        typeof, var_name = split(string, " ")
        assert is_correct_var_name(var_name), f"variable name '{var_name}' is not correct"
        Node(var_declare(typeof, var_name), parent=stack[-1])


def create_ast(listing):
    program = Node("program")
    stack.append(program)
    for line in split(listing, "\n"):
        if "//" in line:
            splited_line = split(line, "//")
            if len(splited_line) > 1:
                line = splited_line[0]
            else:
                continue
        else:
            line = line.strip()
        if line == "":
            continue
        elif "func" in line:
            parse_func(line)
        elif "while" in line:
            parse_while(line)
        elif "if" in line:
            parse_if(line)
        elif line == "}":
            stack.pop()
        elif "else" in line:
            s1, s2 = split(line, "else")
            assert s1 == "}" and s2 == "{"
            stack[-1] = Node("else_body", parent=stack[-1].parent)
        elif line.startswith("return"):
            if line == "return":
                Node("return", parent=stack[-1])
            else:
                index = line.find(" ")
                ret, expr = line[:index].strip(), line[index+1:].strip()
                assert ret == "return"
                ret_node = Node("return", parent=stack[-1])
                parse_expr(expr, ret_node)
        elif line[:4] == "int " or line[:5] == "bool ":
            parse_declaration(line)
        else:
            slitted = split(line, "=")
            if is_correct_var_name(slitted[0]):
                parse_assign(line)
            else:
                parse_expr(line,stack[-1])
    # except Exception as e:
    #     print(e)
    #     print(line)
    return program


if __name__ == "__main__":
    with open(f"test/functionality.barter", "r") as f:
        parent = Node("parent")
        for line in f.read().split(";"):
            program = parse_expr(line, parent)
        # print(parent)
        for pre, fill, node in RenderTree(parent):
            print("%s%s" % (pre, node.name))
