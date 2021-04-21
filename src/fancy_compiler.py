from brand_new_ast import parse_program
from global_def import Global
from util import *
from parse_to_source import *
from system_functions import *


def do_function_call(node):
    func_name = node.name.function_name
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





def create_source(program):
    res = ""
    for function in program.children:
        function_name, return_type = function.name
        Global.functions[function_name] = signature(return_type, [x.name for x in function.children[0].children],
                                                    function.children[1])
    for function in Global.functions:
        res += f"def {function}():\n    global stack; "
        set_args(function)
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


def build(filename="default"):
    listing = """
        func return_5 () int {
            return 5
        }
        func inc (int x) int {
            return sum(x,1)
        }
        func cout_3 () void {
            cout(3)
            return
        }
        func cout_sum (int x int y) int {
            int res = sum(x,y)
            cout(res)
            return res
        }
        func main () void {
            int x = 9
            x = sum(3,dif(mul(1,2),div(10,1)))
            //int x = 3 + (2*1 - 10/1)
            cout(x)
            cout_3()
        }
        """
    ast = parse_program(listing)
    print_tree(ast)
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
