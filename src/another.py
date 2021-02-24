def function(args):
    for i, arg in args:
        default += f"push(stack[stack_pointer - {len(function['arguments']) - 1}]);\n"
        variables[-1][arg["arg_name"]] = {"type": arg["type"], "ind": ind}
        ind += 1
    default += f"R1 = stack_pointer - {len(function['arguments'])} + 1;\n"

def variable(variable):
    ind = variables[-1][variable]["ind"]
    return f"get({ind})"

def declaration(var_name, value):
    variables[-1][var_name] = {"type": typeof, "ind": ind}
    ind += 1
    return f"push({value})"

def function_call(function_name, args, variable=None):
    out = f"stack_trace[++stack_trace_pointer] = &&${lbl_counter};\n"
    for arg in args:   
        out += f"push({value(arg)});\n"
    out +=f"""
goto {function_name};
${lbl_counter}:\n"""
    lbl_counter += 1
    if variable:
        out += "push(pop())"

def is_int(arg):
    return arg.isnumeric() 

def is_bool(arg):
    return arg in ["true", "false"]

corr_types = {"int": is_int, "boolean": is_bool}

def is_variable(arg):
    return ["A" <= x <= "x" or x == "_" or is_int(arg) for x in arg].count(True) == len(arg)

def value(arg):
    if is_int(arg) or is_bool(arg):
        return arg
    if is_variable(arg):
        return variable(arg)

def ret(arg):
    return f"set(0, {value(arg)});\ngoto *stack_trace[stack_trace_pointer--];\n"

def if_statement(arg):
    return f"if ({arg}) \{"