from util import *

from complex_expression import parse_expr as parse_complex_expr


def parse(program_name, to_print=True):
    with open(f"test/{program_name}.barter", "r") as f:
        parent = Node("program")
        lines = ""
        for line in f.readlines():
            lines += line.split("//")[0].strip()
        for line in lines.split(";"):
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
