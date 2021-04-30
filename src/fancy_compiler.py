import os

from brand_new_ast import parse_program
from global_def import Global
from util import *
from system_functions import *


def refer(node):
    value = Global.variables[node.children[0].name.name].ind
    return expression(f'stack.append({value}); ', 'ref')


def deref(node):
    bef, expr = do(node.children[0])
    return expression(bef + f"stack.append(stack[{expr.value}]); ", 'int')


def declare_array(node):
    bef, expr = do(node.children[1])
    name = node.children[0].name.name
    size = expr.value
    if Global.variables.get(name) is None:
        Global.variables[name] = variable_declaration("arr", Global.ind)
        index = Global.ind
        Global.ind += int(size)
        return expression(bef + f"stack.append(0); " * int(size) + f"stack.append({index}); ",
                          'der')  # should be changed
        # check behaviour on func
    raise Exception(f"{name} is already declared")


def set_ref(node):
    bef_1, expr_index = do(node.children[0])
    bef_2, expr_value = do(node.children[1])
    return expression(bef_1 + bef_2 + f"stack[{expr_index.value}] = {expr_value.value};  stack.append(0); ",
                      'system')  # unnecessary append


special_funcs = {"ref": refer, "deref": deref, "dec_arr": declare_array, "set_ref": set_ref}


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
        before += f"stack.append({expr.value}); "
    if func_name in Global.functions:
        before += f"top_pointer_stack.append(len(stack)-{len(args)}); "
        if Global.functions[func_name].return_type != "void" and len(args) == 0:  # dont need this in c++
            before += "stack.append(0); "
    return expression(before + func_name + "(); ", return_type)


def do(node):
    if type(node.name) == function_call:
        value, typeof = do_function_call(node)
        return value, expression(f"stack.pop()", typeof)
    if type(node.name) == constant:
        return "", expression(f"{node.name.value}", node.name.type)
    if type(node.name) == variable:
        assert node.name.name in Global.variables, f"{node.name.name}, {Global.variables}"
        var = Global.variables[node.name.name]
        return "", expression(f"stack[top_pointer_stack[-1]+{var.ind}]", var.type)
    raise Exception(node.name)

def parse_body(node):
    res = ""
    for sub_function in node.children:
        if sub_function.name == "if":
            condition = sub_function.children[0]
            bef, value = do(condition)
            res += bef + f"if {value.value}: " + parse_body(sub_function.children[1])
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
        res += f"def {function}():\n    global stack; "
        set_args(function)
        res += parse_body(Global.functions[function].body)
    return res


def build(filename="default"):
    listing = """
        func pass_ref (int x) void {
            cout(x)
            set_ref(x,10)
            set_ref(sum(x,1),15)
            set_ref(sum(x,2),20)
            return
        }
        func dec_ref () void {
            int z = 18
            int arr = dec_arr(a,3)
            pass_ref(arr)
            cout(deref(sum(arr,0)))
            cout(deref(sum(arr,1)))
            cout(deref(sum(arr,2)))
        }
        func main () void {
            //if true {
                cout(3)
            //}
            int a = false
            cout(a)
            int x = 99
            int y = 3
            dec_ref()
        }
        """
    ast = parse_program(listing)
    # print_tree(ast)
    res = create_source(ast)
    with open("cool_template.py", "r") as template:
        listing = template.read() + res + "\nif __name__ == '__main__':\n   main()"
    with open(f'build/{filename}.py', 'w') as f:
        f.write(listing)
    os.system(f"py build/{filename}.py")


def main():
    build()


if __name__ == '__main__':
    main()
