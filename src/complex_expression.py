from anytree import Node, RenderTree
from collections import namedtuple

bin_op = namedtuple('bin_op', 'sign')
unary_op = namedtuple('unary_op', 'sign')
operators = ["<=", ">=", "+", "-", "*", "/", "==", "!=", "<", ">", "!"]


def do(expr):
    array = []
    numbers_1 = {}
    numbers_2 = {}
    for operator in operators:
        i = -1
        while True:
            i = expr.find(operator, i + 1)
            if i != -1:
                array.append((operator, i))
            else:
                break
    array.sort(key=lambda x: x[1])
    j = 0
    for op, i in array:
        number = expr[j:i]
        if number != '':
            numbers_1[j] = number
            numbers_2[i] = number
        else:
            pass
        j = i + 1
    # numbers.append((expr[j:], j, len(expr)))
    print(expr)
    print(array)
    # print(numbers)
    # print(numbers[4][0], expr[numbers[4][1]:numbers[4][2]])
    print(numbers_1)
    print(numbers_2)
    print(array[1][0])
    print(numbers_2[array[1][1]])
    print(numbers_1[array[1][1] + len(array[1][0])])
    # index = 1
    # print(numbers[index], array[index][0], numbers[index + 1])


def find(expr, ind):
    i = expr.find("(", ind)
    j = expr.find(")", ind)
    if i < 0 or j < 0:
        return max(i, j)
    else:
        return min(i, j)


def find_brackets(expr):
    ind = find(expr, 0)
    start = ind
    assert expr[ind] == "("
    bracket_control = 1
    while True:
        ind = find(expr, ind + 1)
        if ind == -1:
            break
        bracket = expr[ind]
        if bracket == "(":
            bracket_control += 1
        elif bracket == ")":
            bracket_control -= 1
        if bracket_control == 0:
            break
    print(expr[start + 1:ind])
    return ind


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

if __name__ == "__main__":
    # expr = "15--12+98/3*780<=32"
    expr = "3*-(5-2)/(2+1)"
    print_tree(parse_expr(expr))

