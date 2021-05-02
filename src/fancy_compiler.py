import os

from brand_new_ast import parse_program
from global_def import Global
from util import *
from system_functions import *


def refer(node):
    value = Global.variables[node.children[0].name.name].ind
    return expression(f'push({value}); ', 'ref')


def deref(node):
    bef, expr = do(node.children[0])
    return expression(bef + f"push(stack[{expr.value}]); ", 'int')


def declare_array(node):
    bef, expr = do(node.children[1])
    name = node.children[0].name.name
    size = expr.value
    if Global.variables.get(name) is None:
        Global.variables[name] = variable_declaration("arr", Global.ind)
        index = Global.ind
        Global.ind += int(size)
        return expression(bef + f"push(0); " * int(size) + f"push({index}+last()); ",
                          'der')  # should be changed
        # check behaviour on func
    raise Exception(f"{name} is already declared")


def set_ref(node):
    bef_1, expr_index = do(node.children[0])
    bef_2, expr_value = do(node.children[1])
    return expression(bef_1 + bef_2 + f"stack[{expr_index.value}] = {expr_value.value};  push(0); ",
                      'system')  # unnecessary append

def line(node):
    return expression("cout << '\\n';\n", "system")

special_funcs = {"ref": refer, "deref": deref, "dec_arr": declare_array, "set_ref": set_ref, "line": line}


def do_function_call(node):
    func_name = node.name.function_name
    if func_name in special_funcs:
        return special_funcs[func_name](node)
    before = ""
    args = []
    if func_name in Global.functions:
        return_type = Global.functions[func_name].return_type
    else:
        return_type = Global.corresponding[func_name].return_type
    for ind, child in enumerate(node.children):
        bef, expr = do(child)
        before += bef
        args.append(expr)
        before += f"push({expr.value}); "
    if func_name in Global.functions:
        # before += f"top_pointer_push(stack_pointer-{len(args)}); "
        # if Global.functions[func_name].return_type != "void" and len(args) == 0:  # dont need this in c++
        #     before += "push(0); "
        function_call_text = f"top_pointer_stack[++top_pointer] = stack_pointer - {len(node.children)} + 1;\n" \
                             f"stack_trace[++stack_trace_pointer] = &&${Global.label};\n" \
                             f"goto {func_name};\n" \
                             f"${Global.label}:\n"
    else:
        function_call_text = f"stack_trace[++stack_trace_pointer] = &&${Global.label};\n" \
                             f"goto {func_name};\n" \
                             f"${Global.label}:\n"
    Global.label += 1
    return expression(before + function_call_text, return_type)


def do(node):
    if type(node.name) == function_call:
        value, typeof = do_function_call(node)
        return value, expression(f"pop()", typeof)
    if type(node.name) == constant:
        return "", expression(f"{node.name.value}", node.name.type)
    if type(node.name) == variable:
        assert node.name.name in Global.variables, f"{node.name.name}, {Global.variables}"
        var = Global.variables[node.name.name]
        return "", expression(f"stack[last()+{var.ind}]", var.type)
    raise Exception(node.name)

def parse_body(node):
    res = ""
    for sub_function in node.children:
        if sub_function.name == "if":
            condition = sub_function.children[0]
            bef, value = do(condition)
            res += bef + "if (%s) {\n%s\n;\n}\n" % (value.value, parse_body(sub_function.children[1]))
        if sub_function.name == "while":
            condition = sub_function.children[0]
            label = Global.label
            Global.label += 1
            bef, value = do(condition)
            bef = f"${label}:\n" + bef
            res += bef + "if (%s) {\n%s\n;\n goto $%s;\n}\n" % (value.value, parse_body(sub_function.children[1]), label)
        if type(sub_function.name) == variable_declaration:
            typeof, name = sub_function.name
            value = sub_function.children[0]
            bef, value = do(value)
            res += bef + create_variable_declaration(name, typeof, value.value)
        if type(sub_function.name) == assignment:
            value = sub_function.children[0]
            bef, value = do(value)
            res += bef + create_assignment(sub_function.name.name, value.value)
        if sub_function.name == "return":
            if len(sub_function.children):
                value = sub_function.children[0]
                bef, value = do(value)
                res += bef + create_return(value.value)
            else:
                res += create_return_void()
        if type(sub_function.name) == function_call:
            bef, value = do(sub_function)
            if value.type == "void":
                res += bef
            else:
                res += bef + value.value + "; "
    res += "\n"
    return res

def create_source(program):
    res = ""
    for function in program.children:
        function_name, return_type = function.name
        Global.functions[function_name] = signature(return_type, [x.name for x in function.children[0].children],
                                                    function.children[1])
    for function in Global.functions:
        res += "\n%s:\n" % function
        set_args(function)
        res += parse_body(Global.functions[function].body)
        if function == "main":
            res += "$0:\nmyfile.close();\n}\n"
    return res


def build(filename="bubble_sort"):
    with open(f"test/{filename}.barter", "r") as listing:
        listing_text = listing.read()
    ast = parse_program(listing_text)
    # print_tree(ast)
    res = create_source(ast)
    with open("template.cpp", "r") as template:
        listing = template.read() + res
    with open(f'build/{filename}.cpp', 'w') as f:
        f.write(listing)
    os.system(f'g++ build/{filename}.cpp -o build/{filename}.exe')
    os.system(rf".\\build\\{filename}.exe")


def main():
    build()


if __name__ == '__main__':
    main()