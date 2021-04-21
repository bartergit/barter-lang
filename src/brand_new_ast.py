from util import *
from complex_expression import parse_expr


def parse_block(listing):
    block = Node("block")
    for line in listing.split("\n"):
        split_line = line.strip().split()
        if not len(split_line) or split_line[0].startswith("//"):
            continue
        if len(split_line) == 1:
            parse_expr(split_line[0]).parent = block
        elif split_line[0] in types:
            typeof, name, _, value = split_line
            parsed_value = parse_expr(value)
            parent = Node(variable_declaration(typeof, name), parent=block)
            parsed_value.parent = parent
        elif split_line[1] == "=":
            name, _, value = split_line
            parsed_value = parse_expr(value)
            parent = Node(assignment(name), parent=block)
            parsed_value.parent = parent
        elif split_line[0] == "return" and len(split_line) == 2:
            _, value = split_line
            parsed_value = parse_expr(value)
            parent = Node("return", parent=block)
            parsed_value.parent = parent
        elif split_line[0] == "return" and len(split_line) == 1:
            parent = Node("return_void", parent=block)
    return block


def parse_program(listing):
    funcs = listing.split("}")
    program_node = Node("program")
    for function in funcs:
        bracket_ind = function.find("{")
        function_desc = function[:bracket_ind].strip()
        if len(function_desc) == 0:
            continue
        function_body_text = function[bracket_ind + 1:]
        split_function_desc = function_desc.split()
        func, name, tmp_args, return_type = split_function_desc[0], split_function_desc[1], split_function_desc[2:-1], \
                                        split_function_desc[-1]  # no args for now
        args = []
        if len(tmp_args) > 1:
            for i in range(0,len(tmp_args),2):
                args.append(variable_declaration(tmp_args[i], tmp_args[i+1]))
            args[0] = variable_declaration(args[0].type[1:], args[0].name)
            args[-1] = variable_declaration(args[-1].type, args[-1].name[:-1])
        name = name
        assert func == "func"
        function_node = Node(function_declaration(name, return_type), parent=program_node)
        Node("arguments", parent=function_node).children = [Node(x) for x in args]
        parse_block(function_body_text).parent = function_node
    return program_node


def main():
    listing = """
    func hello() void {
        cout(3,3,3,3)
    }
    func main() void {
        int x = 0
        hello()
        int y = sum(x,0)
        cout(2,9,sum(3,1))
    }
    """
    program_node = parse_program(listing)
    print_tree(program_node)


if __name__ == '__main__':
    main()
