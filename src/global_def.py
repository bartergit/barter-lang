from create_ast import *


class Global:
    variables = {}
    arrays = {}
    functions = {}
    ind = 0
    label = 1
    return_type = None
    corresponding = {
        "sum": signature("int", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "dif": signature("int", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "mul": signature("int", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "div": signature("int", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "lt": signature("bool", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "eq": signature("bool", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "bt": signature("bool", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "mod": signature("int", [variable_declaration(name='x', type='int'), variable_declaration(name='y', type='int')], None),
        "cout": signature("void", [variable_declaration(name='x', type='int')], None)
    }
