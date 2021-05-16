from global_def import Global
from util import *
import os
import sys

def type_exception(name, expected, got):
    return TypeError(f"in {name} expected '{expected}', got '{got}' instead")


def create_variable_declaration(name, typeof, value):
    if Global.variables.get(name) is None:
        assert typeof in types, typeof
        Global.variables[name] = indexed_var(typeof, Global.ind)
        Global.ind += 1
        return f"push({value}); "
    raise Exception(f"{name} is already declared")


def create_return(value):
    return f"stack[last()] = {value}; stack_pointer = top_pointer_pop(); goto *stack_trace[stack_trace_pointer--];"


def create_return_void():
    return f"stack_pointer = top_pointer_pop(); goto *stack_trace[stack_trace_pointer--];\n"


def create_assignment(name, value):
    if Global.variables.get(name):
        ind = Global.variables[name].ind
        return f"stack[last()+{ind}] = {value}; "
    raise Exception(f"{name}??")


def set_args(function):
    Global.variables = {}
    Global.ind = 0
    for arg in Global.functions[function].args:
        Global.variables[arg.name] = indexed_var(arg.type, Global.ind)
        Global.ind += 1


def refer(node):
    value = Global.variables[node.children[0].name.name].ind
    return expression(f'push({value}); ', 'ref')


def deref(node):
    bef, expr = do(node.children[0])
    return expression(bef + f"push(stack[{expr.value}]); ", 'int')


def declare_array(node):
    size = do(node.children[0])[1].value
    index = Global.ind
    Global.ind += int(size)
    return expression(f"push(0); " * int(size) + f"push({index}+last()); ", 'int')  # should be changed


def set_ref(node):
    bef_1, expr_index = do(node.children[0])
    bef_2, expr_value = do(node.children[1])
    return expression(bef_1 + bef_2 + f"stack[{expr_index.value}] = {expr_value.value};  push(0); ",
                      'void')  # unnecessary append

def cout(node):
    bef = ""
    for child in node.children:
        before, expr = do(child)
        bef += before
        value = expr.value if expr.type == "int" else booled(expr.value)
        bef += f"cout << {value} << ' ';\n"
    bef += "cout << '\\n';\n"
    return expression(bef, "void")


special_funcs = {"ref": refer, "deref": deref, "dec_arr": declare_array, "set_ref": set_ref, "cout": cout}


def do_function_call(node):
    func_name = node.name.function_name
    if func_name in special_funcs:
        return special_funcs[func_name](node)
    before = ""
    args = []
    if func_name in Global.functions:
        return_type = Global.functions[func_name].return_type
        expected_args = Global.functions[func_name].args
    else:
        return_type = Global.corresponding[func_name].return_type
        expected_args = Global.corresponding[func_name].args
    assert len(expected_args) == len(node.children), f"expected {len(expected_args)}, got {len(node.children)}"
    for ind, child in enumerate(node.children):
        bef, expr = do(child)
        before += bef
        args.append(expr)
        expected_type = expected_args[ind].type
        if expected_type != expr.type:
            raise type_exception(f"function '{func_name}', {ind}th arg '{expected_args[ind].name}'", expected_type,
                                 expr.type)
        before += f"push({expr.value}); "
    if func_name in Global.functions:
        function_call_text = f"top_pointer_stack[++top_pointer] = stack_pointer - {len(node.children)} + 1;\n" \
                             f"stack_trace[++stack_trace_pointer] = &&${Global.label};\n" \
                             f"goto {func_name};\n" \
                             f"${Global.label}:\n"
    else:
        function_call_text = f"stack_trace[++stack_trace_pointer] = &&${Global.label};\n" \
                             f"goto _{func_name};\n" \
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
            if "bool" != value.type:
                raise type_exception(f"condition", "bool", value.type)
            res += bef + "if (%s) {\n%s\n;\n}\n" % (value.value, parse_body(sub_function.children[1]))
        if sub_function.name == "while":
            condition = sub_function.children[0]
            label = Global.label
            Global.label += 1
            bef, value = do(condition)
            if "bool" != value.type:
                raise type_exception(f"loop", "bool", value.type)
            bef = f"${label}:\n" + bef
            res += bef + "if (%s) {\n%s\n;\n goto $%s;\n}\n" % (
                value.value, parse_body(sub_function.children[1]), label)
        if type(sub_function.name) == variable_declaration:
            typeof, name = sub_function.name
            value = sub_function.children[0]
            bef, value = do(value)
            if typeof != value.type:
                raise type_exception(f"{name} variable declaration", typeof, value.type)
            res += bef + create_variable_declaration(name, typeof, value.value)
        if type(sub_function.name) == assignment:
            name = sub_function.name.name
            value = sub_function.children[0]
            bef, value = do(value)
            expected_type = Global.variables.get(name).type
            if expected_type != value.type:
                raise type_exception(f"{name} assignment", expected_type, value.type)
            res += bef + create_assignment(name, value.value)
        if sub_function.name == "return":
            Global.have_return = True
            if len(sub_function.children):
                value = sub_function.children[0]
                bef, value = do(value)
                if Global.return_type != value.type:
                    raise type_exception("return", Global.return_type, value.type)
                res += bef + create_return(value.value)
            else:
                assert Global.return_type == "void"
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
    if getattr(sys, 'frozen', False):
        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    template_path = os.path.join(application_path, "template.cpp")
    with open(template_path, "r") as template:
        res = template.read()
    for function in program.children:
        function_name, return_type = function.name
        Global.functions[function_name] = signature(return_type, [x.name for x in function.children[0].children],
                                                    function.children[1])
    for function in Global.functions:
        res += "\n%s:\n" % function
        set_args(function)
        Global.have_return = False
        Global.return_type = Global.functions[function].return_type
        res += parse_body(Global.functions[function].body)
        assert Global.have_return, f"'{function}' should have explicit return"
        if function == "main":
            res += "$0:;\n}\n"
            # res += "$0:\nmyfile.close();\n}\n"
    return res
