from anytree import Node, RenderTree
from collections import namedtuple

bin_op = namedtuple('bin_op', 'sign')
unary_op = namedtuple('unary_op', 'sign')
operators = ["<=", ">=", "+", "-", "*", "/", "==", "!=", "<", ">", "!"]

def print_tree(t):
    for pre, fill, node in RenderTree(t):
        print("%s%s" % (pre, node.name))


def parse_unary(expr_list, ops):
    out = []
    i = -1
    for ind, sym in enumerate(expr_list):
        if ind == i:
            continue
        if type(sym) == str and sym in ops and (len(out) == 0 or (type(out[-1]) == str and out[-1] in operators)):
            node = Node(unary_op(sym))
            if not isinstance(expr_list[ind + 1], Node):
                Node(expr_list[ind + 1], parent=node)
            else:
                expr_list[ind + 1].parent = node
            i = ind + 1
            out.append(node)
        else:
            out.append(sym)
    return out


def parse_binary(expr_list, operators):
    out = []
    i = -1
    for ind, sym in enumerate(expr_list):
        if ind == i:
            continue
        if type(sym) == str and sym in operators:
            node = Node(bin_op(sym))
            if not isinstance(out[-1], Node):
                Node(out.pop(), parent=node)
            else:
                out.pop().parent = node
            if not isinstance(expr_list[ind + 1], Node):
                Node(expr_list[ind + 1], parent=node)
            else:
                expr_list[ind + 1].parent = node
            i = ind + 1
            out.append(node)
        else:
            out.append(sym)
    return out


def parse_brackets(expr_list):
    out = []
    bracket_control = None
    for i, sym in enumerate(expr_list):
        if sym == "(":
            if bracket_control:
                bracket_control += 1
            else:
                bracket_control = 1
                j = i + 1
        elif sym == ")":
            bracket_control -= 1
        if bracket_control is None:
            out.append(sym)
        if bracket_control == 0:
            bracket_control = None
            out.append(recursive_parse_expr(expr_list[j:i]))
    return out


def recursive_parse_expr(expr_list):
    expr_list = parse_brackets(expr_list)
    expr_list = parse_unary(expr_list, "+-")
    for ops in ["*/", "+-", ["<=", ">=", "<", ">", "=="]]:
        expr_list = parse_binary(expr_list, ops)
    return expr_list[0]

def parse_expr(expr):
    for op in operators + ["(", ")"]:
        expr = expr.replace(op, f" {op} ")
    for op in ["< =", "> =", "! ="]:
        expr = expr.replace(op, op[0] + op[-1])
    expr_list = expr.split()
    return recursive_parse_expr(expr_list)

def evaluate(tree):
    if type(tree.name) == bin_op:
        return f"({evaluate(tree.children[0])}) {tree.name.sign} ({evaluate(tree.children[1])})"
    if type(tree.name) == unary_op:
        return f"{tree.name.sign}({evaluate(tree.children[0])})"
    return tree.name

if __name__ == "__main__":
    # expr = "15--12+98/3*780<=32"
    expr = "3*-(5-2/(12+1))/(2+1)"
    # expr = "-3*-3"
    tree = parse_expr(expr)
    print_tree(tree)
    evaluated = evaluate(tree)
    print(evaluated)

