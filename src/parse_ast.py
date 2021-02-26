from anytree import Node, RenderTree
from collections import namedtuple

variable = namedtuple('variable', 'name')
compare = namedtuple('compare', 'operator')
bin_op = namedtuple('bin_op', 'operator')
constant = namedtuple('constant', 'value')
assign = namedtuple('assign', 'name')
# while b != 0 {
#     if a > b {
#         int a = a − b
#     } else {
#         int b = b − a
#     }
# }
# return a
variables = {"a": "int", "b": "int", "flag": "bool", "c": "bool"}
builtin_functions = ["print"]
functions = ["sum"]
operators = {"-": ["int", "int", "int"], "<": ["int", "int", "bool"], ">": ["int", "int", "bool"], 
"!=": ["int", "int", "bool"]}

def f(node):
    if type(node.name) == assign:
        var_name = node.name.name
        assert len(node.children) == 1
        expr = f(node.children[0])
        assert expr[1] == variables[var_name], f"expected type {variables[var_name]} got {expr[1]}"
        return "%s = %s;\n" % (var_name, expr[0])
    # if type(node.name) == d
    if type(node.name) == bin_op:
        first = f(node.children[0])
        sec = f(node.children[1])
        exp_1, exp_2, return_type = operators[node.name.operator]
        assert exp_1 == first[1] and exp_2 == sec[1], f"exprected types {exp_1} {exp_2}, got {first[1]} {sec[1]}"
        return "%s %s %s" % (first[0], node.name.operator, sec[0]), return_type
    if type(node.name) == constant:
        if node.name.value in ["true", "false"]:
            return node.name.value, "bool"
        return node.name.value, "int"
    if type(node.name) == variable:
        var_name = node.name.name
        assert var_name in variables, f"no such variable: {var_name}" 
        return var_name, variables[var_name]
    # if type(node.name) == bin_op:
    #     first = f(node.children[0])
    #     sec = f(node.children[1])
    #     if first[1] != sec[1]:
    #         raise Exception(f"{first[1]} != {sec[1]}")
    #     return "%s %s %s" % (, node.name.operator, f(node.children[1]))
    if node.name == "while":
        assert len(node.children) == 2
        compare = f(node.children[0])
        assert compare[1] == "bool", "expected bool expression in while"
        return "while (%s) {\n%s}\n" % (compare[0], f(node.children[1]))
    if node.name == "if":
        compare = f(node.children[0])
        assert compare[1] == "bool", "expected bool expression in if"
        assert node.children[1].name == "if_body"
        assert (len(node.children) == 3 and node.children[2].name == "else_body") or len(node.children) == 3
        return "if (%s) {\n%s} else {\n%s}\n" % (compare[0], f(node.children[1]), f(node.children[2]))
    if "body" in node.name:
        out = ""
        for child in node.children:
            out += f(child)
        return out
    print(node)


if __name__ == '__main__':
    program = Node("program")
    whil = Node("while", parent=program)
    ret = Node("ret", parent=program)
    # cond = Node("cond", parent=whil)
    comp = Node(bin_op("!="), parent=whil)
    body = Node("body", parent=whil)
    ret_a = Node(variable('a'), parent=ret)
    v1 = Node(variable("b"), parent=comp)
    v2 = Node(constant(0), parent=comp)
    branch = Node("if", parent=body)
    # branch_condition = Node("condition", parent=branch)
    op = Node(bin_op(">"), parent=branch)
    if_body = Node("if_body", parent=branch)
    else_body = Node("else_body", parent=branch)
    c1 = Node(variable("a"), parent=op)
    c2 = Node(variable("b"), parent=op)
    ass = Node(assign("a"), parent=if_body)
    bin1 = Node(bin_op("-"), parent=ass)
    v3 = Node(variable("a"), parent=bin1)
    v4 = Node(variable("b"), parent=bin1)
    ass = Node(assign("b"), parent=else_body)
    bin2 = Node(bin_op("-"), parent=ass)
    v3 = Node(variable("b"), parent=bin2)
    v4 = Node(variable("a"), parent=bin2)
    for pre, fill, node in RenderTree(program):
        print("%s%s" % (pre, node.name))
    # for pre, fill, node in RenderTree(comp):
    #     print("%s%s" % (pre, node.name))
    # print(f(comp))
    # print(f(ass))
    print(f(whil))




