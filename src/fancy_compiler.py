from brand_new_ast import parse_program
from global_def import Global
from util import *
from parse_to_source import *
from system_functions import *


def do_function_call(node):
    func_name = node.name.function_name
    before = ""
    args = []
    for ind, child in enumerate(node.children):
        bef, expr = do(child)
        before += bef
        args.append(expr)
        before += f"stack.append({expr.value}); "
    return expression(before + func_name + "(); ", "system")


def do(node):
    if type(node.name) == function_call:
        value, typeof = do_function_call(node)
        return value, expression(f"stack.pop()", typeof)
    if type(node.name) == constant:
        return "", expression(f"{node.name.value}", node.name.type)
    if type(node.name) == variable:
        var = Global.variables[node.name.name]
        return "", expression(f"stack[top_pointer_stack[-1]+{var.ind}]", var.type)
    raise Exception(node.name)


def create_source(program):
    res = ""
    for function in program.children:
        function_name, return_type = function.name
        Global.functions[function_name] = signature(return_type, [], function.children[0])
    for function in Global.functions:
        res += f"def {function}():\n    "
        for sub_function in Global.functions[function].body.children:
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
                value = sub_function.children[0]
                bef, value = do(value)
                res += bef + create_return(value.value)
            if type(sub_function.name) == function_call:
                bef, value = do(sub_function)
                res += bef + value.value + "; "
    return res


def build(filename="default"):
    listing = """
        func return_5() void {
            return 5
        }
        func main() void {
            return 2
            int x = sum(3,dif(mul(1,2),div(10,1)))
            x = return_5()
            //int x = 3 + (2*1 - 10/1)
            cout(x)
        }
        """
    ast = parse_program(listing)
    print_tree(ast)
    res = create_source(ast)
    with open("cool_template.py", "r") as template:
        listing = template.read() + res + "\nif __name__ == '__main__':\n\tmain()"
    with open(f'build/{filename}.py', 'w') as f:
        f.write(listing)


def main():
    build()


if __name__ == '__main__':
    main()
