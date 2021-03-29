from util import *

from complex_expression import parse_expr as parse_complex_expr


def parse(program_name, to_print=True):
    with open(f"test/{program_name}.barter", "r") as f:
        parent = Node("program")
        for line in f.read().split(";"):
            line = line.strip()
            if line == "":
                continue
            node = parse_complex_expr(line)
            node.parent = parent
        if to_print:
            for pre, fill, node in RenderTree(parent):
                print("%s%s" % (pre, node.name))
        return parent


if __name__ == "__main__":
    parse("functionality")
