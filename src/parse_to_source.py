from create_ast import *
import sys
import os
from global_def import Global

def do_block(node, is_argument_block=False, return_type=None):
    ret = ""
    for child in node.children:
        value, typeof = do(child)
        ret += value
        if is_argument_block:
            assert child.name.function_name == "set_arg"
            continue
        else:
            assert child.name.function_name != "set_arg"
        if typeof in ["expr " + typeof for typeof in types]:  # excluded void
            ret += "stack.pop(); "
    return ret


def do_system_function(node):
    func_name = node.name.function_name
    if func_name == "dec_func":
        Global.variables = {}
        Global.arrays = {}
        Global.ind = 0
    before = ""
    args = []
    expected_args = None
    if func_name in Global.corresponding:
        return_type, expected_args, body = Global.corresponding[func_name]
        assert len(expected_args) == len(
            node.children), f"'{func_name}' expected {len(expected_args)} args, got {len(node.children)} instead"
    else:
        body = vars(Global)[func_name]
        return_type = "system"
    for ind, child in enumerate(node.children):
        if func_name == "dec_func" and ind == 2:
            expr = expression(do_block(child, is_argument_block=True), "block")
        else:
            expr = do(child)
        if func_name == "dec_func" and ind == 1:
            Global.return_type = expr.value
        if func_name == "ret":
            assert expr.type == Global.return_type, \
                f"function return type is {Global.return_type}, but returned {expr.type}"
        if "expr" in expr.type:
            before += expr.value
            expr = expression(expr.value, expr.type[5:])  # convert 'expr type' to 'type'
            args.append("stack.pop()")
        # elif expr.type == "block":  # ?
        #     args.append(expr.value)
        else:
            args.append(expr.value)
            # args.append(f"'{expr.value}'" if func_name == "cout" and expr.type == "str" else expr.value)  # messy
        if expected_args:
            assert expr.type == expected_args[ind].type, \
                f"'{func_name}', arg '{expected_args[ind].value}', got {expr.type} instead of {expected_args[ind].type}"
        if func_name == "index" and ind == 0:
            # if args[0] in Global.arrays:
            #     return_type = Global.arrays.get(args[0]).type
            # else:
            return_type = Global.variables.get(args[0]).type if args[0] in Global.variables else "int" # change this
            if "arr" in return_type:
                return_type = return_type.split(" ")[1]
        if func_name == "dec_ref" and ind == 2:
            got_type = Global.variables[args[2]].type
            assert args[1] == got_type, f"expected {args[1]}, got {got_type} instead"
        if func_name == "dec_var" and ind == 2:
            assert args[1] in types, f"unknown type {args[1]}"
            assert expr.type == args[1], f"'{args[0]}', expected {args[1]}, got {expr.type} instead"
        if func_name == "set_var" and ind == 1:
            expected_type = Global.variables[args[0]].type
            assert expr.type == expected_type, f"'{args[0]}', expected {expected_type}, got {expr.type} instead"
    return expression(before + body.__func__(*args), return_type)


def do_declared_function(node):
    func_name = node.name.function_name
    before = ""
    args = []
    expected_arg_number = len(Global.functions[func_name].args)
    assert expected_arg_number == len(node.children), \
        f"'{func_name}' expected {expected_arg_number} args, got {len(node.children)} instead"
    for ind, child in enumerate(node.children):
        expr = do(child)
        if "expr" in expr.type:
            before += expr.value
            expr = expression(expr.value, expr.type[5:])  # convert 'expr type' to 'type'
            args.append("stack.pop()")
        elif expr.type == "block":  # ?
            args.append(expr.value)
        else:
            args.append(expr.value)
        # type check
        expected_arg = Global.functions[func_name].args[ind]
        assert expr.type == expected_arg.type, \
            f"'{func_name}', arg '{expected_arg.value}', got {expr.type} instead of {expected_arg.type}"
    for arg in args:
        before += f"stack.append({arg}); "
    before += f"top_pointer_stack.append(len(stack)-{len(node.children)}); "
    return expression(before + f"{node.name.function_name}(); ", Global.functions[func_name].return_type)


def do_function_call(node):
    if node.name.function_name in Global.functions:  # declared function
        return do_declared_function(node)
    else:
        return do_system_function(node)


def do(node):
    if type(node.name) == function_call:
        if node.name.function_name == "block":
            return expression(do_block(node), "block")
        value, typeof = do_function_call(node)
        if typeof != "system":
            typeof = "expr " + typeof
        return expression(value, typeof)
    if type(node.name) == constant:
        return expression(node.name.value, node.name.type)
    if type(node.name) == variable:
        var = Global.variables[node.name.name]
        # return expression(var.ind, var.type)
        return expression(f"stack[top_pointer_stack[-1]+{var.ind}]", var.type)
    raise Exception(node.name)


def create_source(ast):
    out = ""
    for child in ast.children:
        function_name, return_type, args, body_block = child.children  # change this, because it's breaks the errors msgs
        args = [expression(*(y.name[1] for y in x.children)) for x in args.children] if len(
            args.children) else []  # convert to readable form
        return_type = return_type.name.value
        function_name = function_name.name.value
        assert type(child.name) == function_call and child.name.function_name == "dec_func"
        assert return_type in types or return_type == "void", return_type
        Global.functions[function_name] = signature(return_type, args, body_block)
    # print(Global.functions)
    for child in ast.children:
        value, typeof = do(child)
        out += value
    return out


def build(filename, run):
    ast = parse(filename, not run)
    res = create_source(ast)
    with open("template.py", "r") as template:
        listing = template.read() + res + "\nmain()"
        if not run:
            print(listing)
        with open(f'build/{filename}.py', 'w') as f:
            f.write(listing)


def main():
    run = len(sys.argv) > 1 and sys.argv[1] == "run"
    filename = "ref_to_array"
    build(filename, run)
    if run:
        os.system(f'py build/{filename}.py')


if __name__ == "__main__":
    main()
