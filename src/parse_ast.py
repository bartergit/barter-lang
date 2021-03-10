from anytree import Node, RenderTree
from collections import namedtuple
from create_ast import create_ast, bin_op, variable, constant, assign, declare, function_call, declare_func
import os


def cout(args):
    out = "cout << "
    for arg in args:
        out += arg
        out += ' << " " << '
    out += "'\\n';\n"
    return out


def log(args):
    out = 'myfile'
    for arg in args:
        out += " << ";
        out += arg
        out += " << '\\n'"
    return out


builtin_functions = {
    "print": {"return_type": "void", "args": ["int"], "implementation": cout},
    "neg": {"return_type": "bool", "args": ["bool"]},
    "log": {"return_type": "void", "args": ["int"], "implementation": log}
}
functions = {}
operators = {"-": ["int", "int", "int"], "+": ["int", "int", "int"], "<": ["int", "int", "bool"],
             ">": ["int", "int", "bool"], "<=": ["int", "int", "bool"],
             "!=": ["int", "int", "bool"], "*": ["int", "int", "int"], "==": ["int", "int", "bool"]}
variables = {}
ind = 0
lbl_counter = 0
current_function_return_type = None


def f(node, additional_index=None):
    global ind
    global variables
    global lbl_counter
    if type(node.name) == variable:
        var_name = node.name.name
        assert var_name in variables, f"no such variable: {var_name}"
        i = len(variables) - variables[var_name]["ind"]
        if additional_index:
            i += additional_index
        return f"get(stack_pointer - {i})", variables[var_name]["type"]
    if type(node.name) == declare:
        var_name, typeof = node.name.name, node.name.type
        assert var_name not in variables, f"{var_name} already exists"
        if len(node.children):
            expr = f(node.children[0])
            ind += 1
            variables[var_name] = {"type": typeof, "ind": ind}
            assert expr[
                       1] == typeof, f"{node.name} {expr} {node.children[0].name}, expected type {typeof} got {expr[1]}"
            if type(node.children[0].name) == function_call:
                return "%spush(pop());\n" % (expr[0])
            else:
                return "push(%s);\n" % (expr[0])
        else:
            ind += 1
            variables[var_name] = {"type": typeof, "ind": ind}
            return "push(0);\n"
    if type(node.name) == assign:
        var_name = node.name.name
        expr = f(node.children[0])
        assert expr[1] == variables[var_name]["type"], f"expected type {variables[var_name]['type']} got {expr[1]}"
        i = len(variables) - variables[var_name]["ind"]
        if type(node.children[0].name) == function_call:
            return "%sset(stack_pointer - %s, pop());\n" % (expr[0], i)
        return "set(stack_pointer - %s, %s);\n" % (i, expr[0])
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
    if type(node.name) == function_call:
        func_name = node.name.name
        if func_name in functions:
            args = ""
            return_type = functions[func_name].name.type
            args_node = functions[func_name].children[0].children
            assert len(args_node) == len(node.children)
            for i, child in enumerate(node.children):
                val, typeof = f(child, i)
                assert args_node[i].name.type == typeof
                args += f"push({val});\n"
            lbl_counter += 1
            return "%sstack_trace[++stack_trace_pointer] = &&$%s;\ngoto %s;\n$%s:\n" % \
                   (args, lbl_counter, func_name, lbl_counter), return_type
        elif func_name in builtin_functions:
            return_type = builtin_functions[func_name]["return_type"]
            args_node = builtin_functions[func_name]["args"]
            assert len(args_node) == len(node.children)
            args = []
            for i, child in enumerate(node.children):
                val, typeof = f(child)
                assert args_node[i] == typeof
                args.append(val)
            return builtin_functions[func_name]["implementation"](args), return_type
        else:
            raise Exception("syntax error")
    if type(node.name) == declare_func:
        ind = 0
        variables = {}
        args = ""
        assert node.children[0].name == "arguments"
        assert node.children[1].name == "func_body"
        for child in node.children[0].children:
            args += f(child)[:-2] + ";\n"
        return "%s:\n%s" % \
               (node.name.name, f(node.children[1]))
    if node.name == "while":
        assert len(node.children) == 2, node.children
        compare = f(node.children[0])
        assert compare[1] == "bool", "expected bool expression in while"
        lbl_counter += 1
        if_lable_counter = lbl_counter
        return "$%s:\nif (%s) {\n%sgoto $%s;\n}\n" % (
        if_lable_counter, compare[0], f(node.children[1]), if_lable_counter)
    if node.name == "if":
        compare = f(node.children[0])
        assert compare[1] == "bool", "expected bool expression in if"
        assert node.children[1].name == "if_body"
        if len(node.children) == 3:
            return "if (%s) {\n%s} else {\n%s}\n" % (compare[0], f(node.children[1]), f(node.children[2]))
        elif len(node.children) == 2:
            return "if (%s) {\n%s}\n" % (compare[0], f(node.children[1]))
    if "body" in node.name:
        out = ""
        for child in node.children:
            line = f(child)
            if type(line) == tuple:
                out += line[0] + ";\n"
            else:
                out += line
        return out
    if node.name == "return":
        if current_function_return_type == "void":
            assert len(node.children) == 0
            return "stack_pointer-=%s;\ngoto *stack_trace[stack_trace_pointer--];\n" % (len(variables))
        else:
            returned = f(node.children[0])
            assert returned[1] == current_function_return_type
            return "set(stack_pointer-%s, %s);\nstack_pointer-=%s;\ngoto *stack_trace[stack_trace_pointer--];\n" % (
            len(variables) - 1, f(node.children[0])[0], len(variables) - 1)
    raise Exception("syntax error", node.name)


def create_program(listing, name, run=True, print_tree=True):
    global functions
    global current_function_return_type
    functions = {}
    global lbl_counter
    lbl_counter = 0
    program = create_ast(listing)
    for child_index, child in enumerate(program.children):
        assert type(child.name) == declare_func, f"Unexpected syntax '{child.name}', expected function declaration"
        if child.name.type == "void":
            Node("return", parent=program.children[child_index].children[1])
        functions[child.name.name] = child
    if print_tree:
        for pre, fill, node in RenderTree(program):
            print("%s%s" % (pre, node.name))
    assert "main" in functions, "no entry point"
    with open(f"template.cpp", "r") as file:
        out = file.read()
    for child in program.children:
        current_function_return_type = child.name.type
        out += f(child)
    out += "$0:\nmyfile.close();\n}"
    with open(f"build/{name}.cpp", "w") as file:
        file.write(out)
    if run:
        os.system(f'g++ build/{name}.cpp -o build/{name}.exe')
        os.system(rf".\\build\\{name}.exe")


if __name__ == '__main__':
    to_run = ["void"]
    for filename in to_run:
        with open(f"test/{filename}.barter", "r") as file:
            create_program(file.read(), name=filename, run=True)
