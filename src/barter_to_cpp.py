import re
import os
import sys

def split(string, delimiter=None):
    if delimiter is None:
        return [x.strip() for x in string.split()]
    else:
        return [x.strip() for x in string.split(delimiter)]

def re_replace(string):
    return re.sub(r' {2,}' , ' ', string)

file_name = sys.argv[1]
functions = {}
variables = []
types = ["int", "bool"]
int_operators = "+-/*"
bool_operators = ["<", ">", "==", "!=", "<=", ">="]
ind = 0
lbl_counter = 0

def check_function_signature(function_name, arguments):
    assert function_name in functions
    correct_arguments = functions[function_name]["arguments"]
    assert len(arguments) == len(correct_arguments), (arguments, correct_arguments)
    for ind, arg in enumerate(arguments):
        # assert corresponding_function(arg) == correct_arguments[ind]["type"]
        assert True


def variable(variable):
    variable = variable.strip()
    ind = variables[-1][variable]["ind"]
    return f"get({ind})"


def variable_declaration(line):
    line = line.strip()
    first, second = split(line, "=")
    typeof, var_name = split(first, " ")
    assert typeof in types
    line = second.strip()
    if "(" in line:
        assert line[-1] == ")"
        global lbl_counter
        function_name, arguments = split(line, "(")
        arguments = split(arguments[:-1], ",")
        check_function_signature(function_name, arguments)
        out = f"stack_trace[++stack_trace_pointer] = &&${lbl_counter};\n"
        for arg in arguments:   
            out += f"push({corresponding_function(arg)(arg)});\n"
        out += f"""goto {function_name};
${lbl_counter}:\n"""
        lbl_counter += 1
        expr = "pop()"
    else:
        out = "" 
        for sep in int_operators:
            if sep in line:
                arg1, arg2 = split(line, sep)
                f1 = corresponding_function(arg1)
                f2 = corresponding_function(arg2)
                expr = f"{f1(arg1)} {sep} {f2(arg2)}"
    global ind
    variables[-1][var_name] = {"type": typeof, "ind": ind}
    ind += 1
    return out + f"push({expr});\n"


def create_function(line):
    function_decl, arguments = split(line, "(")
    func, function_name = split(function_decl, " ")
    assert func == "func"
    arguments, return_type = split(arguments, ")")
    assert return_type[-1] == "{"
    return_type = return_type[:-1].strip()
    assert return_type in types or return_type == "void"
    arguments = split(arguments, ",")
    arg_list = []
    if arguments != [""]:
        for arg in arguments:
            typeof, arg_name = split(arg, " ")
            assert typeof in types, typeof
            arg_list.append({"type": typeof, "arg_name": arg_name})
    functions[function_name] = {"arguments": arg_list, "return_type": return_type, "body":[]}
    return functions[function_name]

def if_statement(line):
    line = line.strip()
    assert line[:2] == "if"
    assert line[-1] == "{" 
    statement = line[2:-1].strip()
    for sep in bool_operators:
        if sep in statement:
            arg1, arg2 = split(statement, sep)
            f1 = corresponding_function(arg1)
            f2 = corresponding_function(arg2)
            expr = f"{f1(arg1)} {sep} {f2(arg2)}"
            return "if (" + expr + "){\n"
    raise Exception("if statement")


def while_statement(line):
    line = line.strip()
    assert line[:5] == "while"
    statement = line[5:].strip()
    for sep in bool_operators:
        if sep in statement:
            arg1, arg2 = split(statement, sep)
            return statement


def do_nothing(line):
    return line

def add_end_line(line):
    return line + "\n"

def return_statement(line):
    _, ret = split(line, " ")
    return f"set(0, {corresponding_function(ret)(ret)});\ngoto *stack_trace[stack_trace_pointer--];\n"

def print_statement(line):
    _, args = split(line, "(")
    assert args[-1] == ")"
    args = split(args[:-1], ",")
    out = "cout << "
    for arg in args:
        out += corresponding_function(arg)(arg)
        out += ' << " " << '
    out += "'\\n';\n"
    return out

def corresponding_function(string):
    string = string.strip()
    if string.isnumeric():
        return do_nothing
    if string == "}":
        return add_end_line
    if string in variables[-1]:
        return variable
    if string[:2] == "if":
        return if_statement
    if string[:3] in types:
        return variable_declaration
    if string[:len("return")] == "return":
        return return_statement
    if string[:len("print")] == "print":
        return print_statement

def create_headers(text):
    # text = re_replace(text)
    bracket_control = 0
    current = None
    for line in split(text, "\n"):
        if line == "":
            continue
        if bracket_control == 0:
            assert line[:4] == "func"
            bracket_control += 1
            current = create_function(line) 
        else:
            if line == "}":
                bracket_control -= 1
            elif line[-1] == "{":
                bracket_control += 1
            if bracket_control != 0:
                current["body"].append(line)

def create_program():
    default = """
#include <iostream>
#include <vector>
using std::vector;
using std::cout;
int R1 = 0;
vector<void*> stack_trace(40);
vector<long> stack(40);
int stack_trace_pointer = -1;
int stack_pointer = -1;
inline void push(int x){
    stack[++stack_pointer] = x;
}
inline int pop(){
    return stack[stack_pointer--];
}
inline int get(int n){
    return stack[R1 + n];
}
inline void set(int n, int value){
    stack[R1 + n] = value;
}
int main(){
goto main;
"""
    for function_name in functions:
        function = functions[function_name]
        variables.append({})
        global ind
        ind = 0
        default += f"{function_name}:\n"
        for i, arg in enumerate(function["arguments"]):
            default += f"push(stack[stack_pointer - {len(function['arguments']) - 1}]);\n"
            variables[-1][arg["arg_name"]] = {"type": arg["type"], "ind": ind}
            ind += 1
        default += f"R1 = stack_pointer - {len(function['arguments'])} + 1;\n"
        for line in function["body"]:
            foo = corresponding_function(line)
            default += foo(line)
        # if function_name != "main":
        #     default += "goto *stack_trace[stack_trace_pointer--];\n"
        variables.pop()
    default += "}\n"
    with open(f"test/out/{file_name}.cpp", "w") as file:
        file.write(default)
    os.system(f'g++ test/out/{file_name}.cpp -o test/out/{file_name}')
    os.system(rf".\\test\\out\\{file_name}.exe")


if __name__ == "__main__":
    with open(f"test/{file_name}.barter", "r") as file:
        create_headers(file.read())
    create_program()