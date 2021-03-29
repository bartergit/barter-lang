from anytree import Node
from util import *


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


def parse_comma_expr(expr_list, function_call_node):
    if not len(expr_list):
        return  # function_call_node
    j = 0
    expr_list.append(",")
    bracket_control = None
    for i, sym in enumerate(expr_list):
        if sym == "(":
            if bracket_control:
                bracket_control += 1
            else:
                bracket_control = 1
        elif sym == ")":
            bracket_control -= 1
        elif sym == "," and (bracket_control == 0 or bracket_control is None):
            recursive_parse_expr(expr_list[j:i]).parent = function_call_node
            j = i + 1


def parse_brackets(expr_list):
    out = []
    j = None
    bracket_control = None
    function_call_node = None
    for i, sym in enumerate(expr_list):
        if sym == "(":
            if len(out) and is_correct_var_name(out[-1]):
                function_call_node = Node(
                    function_call(out.pop()))  # check if previous one is variable, then parse function
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
            if function_call_node:
                out.append(function_call_node)
                parse_comma_expr(expr_list[j:i], function_call_node)
                function_call_node = None
            else:
                out.append(recursive_parse_expr(expr_list[j:i]))
    return out


def recursive_parse_expr(expr_list):
    if len(expr_list) == 1:
        return Node(parse_value(expr_list[0]))
    expr_list = parse_brackets(expr_list)
    expr_list = parse_unary(expr_list, "+-")
    for ops in ["*/", "+-", ["<=", ">=", "<", ">", "==", "!="]]:
        expr_list = parse_binary(expr_list, ops)
    return expr_list[0]


def finalize_parsing_expr(node):
    if type(node.name) == bin_op:
        finalize_parsing_expr(node.children[0])
        finalize_parsing_expr(node.children[1])
    elif type(node.name) == unary_op:
        finalize_parsing_expr(node.children[0])
    elif type(node.name) == function_call:
        for child in node.children:
            finalize_parsing_expr(child)
    elif type(node.name) in [variable, constant]:
        pass
    else:
        node.name = parse_value(node.name)


def parse_expr(expr):
    for op in operators + ["(", ")", ","]:
        expr = expr.replace(op, f" {op} ")
    for op in ["< =", "> =", "! ="]:
        expr = expr.replace(op, op[0] + op[-1])
    expr_list = expr.split()
    node = recursive_parse_expr(expr_list)
    finalize_parsing_expr(node)
    return node


def evaluate_to_register(tree, ind=0):
    if type(tree.name) == bin_op:
        first = tree.children[0]
        sec = tree.children[1]
        before = ""
        after = ""
        if type(first.name) in [bin_op, unary_op]:
            before += evaluate_to_register(first)
        else:
            after += f"R0 = {evaluate_to_register(first)};\n"
        if type(sec.name) in [bin_op, unary_op]:
            before += evaluate_to_register(sec, 1)
        else:
            after += f"R1 = {evaluate_to_register(sec)};\n"
        return before + after + f"R{ind} = R0 {tree.name.sign} R1;\n"
    if type(tree.name) == unary_op:
        first = tree.children[0]
        before = ""
        after = ""
        if type(first.name) in [bin_op, unary_op]:
            before += evaluate_to_register(first)
        else:
            after += f"R{ind} = {evaluate_to_register(first)};\n"
        return before + after + f"R{ind} = {tree.name.sign} R{ind};\n"
    if type(tree.name) == constant:
        return tree.name.value
    return tree.name.name


def evaluate_to_stack(tree):
    if type(tree.name) == bin_op:
        first = tree.children[0]
        sec = tree.children[1]
        before = ""
        after = ""
        if type(sec.name) in [bin_op, unary_op]:
            before += evaluate_to_stack(sec)
        else:
            after += f"stack.append({evaluate_to_stack(sec)});\n"
        if type(first.name) in [bin_op, unary_op]:
            before += evaluate_to_stack(first)
        else:
            after += f"stack.append({evaluate_to_stack(first)});\n"
        return before + after + f"stack.append(stack.pop() {tree.name.sign} stack.pop());\n"
    if type(tree.name) == unary_op:
        first = tree.children[0]
        before = ""
        after = ""
        if type(first.name) in [bin_op, unary_op]:
            before += evaluate_to_stack(first)
        else:
            after += f"stack.append({evaluate_to_stack(first)});\n"
        return before + after + f"stack.append({tree.name.sign}stack.pop());\n"
    if type(tree.name) == constant:
        return tree.name.value
    return tree.name.name


if __name__ == "__main__":
    expr = "36/(3+5*(2+1))"
    expr = "-3*-2"
    expr = "-(8*(3+5))+1/1"
    expr = "print(1+3+2, 5)"
    tree = parse_expr(expr)
    print_tree(tree)
    expr = "1+3+2"
    tree = parse_expr(expr)
    print_tree(tree)
    # print(out)
