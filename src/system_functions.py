from global_def import Global
from util import *


def create_variable_declaration(name, typeof, value):
    if Global.variables.get(name) is None:
        assert typeof in types, typeof
        Global.variables[name] = indexed_var(typeof, Global.ind)
        Global.ind += 1
        return f"stack.append({value}); "
    raise Exception(f"{name} is already declared")


def create_return(value):
    return f"stack[top_pointer_stack[-1]] = {value}; stack = stack[:top_pointer_stack.pop() + 1]; return;"


def create_assignment(name, value):
    if Global.variables.get(name):
        ind = Global.variables[name].ind
        return f"stack[top_pointer_stack[-1]+{ind}] = {value}; "
    raise Exception(f"{name}??")
