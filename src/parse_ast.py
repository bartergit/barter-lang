from anytree import Node, RenderTree
from collections import namedtuple
from create_ast import create_ast, bin_op, variable, constant, assign, declare, function_call, declare_func


def cout(args):
    out = "cout << "
    for arg in args:
        out += arg
        out += ' << " " << '
    out += "'\\n';\n"
    return out

builtin_functions = {"print": {"return_type":"void", "args":["int"], "implementation": cout}, "neg": {"return_type":"bool", "args": ["bool"]}}
functions = {}
operators = {"-": ["int", "int", "int"], "+": ["int", "int", "int"], "<": ["int", "int", "bool"], ">": ["int", "int", "bool"], 
"!=": ["int", "int", "bool"]}
variables = {}
ind = 0
lbl_counter = 0

def f(node):
    global ind
    global variables
    global lbl_counter
    if type(node.name) == declare:
        var_name, typeof = node.name.name, node.name.type
        assert var_name not in variables, f"{var_name} already exists"
        # assert len(node.children) <= 1
        if len(node.children):
            expr = f(node.children[0])
            if type(node.children[0].name) == function_call: 
                variables[var_name] = {"type": typeof, "ind": ind}
                assert expr[1] == typeof, f"{node.name} {expr} {node.children[0].name}, expected type {typeof} got {expr[1]}"  
                return "%spush(pop());\n" % (expr[0])
            else:
                ind += 1
                variables[var_name] = {"type": typeof, "ind": ind}
                assert expr[1] == typeof, f"{node.name} {expr} {node.children[0].name}, expected type {typeof} got {expr[1]}"
                return "push(%s);\n" % (expr[0])
        # return "%s %s = %s;\n" % (typeof, var_name, expr[0])
        else:
            ind += 1
            variables[var_name] = {"type": typeof, "ind": ind}
            return "push(0);\n"
    if type(node.name) == assign:
        var_name = node.name.name
        # assert len(node.children) == 1
        expr = f(node.children[0])
        assert expr[1] == variables[var_name]["type"], f"expected type {variables[var_name]['type']} got {expr[1]}"
        # return "%s = %s;\n" % (var_name, expr[0])
        i = len(variables) - variables[var_name]["ind"]
        return "set(%s, stack_pointer - %s);\n" % (expr[0], i)
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
        i = variables[var_name]["ind"]
        return f"get(stack_pointer - {len(variables) - i})", variables[var_name]["type"]
        # return var_name, variables[var_name]["type"]
    if type(node.name) == function_call:
        func_name = node.name.name
        if func_name in functions:
            args = ""
            return_type = functions[func_name].name.type
            args_node = functions[func_name].children[0].children
            assert len(args_node) == len(node.children)
            for i, child in enumerate(node.children):
                val, typeof = f(child)
                assert args_node[i].name.type == typeof 
                args += f"push({val});\n"
                ind += 1
            lbl_counter += 1
            return "%sstack_trace[++stack_trace_pointer] = &&$%s;\ngoto %s;\n$%s:\n" % (args, lbl_counter, func_name, lbl_counter), return_type
        elif func_name in builtin_functions:
            return_type = builtin_functions[func_name]["return_type"]
            args_node = builtin_functions[func_name]["args"]
            assert len(args_node) == len(node.children)
            args = []
            for i, child in enumerate(node.children):
                val, typeof = f(child)
                assert args_node[i] == typeof 
                args.append(val)
                return builtin_functions[func_name]["implementation"](args)
        else:
            raise Exception("syntax error")
        
        # return "%s(%s)" % (func_name, args), return_type
    if type(node.name) == declare_func:
        ind = 0
        variables = {}
        # ind -= len(node.children[0].children)
        args = ""
        assert node.children[0].name == "arguments"
        assert node.children[1].name == "func_body"
        for child in node.children[0].children:
            # assert type(child.name) == declare
            args += f(child)[:-2] + ";\n"
        # if len(args):
        #     args = args[:-1]
        return "%s:\n%s" % \
            (node.name.name, f(node.children[1]))
        # return "%s %s (%s) {\n%s}\n" % (node.name.type, node.name.name, args, f(node.children[1]))
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
        returned = f(node.children[0])
        return "set(0,%s);\nstack_pointer=R1;\ngoto *stack_trace[stack_trace_pointer--];\n" % (f(node.children[0])[0])
        # return "return %s;\n" % f(node.children[0])[0]
    raise Exception("syntax error", node.name)

# x y z stack_pointer - len(var) + ind + 1
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
        int res = sum(5,8)
        print(res)
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





