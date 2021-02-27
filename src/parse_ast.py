from anytree import Node, RenderTree
from collections import namedtuple
from create_ast import create_ast, bin_op, variable, constant, assign, declare, function_call, declare_func
variables = {}
builtin_functions = {"print": {"return_type":"void", "args":["int"]}, "neg": {"return_type":"bool", "args": ["bool"]}}
functions = {}
operators = {"-": ["int", "int", "int"], "+": ["int", "int", "int"], "<": ["int", "int", "bool"], ">": ["int", "int", "bool"], 
"!=": ["int", "int", "bool"]}

def f(node):
    if type(node.name) == declare:
        var_name, typeof = node.name.name, node.name.type
        variables[var_name] = typeof
        assert len(node.children) <= 1
        if len(node.children):
            expr = f(node.children[0])
            assert expr[1] == typeof, f"{node.name} {expr} {node.children[0].name}, expected type {typeof} got {expr[1]}"
            return "%s %s = %s;\n" % (typeof, var_name, expr[0])
        else:
            return "%s %s;\n" % (typeof, var_name)
    if type(node.name) == assign:
        var_name = node.name.name
        assert len(node.children) == 1
        expr = f(node.children[0])
        assert expr[1] == variables[var_name], f"expected type {variables[var_name]} got {expr[1]}"
        return "%s = %s;\n" % (var_name, expr[0])
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
    if type(node.name) == function_call:
        args = ""
        func_name = node.name.name
        if func_name in functions:
            return_type = functions[func_name].name.type
            args_node = functions[func_name].children[0].children
            assert len(args_node) == len(node.children)
            for ind, child in enumerate(node.children):
                val, typeof = f(child)
                assert args_node[ind].name.type == typeof 
                args += val + ","
            if len(args):
                args = args[:-1]   
        elif func_name in builtin_functions:
            return_type = builtin_functions[func_name]["return_type"]
            args_node = builtin_functions[func_name]["args"]
            assert len(args_node) == len(node.children)
            for ind, child in enumerate(node.children):
                val, typeof = f(child)
                assert args_node[ind] == typeof 
                args += val + ","
            if len(args):
                args = args[:-1]
        else:
            raise Exception("syntax error")
        return "%s(%s)" % (func_name, args), return_type
    if type(node.name) == declare_func:
        args = ""
        assert node.children[0].name == "arguments"
        assert node.children[1].name == "func_body"
        for child in node.children[0].children:
            assert type(child.name) == declare
            args += f(child)[:-2] + ","
        if len(args):
            args = args[:-1]
        return "%s %s (%s) {\n%s}\n" % (node.name.type, node.name.name, args, f(node.children[1]))
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
            line = f(child)
            if type(line) == tuple:
                out += line[0] + ";\n"
            else:
                out += line
        return out
    if node.name == "return":
        assert len(node.children) == 1
        returned = f(node.children[0])
        return "return %s;\n" % f(node.children[0])[0]
    raise Exception("syntax error", node.name)


if __name__ == '__main__':
    listing = """
    func sum(int x, int y) int {
        int res = x + y
        return res
    }
    func Euclidean_algorithm(int a, int b) int {
        while b != 0 {
            if a > b {
                a = a - b
            } else {
                b = b - a
            }
        }
        return a 
    }
    func main() void {
        bool f = true
        int gcd = Euclidean_algorithm(13, 24)
        print(gcd)
    }
    """
    program = create_ast(listing)
    for pre, fill, node in RenderTree(program):
        print("%s%s" % (pre, node.name))
    for child in program.children:
        assert type(child.name) == declare_func, f"Unexpected syntax '{child.name}', expected function declaration"
        functions[child.name.name] = child
    assert "main" in functions, "no entry point"
    # for pre, fill, node in RenderTree(functions["sum"]):
    #     print("%s%s" % (pre, node.name))
    for child in program.children:
        print(f(child))





