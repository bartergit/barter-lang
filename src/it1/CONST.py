types = ["str", "bool", "int"]
operations = ["+", "-", "*", "/"]
special = ["true", "false", "return", "void"]
first_priority_operations = ["*", "/"]
sec_priority_operations = ["+", "-"]
# op -> var | (
# var -> op | )
# ( -> op | ( | var


# func = func name (type name,) type
# func  -> {
# {     -> } | dec
# dec   -> } | dec
# }     -> func | end