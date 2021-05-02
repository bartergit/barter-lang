from create_ast import *


class Global:
    variables = {}
    arrays = {}
    functions = {}
    ind = 0
    label = 1
    return_type = None
    corresponding = {
        "sum": signature("int", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "dif": signature("int", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "mul": signature("int", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "div": signature("int", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "lt": signature("bool", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "eq": signature("bool", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "bt": signature("bool", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "mod": signature("int", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "cout": signature("void", [expression(value='x', type='int')], sum)
    }
