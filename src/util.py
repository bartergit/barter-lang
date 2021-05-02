from anytree import Node, RenderTree
from collections import namedtuple

variable_declaration = namedtuple('variable_declaration', 'type name')
function_declaration = namedtuple('function_declaration', 'name return_type')
assignment = namedtuple('assign', 'name')
###
###
signature = namedtuple('signature', 'return_type args body')
expression = namedtuple('expression', 'value type')
variable = namedtuple('variable', 'name')
constant = namedtuple('constant', 'type value')
indexed_var = namedtuple('indexed_var', 'type ind')
function_call = namedtuple('function_call', 'function_name')
bin_op = namedtuple('bin_op', 'sign')
unary_op = namedtuple('unary_op', 'sign')

types = ["int", "bool"]
operators = ["<=", ">=", "+", "-", "*", "/", "==", "!=", "<", ">", "!"]
special = ["while", "for", "true", "false", "if", "func"] + types

def is_correct_var_name(string):
    return ["A" <= x <= "z" or x == "_" or x.isnumeric() for x in string[1:]].count(True) == len(string) - 1 \
           and ("A" <= string[0] <= "z" or string[0] == "_") and string not in special

def parse_value(string):
    if string[-1] == string[0] == "'":
        return constant("str", string[1:-1])
    if string in ["true", "false"]:
        return constant("bool", string)
    if string.isnumeric():
        return constant("int", string)
    if is_correct_var_name(string):
        return variable(string)
    raise Exception(f"syntax error in {string}", string)

def split(string, delimiter=None):
    if delimiter is None:
        return [x.strip() for x in string.split()]
    else:
        return [x.strip() for x in string.split(delimiter)]


def print_tree(t):
    for pre, fill, node in RenderTree(t):
        print("%s%s" % (pre, node.name))