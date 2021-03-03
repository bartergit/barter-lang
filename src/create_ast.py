from anytree import Node, RenderTree
from collections import namedtuple

variable = namedtuple('variable', 'name')
compare = namedtuple('compare', 'operator')
bin_op = namedtuple('bin_op', 'operator')
constant = namedtuple('constant', 'value')
assign = namedtuple('assign', 'name')
declare = namedtuple('declare', 'type name')
function_call = namedtuple('function_call', 'name')
declare_func = namedtuple('declare_func', 'name type')
# argument = namedtuple('argument', 'type name')

def split(string, delimiter=None):
    if delimiter is None:
        return [x.strip() for x in string.split()]
    else:
        return [x.strip() for x in string.split(delimiter)]

listing = """while b != 0 {
    if a > b {
        int a = a - b
    } else {
        int b = b - a
        int c = b + a
        int f = true
    }
}
return a"""

operators = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]
types = ["int", "bool"]
special = ["while", "for", "true", "false", "if", "func"] + types
stack = []

def is_correct_var_name(string):
    return ["A" <= x <= "z" or x == "_" or x.isnumeric() for x in string[1:]].count(True) == len(string) - 1 \
        and ("A" <= string[0] <= "z" or string[0] == "_") and string not in special

def parse_value(string, parent):
    if string.isnumeric() or string in ["true", "false"]:
        return Node(constant(string), parent = parent)
    if is_correct_var_name(string):
        return Node(variable(string), parent = parent)
    if "(" in string and ")" in string:
        func_name, args = split(string, "(")
        assert args[-1] == ")", string
        args = split(args[:-1], ",")
        func_call = Node(function_call(func_name), parent = parent)
        if args != [""]:
            for arg in args:
                parse_value(arg, func_call)
        return func_call
    raise Exception(f"syntax error in {string}", is_correct_var_name(string))


def parse_expr(statement, parent):
    for operator in operators:
        if operator in statement:
            arg1, arg2 = split(statement, operator)
            operator_node = Node(bin_op(operator), parent=parent)
            parse_value(arg1, operator_node)       
            parse_value(arg2, operator_node)
            return
    parse_value(statement.strip(),parent)
    # raise Exception("syntax error", statement, operators, "-" in statement)


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
    arg_list = []
    if arguments != [""]:
        for arg in arguments:
            typeof, arg_name = split(arg, " ")
            assert typeof in types, typeof
            Node(declare(typeof, arg_name), parent=args_node)
    stack.append(Node("func_body", parent=func_node))
    # functions[function_name] = {"arguments": arg_list, "return_type": return_type, "body":[]}
    # return functions[function_name]


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
        first, expr = split(string, "=")
        typeof, var_name = split(first, " ")
        assert is_correct_var_name(var_name), f"variable name '{var_name}' is not correct"
        declare_node = Node(declare(typeof, var_name), parent=stack[-1])
        parse_expr(expr, declare_node)
    else:
        typeof, var_name = split(string, " ")
        assert is_correct_var_name(var_name), f"variable name '{var_name}' is not correct"
        declare_node = Node(declare(typeof, var_name), parent=stack[-1])

def create_ast(listing):
    program = Node("program")
    stack.append(program)
    for line in split(listing, "\n"):
        if "//" in line:
            line, _ = split(line, "//")
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
            s1,s2 = split(line, "else")
            assert s1 == "}" and s2 == "{"
            stack[-1] = Node("else_body", parent = stack[-1].parent)
        elif "return" in line:
            ret, expr = split(line, " ")
            assert ret == "return"
            ret_node = Node("return", parent = stack[-1])
            parse_expr(expr, ret_node)
        elif line[:4] == "int "  or line[:5] == "bool ":
            parse_declaration(line)
        else:
            slitted = split(line, "=")
            if is_correct_var_name(slitted[0]):
                parse_assign(line)
            else:
                parse_value(line, stack[-1])
    return program

if __name__ == "__main__": 
    pass  
    # for pre, fill, node in RenderTree(program):
    #     print("%s%s" % (pre, node.name))


            


