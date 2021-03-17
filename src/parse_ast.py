import sys
from collections import defaultdict, Counter
from create_ast import create_ast
from util import *
import os


def cout_int(args):
    out = "cout << "
    for arg in args:
        out += arg
        out += ' << " " << '
    out += "'\\n';\n"
    return out

def cout_bool(args):
    out = "cout << "
    for arg in args:
        out += '"true"' if arg == 1 else '"false"'
        out += ' << " " << '
    out += "'\\n';\n"
    return out


def log(args):
    out = 'myfile'
    for arg in args:
        out += " << "
        out += arg
        out += " << '\\n'"
    return out


builtin_functions = {
    "print": [signature("void", ["int"], cout_int, 0), signature("void", ["bool"], cout_bool, 0)],
    "log": [signature("void", ["int"], log, 0)]
}
functions = defaultdict(list)
operators = {"-": ["int", "int", "int"], "+": ["int", "int", "int"], "<": ["int", "int", "bool"],
             ">": ["int", "int", "bool"], "<=": ["int", "int", "bool"],
             "!=": ["int", "int", "bool"], "*": ["int", "int", "int"], "==": ["int", "int", "bool"],
             "/": ["int", "int", "int"]
             }
unary_operators = {"!": ["bool", "bool"], "-": ["int", "int"], "+": ["int", "int"]}
variables = {}
functions_index = Counter()
ind = 0
lbl_counter = 0
current_function_return_type = None
additional_index = None


def create_variable(node):
    var_name = node.name.name
    assert var_name in variables, f"no such variable: {var_name}"
    i = len(variables) - variables[var_name]["ind"]
    if additional_index:
        i += additional_index
    return expression(f"get(stack_pointer - {i})", variables[var_name]["type"])


def create_bin_op(node):
    first = parse_node(node.children[0])
    sec = parse_node(node.children[1])
    expected_first_type, expected_sec_type, return_type = operators[node.name.sign]
    assert expected_first_type == first.type and expected_sec_type == sec.type, \
        f"expected types {expected_first_type} {expected_sec_type}, got {first.type} {sec.type}"
    return expression(f"({first.value} {node.name.sign} {sec.value})", return_type)

def create_unary_op(node):
    first = parse_node(node.children[0])
    expected_first_type, return_type = unary_operators[node.name.sign]
    assert expected_first_type == first.type, \
        f"expected type {expected_first_type}, got {first.type}"
    return expression(f"{node.name.sign}({first.value})", return_type)


def create_constant(node):
    if node.name.value in ["true", "false"]:
        return expression(node.name.value, "bool")
    return expression(node.name.value, "int")


def create_function_call(node):
    global lbl_counter, additional_index
    func_name = node.name.name
    if func_name in functions:
        args = ""
        for function in functions[func_name]:
            return_type = function.return_type
            args_node = function.args
            if len(args_node) != len(node.children):
                continue
            signature_is_fine = True
            for i, child in enumerate(node.children):
                additional_index = i
                val, typeof = parse_node(child)
                if args_node[i] != typeof:
                    signature_is_fine = False
                    break
                args += f"push({val});\n"
            if not signature_is_fine:
                continue
            additional_index = None
            func_name += str(function.ind)
            lbl_counter += 1
            return expression(
                f"{args}stack_trace[++stack_trace_pointer] = &&${lbl_counter};\ngoto {func_name};\n${lbl_counter}:\n",
                return_type)
        raise Exception(f"no matching function for giving signature")
    elif func_name in builtin_functions:
        for function in builtin_functions[func_name]:
            return_type = function.return_type
            args_node = function.args
            if len(args_node) != len(node.children):
                continue
            args = []
            signature_is_fine = True
            for i, child in enumerate(node.children):
                val, typeof = parse_node(child)
                if args_node[i] != typeof:
                    signature_is_fine = False
                    break
                args.append(val)
            if not signature_is_fine:
                continue
            return expression(function.implementation(args), return_type)
    else:
        raise Exception("syntax error")


def create_variable_declaration(node):
    global ind
    var_name, typeof = node.name.name, node.name.type
    assert var_name not in variables, f"{var_name} already exists"
    if len(node.children):
        expr = parse_node(node.children[0])
        # assert type(expr) == expression, expr
        ind += 1
        variables[var_name] = {"type": typeof, "ind": ind}
        assert expr.type == \
               typeof, f"{node.name} {expr} {node.children[0].name}, expected type {typeof} got {expr.type}"
        if type(node.children[0].name) == function_call:
            return f"{expr[0]}" \
                   f"push(pop());\n"
        else:
            return f"push({expr[0]});\n"
    else:
        ind += 1
        variables[var_name] = {"type": typeof, "ind": ind}
        return "push(0);\n"


def create_assign(node):
    var_name = node.name.name
    expr = parse_node(node.children[0])
    assert expr[1] == variables[var_name]["type"], f"expected type {variables[var_name]['type']} got {expr[1]}"
    i = len(variables) - variables[var_name]["ind"]
    if type(node.children[0].name) == function_call:
        return f"{expr[0]}" \
               f"set(stack_pointer - {i}, pop());\n"
    return f"set(stack_pointer - {i}, {expr[0]});\n"


def create_function_declaration(node):
    global ind, variables
    ind = 0
    variables = {}
    args = ""
    function_name = node.name.name
    assert function_name in functions
    overloaded_name = function_name + str(functions_index[function_name])
    functions_index[function_name] += 1
    for child in node.children[0].children:
        args += parse_node(child)[:-2] + ";\n"
    return f"{overloaded_name}:\n" \
           f"{parse_node(node.children[1])}"


def create_while(node):
    global lbl_counter
    assert len(node.children) == 2, node.children
    compare = parse_node(node.children[0])
    assert compare.type == "bool", "expected bool expression in while"
    lbl_counter += 1
    if_label_counter = lbl_counter
    return "$%s:\nif (%s) {\n%sgoto $%s;\n}\n" % (
        if_label_counter, compare.value, parse_node(node.children[1]), if_label_counter)


def create_if(node):
    compare = parse_node(node.children[0])
    assert compare[1] == "bool", "expected bool expression in if"
    assert node.children[1].name == "if_body"
    if len(node.children) == 3:
        return "if (%s) {\n%s} else {\n%s}\n" % (compare[0], parse_node(node.children[1]), parse_node(node.children[2]))
    elif len(node.children) == 2:
        return "if (%s) {\n%s}\n" % (compare[0], parse_node(node.children[1]))


def create_body(node):
    out = ""
    for child in node.children:
        line = parse_node(child)
        if type(line) == expression:
            out += line.value + ";\n"
        else:
            out += line
    return out


def create_return(node):
    if current_function_return_type == "void":
        assert len(node.children) == 0
        return f"stack_pointer-={len(variables)};\n" \
               f"goto *stack_trace[stack_trace_pointer--];\n"
    else:
        returned = parse_node(node.children[0])
        assert returned[1] == current_function_return_type
        return f"set(stack_pointer-{len(variables) - 1}, {parse_node(node.children[0])[0]});\n" \
               f"stack_pointer-={len(variables) - 1};\n" \
               f"goto *stack_trace[stack_trace_pointer--];\n"


def parse_node(node):
    corresponding_functions_from_type = {variable: create_variable, var_declare: create_variable_declaration,
                                         assign: create_assign,
                                         bin_op: create_bin_op, constant: create_constant,
                                         function_call: create_function_call,
                                         declare_func: create_function_declaration,
                                         unary_op: create_unary_op}
    corresponding_functions_from_name = {"while": create_while, "if": create_if, "return": create_return}
    func = corresponding_functions_from_type.get(type(node.name), corresponding_functions_from_name.get(node.name))
    if func is not None:
        return func(node)
    if "body" in node.name:
        return create_body(node)
    raise Exception("syntax error", node.name)


def build(listing, name, print_tree=True):
    global functions, lbl_counter, current_function_return_type, functions_index
    functions_index = Counter()
    functions = defaultdict(list)
    lbl_counter = 0
    program = create_ast(listing)
    for child_index, child in enumerate(program.children):
        assert type(child.name) == declare_func, f"Unexpected syntax '{child.name}', expected function declaration"
        if child.name.type == "void":
            Node("return", parent=program.children[child_index].children[1])
        arguments = [x.name.type for x in child.children[0].children]
        functions[child.name.name].append(
            signature(child.name.type, arguments, child.children[1], len(functions[child.name.name])))  # put first actually
    if print_tree:
        for pre, fill, node in RenderTree(program):
            print("%s%s" % (pre, node.name))
    assert "main" in functions, "no entry point"
    with open(f"template.cpp", "r") as file:
        out = file.read()
    for child in program.children:
        current_function_return_type = child.name.type
        out += parse_node(child)
    out += "$0:\nmyfile.close();\n}"
    with open(f"build/{name}.cpp", "w") as file:
        file.write(out)


def build_and_run(listing, name, print_tree=True):
    build(listing, name, print_tree=print_tree)
    os.system(f'g++ build/{name}.cpp -o build/{name}.exe')
    os.system(rf".\\build\\{name}.exe")


if __name__ == '__main__':
    to_run = ["array"]
    args = sys.argv
    if len(args) == 2:
        to_run = [args[1]]
    for filename in to_run:
        with open(f"test/{filename}.barter", "r") as file:
            build_and_run(file.read(), name=filename)

#include <iostream>

# int main() {
#   char ar []= {1,1,8};
#   char * ptr = ar;
#   short  * ptr2 = reinterpret_cast <short  *>(ptr);
#   std::cout << *ptr2;
# }
