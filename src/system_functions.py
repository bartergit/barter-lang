from global_def import Global
from util import *


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
