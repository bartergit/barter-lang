from create_ast import *
import sys
import os


class Global:
    variables = {}
    arrays = {}
    functions = {}
    ind = 0

    @staticmethod
    def sum(x, y):
        return f"stack.append({x}); stack.append({y}); sum(); "

    @staticmethod
    def dif(x, y):
        return f"stack.append({y}); stack.append({x}); dif(); "

    @staticmethod
    def lt(x, y):
        return f"stack.append({y}); stack.append({x}); lt(); "

    @staticmethod
    def cout(*args):
        out = ""
        for arg in args:
            out += f"stack.append('{arg}'); "
        return out + f"stack.append({len(args)}); cout(); "

    @staticmethod
    def cond(compare, block):
        out = f"\nif {compare}: "
        out += block
        return out + "\n"

    @staticmethod
    def dec_var(name, typeof, value):
        if Global.variables.get(name) is None:
            assert typeof in types
            Global.variables[name] = dec_var(typeof, Global.ind)
            Global.ind += 1
            return f"stack.append({value}); "
        raise Exception(f"{name} is already declared")

    @staticmethod
    def set_var(name, value):
        if Global.variables.get(name) is not None:
            ind = Global.variables[name].ind
            return f"stack[top_pointer_stack[-1]+{ind}] = {value}; "
        raise Exception(f"{name}??")

    # arrays
    @staticmethod
    def dec_arr(name, typeof, size):
        if Global.arrays.get(name) is None:
            assert typeof in types
            Global.arrays[name] = dec_arr("arr " + typeof, Global.ind, int(size))
            Global.ind += int(size)
            return f"stack.append(0); " * int(size)
        raise Exception(f"{name} is already declared")

    @staticmethod
    def index(name, pos_index):
        if Global.arrays.get(name) is not None:
            pos_index = int(pos_index)
            assert 0 <= pos_index < Global.arrays[name].size, f"{name}[{pos_index}]??"
            ind = Global.arrays[name].ind + pos_index
            return f"stack.append(stack[top_pointer_stack[-1]+{ind}]); "
        raise Exception(f"{name}??")

    @staticmethod
    def set_arr(name, pos_index, value):
        if Global.arrays.get(name) is not None:
            pos_index = int(pos_index)
            assert 0 <= pos_index < Global.arrays[name].size
            ind = Global.arrays[name].ind + pos_index
            return f"stack[top_pointer_stack[-1]+{ind}] = {value}; "
        raise Exception(f"{name}??")

    # end of array
    @staticmethod
    def set_arg(name, typeof):
        Global.variables[name] = dec_var(typeof, Global.ind)
        Global.ind += 1
        return ""

    @staticmethod
    def dec_func(name, _return_type, _args, body_block):
        # print(return_type, args, Global.functions[name].args)
        return f"\ndef {name}():\n    global stack; {body_block}\n"

    @staticmethod
    def ret(value):
        return f"stack[top_pointer_stack[-1]] = {value}; stack = stack[:top_pointer_stack.pop() + 1]; return; "


def do_block(node):
    ret = ""
    for child in node.children:
        value, typeof = do(child)
        ret += value
        if typeof == "expr int":  # change this this!
            ret += "stack.pop(); "
    return ret


def do_function_call(node):
    func_name = node.name.function_name
    if func_name == "dec_func":
        Global.variables = {}
        Global.arrays = {}
        Global.ind = 0
    before = ""
    args = []
    if func_name in Global.functions:  # check number of args
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
        if func_name in Global.functions:
            expected_arg = Global.functions[func_name].args[ind]
            assert expr.type == expected_arg.type, \
                f"'{func_name}', arg '{expected_arg.value}', got {expr.type} instead of {expected_arg.type}"
        if func_name == "dec_var" and ind == 2:
            assert expr.type == args[1], f"'{args[0]}', expected {args[1]}, got {expr.type} instead"
        if func_name == "set_var" and ind == 1:
            expected_type = Global.variables[args[0]].type
            assert expr.type == expected_type, f"'{args[0]}', expected {expected_type}, got {expr.type} instead"
        # type check end
    if func_name in Global.functions:  # declared function
        for arg in args:
            before += f"stack.append({arg}); "
        before += f"top_pointer_stack.append(len(stack)-{len(node.children)}); "
        return expression(before + f"{node.name.function_name}(); ", Global.functions[func_name].return_type)
    else:  # sys func
        return expression(before + vars(Global)[node.name.function_name].__func__(*args), "system")


def do(node):
    if type(node.name) == function_call:
        if node.name.function_name == "block":
            return expression(do_block(node), "block")
        value, typeof = do_function_call(node)
        return expression(value, "expr " + typeof)
    if type(node.name) == constant:
        return expression(node.name.value, node.name.type)
    if type(node.name) == variable:
        var = Global.variables[node.name.name]
        return expression(f"stack[top_pointer_stack[-1]+{var.ind}]", var.type)
    raise Exception(node.name)


def create_source(ast):
    out = ""
    for child in ast.children:
        function_name, return_type, args, body_block = child.children
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
    run = sys.argv[1] == "run"
    filename = "functionality"
    build(filename, run)
    if run:
        os.system(f'py build/{filename}.py')


if __name__ == "__main__":
    main()
