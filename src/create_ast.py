from anytree import Node, RenderTree
from collections import namedtuple

variable = namedtuple('variable', 'name')
compare = namedtuple('compare', 'operator')
bin_op = namedtuple('bin_op', 'operator')
constant = namedtuple('constant', 'value')
assign = namedtuple('assign', 'name')
declare = namedtuple('declare', 'type name')

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
special = ["while", "for", "true", "false", "if"]
stack = []

def is_correct_var_name(string):
    return ["A" <= x <= "x" or x == "_" or x.isnumeric() for x in string[1:]].count(True) == len(string) - 1 \
        and ("A" <= string[0] <= "x" or string[0] == "_") and string not in special

def parse_value(string, parent):
    if string.isnumeric() or string in ["true", "false"]:
        return Node(constant(string), parent = parent)
    if is_correct_var_name(string):
        return Node(variable(string), parent = parent)
    raise Exception(f"syntax error in {string}")


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


def parse_while(string):
    string = string.strip()
    assert string[:len("while")] == "while"
    assert line[-1] == "{" 
    statement = line[len("while"):-1].strip()
    while_statement = Node("while", parent=stack[-1])
    while_body = Node("while_body", parent=stack[-1])
    stack.append(while_body)
    parse_expr(statement, while_statement)
    

def parse_if(string):
    string = string.strip()
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
    first, expr = split(string, "=")
    typeof, var_name = split(first, " ")
    assert is_correct_var_name(var_name), f"variable name '{var_name}' is not correct"
    declare_node = Node(declare(typeof, var_name), parent=stack[-1])
    parse_expr(expr, declare_node)

if __name__ == "__main__":
    program = Node("program")
    stack.append(program)
    for line in split(listing, "\n"):
        line = line.strip()
        if line == "":
            continue
        if "while" in line:
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
            pass
        elif line[:4] == "int "  or line[:5] == "bool ":
            parse_declaration(line)
        else:
            parse_assign(line)
    for pre, fill, node in RenderTree(program):
        print("%s%s" % (pre, node.name))


            


